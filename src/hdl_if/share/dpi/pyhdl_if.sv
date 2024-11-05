/**
 * pyhdl_if.sv
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
 * Created on
 *     Author: 
 */
package pyhdl_if;

    `include "pyhdl_dpi_imports.svh"

    import "DPI-C" context function int pyhdl_if_dpi_entry();

    // Cached handles to Python objects
    PyObject        None;
    PyObject __hdl_pi_if;
    PyObject __backend;
    PyObject __mkTask;

    // TLM interface fields
    PyObject            stream_rgy;
    PyObject            register_stream;
    PyObject            stream_req_t;
    PyObject            stream_rsp_t;

    typedef enum {
        StreamKind_Req,
        StreamKind_Rsp,
        StreamKind_ReqRsp
    } stream_kind_e;

    interface class PyHdlPiRunnable;
        pure virtual task run();
    endclass

    // 
    bit                                 prv_run_q_running = 0;
    mailbox #(PyHdlPiRunnable)          prv_run_q = new();
    task automatic __pyhdl_pi_if_run();
        forever begin
            automatic PyHdlPiRunnable runnable;
            prv_run_q.get(runnable);

            fork
                begin
                    runnable.run();
                end
            join_none
        end
    endtask

    function automatic void pyhdl_pi_if_queue_runnable(PyHdlPiRunnable runnable);
        if (!prv_run_q_running && $time > 0) begin
            $display("PyHDL-Pi-IF Fatal Error: SV event loop is not running at time %0t", $time);
            $finish;
        end
        void'(prv_run_q.try_put(runnable));
    endfunction

    function void pyhdl_if_start();
        if (!prv_run_q_running) begin
            prv_run_q_running = 1;
            fork
                __pyhdl_pi_if_run();
            join_none
        end
    endfunction

    // Deprecated
    function void pyhdl_pi_if_start();
        pyhdl_if_start();
    endfunction

    typedef class PyHdlDpiTimeCB;
    PyHdlDpiTimeCB          prv_time_cb[$];

    `include "pyhdl_if_time_cb.svh"    
    `include "pyhdl_if_pi_dpi.svh"


    // Allows the Python environment to process events
    function automatic void pyhdl_pi_if_idle();
        PyObject args, idle_h, backend_m, backend_c, inst_m;
        if (__backend == null) begin
            backend_m = PyImport_ImportModule("hdl_if.backend");
            backend_c = PyObject_GetAttrString(backend_m, "Backend");
            inst_m = PyObject_GetAttrString(backend_c, "inst");
            args = PyTuple_New(0);
            __backend = PyObject_Call(inst_m, args, null);
            Py_DecRef(args);
        end
        args = PyTuple_New(0);
        idle_h = PyObject_GetAttrString(__backend, "idle");
        void'(pyhdl_pi_if_HandleErr(PyObject_Call(idle_h, args, null)));
        Py_DecRef(args);
    endfunction

    function automatic PyObject pyhdl_pi_if_getBackend();
        PyObject args, backend_m, backend_c, inst_m;
        if (__backend == null) begin
            backend_m = PyImport_ImportModule("hdl_if.backend");
            backend_c = PyObject_GetAttrString(backend_m, "Backend");
            inst_m = PyObject_GetAttrString(backend_c, "inst");
            args = PyTuple_New(0);
            __backend = PyObject_Call(inst_m, args, null);
            Py_DecRef(args);
        end
        return __backend;
    endfunction

    function automatic PyObject pyhdl_pi_if_HandleErr(PyObject obj);
        if (obj == null) begin
            PyErr_Print();
        end
        return obj;
    endfunction

    
    function automatic PyObject pyhdl_pi_if_mkTask(PyObject callable);
        PyObject args;
        args = PyTuple_New(1);
        void'(PyTuple_SetItem(args, 0, callable));
        return pyhdl_pi_if_HandleErr(PyObject_Call(__mkTask, args, null));
    endfunction

    /**
     * pyhdl_pi_if_NewClass
     *
     * Create a new class object, given a package/class name and arguments
     */
    function automatic PyObject pyhdl_pi_if_NewClass(
        string                  pkg_name,
        string                  cls_name,
        PyObject                args[$]);
        PyObject pkg, cls_t, args_o;

        pkg = PyImport_ImportModule(pkg_name);
        cls_t = PyObject_GetAttrString(pkg, cls_name);
        args_o = PyTuple_New(args.size());

        foreach (args[i]) begin
            void'(PyTuple_SetItem(args_o, i, args[i]));
        end

        return PyObject_Call(cls_t, args_o, null);
    endfunction

    /****************************************************************
     * PyHDL-IF Call 
     ****************************************************************/
    typedef interface class ICallApi;

    PyObject            __hdl_call_if;
    PyObject            __ep_h;
    ICallApi            __objects[];
    semaphore           __callsem[];
    PyObject            __callsem_res[];

    // Empty base class
    class CallEmptyBase;
    endclass

    // Empty base class (UVM-Friendly)
    class CallEmptyUvmBase;
        function new(string name="base");
        endfunction
    endclass

    `include "pyhdl_if_taskcall_closure.svh"
    `include "pyhdl_if_icall_api.svh"
    `include "pyhdl_if_call_init.svh"
    `include "pyhdl_if_call_api.svh"
    `include "pyhdl_if_call_dpi.svh"

    `include "pyhdl_if_tlm_init.svh"

    `include "pyhdl_if_init.svh"
    function automatic bit __do_init();
        bit ret = __pyhdl_if_init();
        return ret;
    endfunction

    bit __init = __do_init();

    /****************************************************************
     * PyHDL-IF TLM 
     ****************************************************************/

    function automatic PyObject pyhdl_tlm_if_registerStream(
        stream_kind_e   kind,
        string          iname,
        ICallApi        impl);
        PyObject args, obj_h;
        
        args = PyTuple_New(1);

        void'(PyTuple_SetItem(args, 0, PyUnicode_FromString(iname)));

        case (kind)
            StreamKind_Req:
                obj_h = pyhdl_if_newObject(stream_req_t, impl, args);
            StreamKind_Rsp:
                obj_h = pyhdl_if_newObject(stream_rsp_t, impl, args);
            default: begin
                $display("Fatal Error: unknown stream type");
                $finish;
            end
        endcase

        begin
            args = PyTuple_New(1);
            void'(PyTuple_SetItem(args, 0, obj_h));
            void'(pyhdl_pi_if_HandleErr(PyObject_Call(register_stream, args, null)));
        end

        return obj_h;
    endfunction

endpackage

