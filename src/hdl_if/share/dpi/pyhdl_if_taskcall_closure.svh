
class TaskCallClosure implements PyHdlPiRunnable;
    ICallApi        m_obj;
    PyObject        m_evt_obj;
    string          m_method_name;
    PyObject        m_args;

    function new(
        ICallApi        obj,
        PyObject        evt_obj,
        string          method_name,
        PyObject        args);
        `PYHDL_IF_ENTER(("TaskCallClosure::new(method=%0s)", method_name));
        m_obj = obj;
        m_evt_obj = evt_obj;
        m_method_name = method_name;
        `PYHDL_IF_DEBUG(("m_method_name=%0s", m_method_name));
        m_args = args;
        `PYHDL_IF_LEAVE(("TaskCallClosure::new(method=%0s)", method_name));
    endfunction

    virtual task run();
        PyObject args, res, evt_obj_set;
        PyGILState_STATE state = PyGILState_Ensure();
        `PYHDL_IF_ENTER(("TaskCallClosure::run(method=%0s)", m_method_name));

        // Track this Python->SV call when it actually starts executing
        __py2sv_call++;
        `PYHDL_IF_DEBUG(("TaskCallClosure::run py2sv++ = %0d (method=%s)", __py2sv_call, m_method_name));

        evt_obj_set = PyObject_GetAttrString(m_evt_obj, "set");
        args = PyTuple_New(1);

        m_obj.invokeTask(res, state, m_method_name, m_args);

        // Signal Python->SV call completed by incrementing resp
        __py2sv_resp++;
        `PYHDL_IF_DEBUG(("TaskCallClosure::run py2sv-- = %0d (method=%s)", __py2sv_call, m_method_name));

        if (res == null) begin
            res = None;
        end

        `PYHDL_IF_DEBUG((
            "--> TaskCallClosure: Send call completion: py2sv_call=%0d py2sv_resp=%0d sv2py_call=%0d sv2py_resp=%0d",
            __py2sv_call, __py2sv_resp, __sv2py_call, __sv2py_resp));
        void'(PyTuple_SetItem(args, 0, res));
        res = PyObject_Call(evt_obj_set, args, null);
        `PYHDL_IF_DEBUG((
            "<-- TaskCallClosure: Send call completion: py2sv_call=%0d py2sv_resp=%0d sv2py_call=%0d sv2py_resp=%0d",
            __py2sv_call, __py2sv_resp, __sv2py_call, __sv2py_resp));

        if (res == null) begin
            $display("Internal Error: Failed to trigger pyhdl_call_if event");
            $finish;
        end

        // If there are pending sv2py calls, poll until something changes
        if (__sv2py_call != __sv2py_resp) begin
            int py2sv_call_curr = __py2sv_call;
            int py2sv_resp_curr = __py2sv_resp;
            int sv2py_call_curr = __sv2py_call;
            int sv2py_resp_curr = __sv2py_resp;
            `PYHDL_IF_DEBUG((
                "TaskCallClosure::run - poll waiting for a change: ps_c=%0d ps_r=%0d sp_c=%0d sp_r=%0d",
                __py2sv_call, __py2sv_resp, __sv2py_call, __sv2py_resp));
            while (
                py2sv_call_curr == __py2sv_call 
                && py2sv_resp_curr == __py2sv_resp
                && sv2py_call_curr == __sv2py_call
                && sv2py_resp_curr == __sv2py_resp) begin
                `PYHDL_IF_DEBUG(("TaskCallClosure::run --> poll"));
                pyhdl_pi_if_idle();
                PyGILState_Release(state);
                void'(pyhdl_if_sched_yield());
                #0; // Allow the SV scheduler to start new threads
                state = PyGILState_Ensure();
                `PYHDL_IF_DEBUG(("TaskCallClosure::run <-- poll"));
            end
            `PYHDL_IF_DEBUG((
                "TaskCallClosure::run - done waiting for a change: ps_c=%0d ps_r=%0d sp_c=%0d sp_r=%0d",
                __py2sv_call, __py2sv_resp, __sv2py_call, __sv2py_resp));
        end else begin
            `PYHDL_IF_DEBUG(("TaskCallClosure::run - no outstanding sv2py ... which is odd"));
        end

        PyGILState_Release(state);
        `PYHDL_IF_LEAVE(("TaskCallClosure::run(method=%0s)", m_method_name));
    endtask
endclass