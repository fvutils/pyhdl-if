
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

        evt_obj_set = PyObject_GetAttrString(m_evt_obj, "set");
        args = PyTuple_New(1);

        m_obj.invokeTask(res, state, m_method_name, m_args);

        if (res == null) begin
            res = None;
        end

        void'(PyTuple_SetItem(args, 0, res));
        res = PyObject_Call(evt_obj_set, args, null);

        if (res == null) begin
            $display("Internal Error: Failed to trigger pyhdl_call_if event");
            $finish;
        end

        PyGILState_Release(state);
        `PYHDL_IF_LEAVE(("TaskCallClosure::run(method=%0s)", m_method_name));
    endtask
endclass