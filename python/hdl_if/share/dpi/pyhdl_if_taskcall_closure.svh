
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
        m_obj = obj;
        m_evt_obj = evt_obj;
        m_method_name = method_name;
        m_args = args;
    endfunction

    virtual task run();
        PyObject evt_obj_set = PyObject_GetAttrString(m_evt_obj, "set");
        PyObject args = PyTuple_New(1);
        PyObject res;

        m_obj.invokeTask(res, m_method_name, m_args);

        if (res == null) begin
            res = None;
        end

        void'(PyTuple_SetItem(args, 0, res));
        res = PyObject_Call(evt_obj_set, args, null);

        if (res == null) begin
            $display("Internal Error: Failed to trigger pyhdl_call_if event");
            $finish;
        end
    endtask
endclass