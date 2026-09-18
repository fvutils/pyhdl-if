/**
 * pyhdl_if_call_api.sv
 *
 * Copyright 2024 Matthew Ballance and Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may 
 * not use this file except in compliance with the License.  
 * You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software 
 * distributed under the License is distributed on an "AS IS" BASIS, 
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
 * See the License for the specific language governing permissions and 
 * limitations under the License.
 *
 * Created on:
 *     Author: 
 */

    /**
     * Calls a Python coroutine and blocks until it completes.
     *
     * Use this for a method that may suspend. The call is handed to the Python
     * event loop and this task waits on a semaphore, releasing the GIL while it
     * does, so the coroutine -- and anything else Python has scheduled -- can
     * run. #pyhdl_if_invokePyFunc is the non-blocking counterpart.
     *
     * @param res Value the coroutine returned. Never null; a Python `None`
     *        arrives as the `None` handle rather than a null handle.
     * @param obj The Python object to call the method on.
     * @param method Name of the method to invoke.
     * @param args Positional arguments, as a Python tuple. Ownership passes to
     *        the callee.
     */
    task automatic pyhdl_if_invokePyTask(
        output PyObject     res,
        input PyObject      obj,
        input string        method,
        input PyObject      args);
        int sem_id = pyhdl_if_allocSem();
        PyObject proxy_h, invoke_py_t, proxy_args;
        PyGILState_STATE state;

        state = PyGILState_Ensure();

        // Track this SV->Python call
        __sv2py_call++;

        proxy_h = PyObject_GetAttrString(obj, "_proxy");
        invoke_py_t = PyObject_GetAttrString(proxy_h, "invoke_py_t");
        proxy_args = PyTuple_New(3);

        void'(PyTuple_SetItem(proxy_args, 0, PyLong_FromLong(longint'(sem_id))));
        void'(PyTuple_SetItem(proxy_args, 1, PyUnicode_FromString(method)));
        void'(PyTuple_SetItem(proxy_args, 2, args));

        void'(pyhdl_pi_if_HandleErr(PyObject_Call(invoke_py_t, proxy_args, null)));

        pyhdl_if_waitSem(sem_id, res, state);

        PyGILState_Release(state);

        // Call completed
        __sv2py_resp++;

    endtask

    /**
     * Calls a plain Python method and returns its result.
     *
     * The call runs to completion inside this function, so the method must not
     * suspend -- use #pyhdl_if_invokePyTask for a coroutine. The GIL is taken
     * for the duration and released before returning.
     *
     * @param obj The Python object to call the method on.
     * @param method Name of the method to invoke.
     * @param args Positional arguments, as a Python tuple. Ownership passes to
     *        the callee.
     * @return The returned object, or null if the call raised. The exception
     *         has already been printed.
     */
    function automatic PyObject pyhdl_if_invokePyFunc(
        input PyObject      obj,
        input string        method,
        input PyObject      args);
        PyObject res, proxy_h, invoke_py_f, proxy_args;
        PyGILState_STATE state;

        state = PyGILState_Ensure();

        proxy_h = PyObject_GetAttrString(obj, "_proxy");
        invoke_py_f = PyObject_GetAttrString(proxy_h, "invoke_py_f");
        proxy_args = PyTuple_New(2);

        void'(PyTuple_SetItem(proxy_args, 0, PyUnicode_FromString(method)));
        void'(PyTuple_SetItem(proxy_args, 1, args));

        res = pyhdl_pi_if_HandleErr(PyObject_Call(invoke_py_f, proxy_args, null));

        PyGILState_Release(state);

        return res;
    endfunction

    /**
     * Reserves a slot in the object table for a SystemVerilog callee.
     *
     * The table maps the integer the Python side carries back to the object
     * that should receive the call, because a class handle cannot cross the
     * DPI boundary. A freed slot is reused; the table grows 64 entries at a
     * time when none is free.
     *
     * @param sv_api_if The object to register. Its `invokeFunc`/`invokeTask`
     *        are what an incoming call dispatches to.
     * @return The slot index, which becomes the object's id.
     */
    function automatic int allocObjId(ICallApi sv_api_if);
        int ret = -1, i;

        for (i=0; i<__objects.size(); i++) begin
            if (__objects[i] == null) begin
                ret = i;
                break;
            end
        end

        if (ret == -1) begin
            __objects = new[__objects.size()+64](__objects);
            ret = i;
        end

        __objects[ret] = sv_api_if;

        return ret;
    endfunction

    /**
     * Reserves a semaphore for one in-flight call to Python.
     *
     * Each blocking call needs its own, since several may be outstanding at
     * once. Pair with #pyhdl_if_waitSem to wait and #pyhdl_if_setSem to
     * complete; the slot is released when the result is collected.
     *
     * @return The semaphore id, which travels with the call so the response
     *         can find its way back.
     */
    function automatic int pyhdl_if_allocSem();
        int ret = -1, i;

        for (i=0; i<__callsem_res.size(); i++) begin
            if (__callsem_res[i] == null) begin
                ret = i;
                break;
            end
        end

        if (ret == -1) begin
            __callsem = new[__callsem.size()+64](__callsem);
            __callsem_res = new[__callsem_res.size()+64](__callsem_res);
            for (int j=i; j<__callsem.size(); j++) begin
                __callsem[j] = new();
            end
            ret = i;
        end

        __callsem_res[ret] = None;

        return ret;
    endfunction

    /**
     * Waits for a call to Python to complete, without holding the GIL.
     *
     * Polls rather than blocking outright, because a Python thread may call
     * back into SystemVerilog while this one waits -- and that re-entry needs
     * both the GIL and the simulator's scheduler. Each pass pumps the Python
     * event loop, drops the GIL, yields, and takes it again. The loop ends when
     * the result arrives, or when a new Python-to-SystemVerilog call appears
     * and must be serviced first.
     *
     * @param id Semaphore id from #pyhdl_if_allocSem.
     * @param res The value the Python side returned.
     * @param state The caller's GIL state. Passed `inout` because this task
     *        releases and re-acquires it; the handle the caller holds after the
     *        call is not the one it passed in.
     */
    task automatic pyhdl_if_waitSem(
        input int           id,
        output PyObject     res,
        inout PyGILState_STATE state);
        // Wait for the semaphore while supporting Python threads that may call
        // back into SV via run_coroutine_threadsafe.
        //
        // Strategy: Keep polling idle() until either:
        // 1. Our call completes (semaphore is set)
        // 2. A new py2sv call or time delay is queued (py2sv is greater than initial)
        //
        // When work is queued, we yield with #0 to let __pyhdl_pi_if_run() process it.
        // We must NOT wait for simulation time here - that would block thread-initiated
        // calls which depend on idle() being pumped to process their scheduled coroutines.
        //
        // The loop exits via its condition, not 'break': verilator 5.044
        // --timing drops an assignment made just before a 'break' here.
        int initial_py2sv_call = __py2sv_call;
        bit have = 1'b0;
        bit done = 1'b0;
        `PYHDL_IF_DEBUG(("--> pyhdl_if_waitSem: id=%0d sv2py=%0d py2sv=%0d", id, __sv2py_call, __py2sv_resp));


        while (!done) begin
            `PYHDL_IF_DEBUG((
                "--> pyhdl_if_waitSem: poll sv2py_call=%0d py2sv_resp=%0d py2sv_call=%0d py2sv_resp=%0d",
                    __sv2py_call, __sv2py_resp, __py2sv_call, __py2sv_resp));
            if (__callsem[id].try_get() != 32'h0) begin
                `PYHDL_IF_DEBUG(("pyhdl_if_waitSem: callsem is valid"));
                have = 1'b1;
                done = 1'b1;
            end else if (__py2sv_call != initial_py2sv_call) begin
                `PYHDL_IF_DEBUG((
                    "pyhdl_if_waitSem: change in new calls: %0d -> %0d",
                    initial_py2sv_call, __py2sv_call));
                done = 1'b1;
            end else begin
                // Pump Python event loop to process scheduled coroutines
                pyhdl_pi_if_idle();
                PyGILState_Release(state);
                void'(pyhdl_if_sched_yield());
                #0; // Allow the SV scheduler to start new threads
                state = PyGILState_Ensure();
            end
        end

        if (have) begin
            `PYHDL_IF_DEBUG(("pyhdl_if_waitSem: call already complete"));
        end else begin
            `PYHDL_IF_DEBUG(("--> pyhdl_if_waitSem: wait for call to complete"));
            __callsem[id].get();
            `PYHDL_IF_DEBUG(("<-- pyhdl_if_waitSem: wait for call to complete"));
        end

        `PYHDL_IF_DEBUG(("pyhdl_if_waitSem: done id=%0d", id));
        res = __callsem_res[id];
        __callsem_res[id] = null;

        `PYHDL_IF_DEBUG(("<-- pyhdl_if_waitSem: id=%0d sv2py=%0d py2sv=%0d", id, __sv2py_call, __py2sv_resp));
    endtask

    /**
     * Completes a call to Python by publishing its result.
     *
     * Called from the response path when the coroutine finishes. Releases the
     * task waiting in #pyhdl_if_waitSem on the same id.
     *
     * @param id Semaphore id the call was issued with.
     * @param res Value to hand back to the waiting task.
     */
    function automatic void pyhdl_if_setSem(
        input int           id,
        input PyObject      res);
        // Python drops its reference when the coroutine returns, so hold one
        // for the waiter. Ownership passes to pyhdl_if_invokePyTask's caller.
        Py_IncRef(res);
        __callsem_res[id] = res;
        __callsem[id].put(1);
    endfunction

    /**
     * Constructs the Python peer of a SystemVerilog object.
     *
     * Calls the endpoint's `newObj`, which instantiates `cls_t` and binds it to
     * the SystemVerilog side so calls can travel in both directions.
     *
     * @param cls_t The Python class to instantiate.
     * @param sv_api_if The SystemVerilog object that should receive calls from
     *        Python. Pass null for a one-way object, which is given the id -1.
     * @param init_args Arguments for the constructor, as a Python tuple.
     * @return The new Python object, or null if construction raised.
     */
    function automatic PyObject pyhdl_if_newObject(
        PyObject        cls_t,
        ICallApi        sv_api_if,
        PyObject        init_args);
        int obj_id;
        PyObject args, ret, new_obj;
        PyGILState_STATE state;

        state = PyGILState_Ensure();

        new_obj = PyObject_GetAttrString(__ep_h, "newObj");
        args = PyTuple_New(3);

        obj_id = (sv_api_if != null)?allocObjId(sv_api_if):-1;

        Py_IncRef(new_obj);

        void'(PyTuple_SetItem(args, 0, cls_t));
        void'(PyTuple_SetItem(args, 1, PyLong_FromLong(longint'(obj_id))));
        void'(PyTuple_SetItem(args, 2, init_args));

        ret = pyhdl_pi_if_HandleErr(PyObject_Call(new_obj, args, null));

        Py_DecRef(new_obj);

        PyGILState_Release(state);

        return ret;
    endfunction

    /**
     * Publishes an object under a hierarchical path so Python can find it.
     *
     * The path is what a Python-side lookup binds against -- normally
     * `$sformatf("%m")` from the scope being registered.
     *
     * @param obj The Python object to publish.
     * @param inst_path Hierarchical path to publish it under.
     * @param trim_elems Leading path elements to drop, for trimming a testbench
     *        prefix that means nothing to the Python side.
     */
    function automatic void pyhdl_if_registerObject(
        PyObject            obj,
        string              inst_path,
        int                 trim_elems=0);
        PyObject args, ret, reg_obj;
        PyGILState_STATE state = PyGILState_Ensure();

        reg_obj = PyObject_GetAttrString(__ep_h, "registerObj");
        args = PyTuple_New(3);

        void'(PyTuple_SetItem(args, 0, obj));
        void'(PyTuple_SetItem(args, 1, PyUnicode_FromString(inst_path)));
        void'(PyTuple_SetItem(args, 2, PyLong_FromLong(longint'(trim_elems))));

        ret = pyhdl_pi_if_HandleErr(PyObject_Call(reg_obj, args, null));

        Py_DecRef(reg_obj);

        PyGILState_Release(state);
    endfunction

    /**
     * Binds an existing Python object to a SystemVerilog callee.
     *
     * Use this when the Python object already exists -- because Python created
     * it -- and only the reverse direction needs wiring.
     * #pyhdl_if_newObject does both at once for an object SystemVerilog
     * constructs.
     *
     * @param obj The Python object to connect.
     * @param sv_api_if The object incoming calls dispatch to. Null connects
     *        nothing, leaving the Python object one-way.
     */
    function automatic void pyhdl_if_connectObject(
        PyObject        obj,
        ICallApi        sv_api_if);
        int obj_id = (sv_api_if != null)?allocObjId(sv_api_if):-1;
        PyObject args, ret, connect;
        PyGILState_STATE state = PyGILState_Ensure();

        connect = PyObject_GetAttrString(__ep_h, "connectObj");
        args = PyTuple_New(2);

        void'(PyTuple_SetItem(args, 0, obj));
        void'(PyTuple_SetItem(args, 1, PyLong_FromLong(longint'(obj_id))));
        ret = PyObject_Call(connect, args, null);

        if (ret == null) begin
            `PYHDL_IF_ERROR(("exception while calling 'connectObj'"));
            `STACKTRACE;
            PyErr_Print();
        end
        PyGILState_Release(state);
    endfunction
