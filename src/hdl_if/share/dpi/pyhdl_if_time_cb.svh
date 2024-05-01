
class PyHdlDpiTimeCB implements PyHdlPiRunnable;
    PyObject            m_target;
    int                 m_cb_id;
    longint unsigned    m_time_ps;

    function new(
        PyObject            target, 
        int                 cb_id,
        longint unsigned    time_ps);
        m_target = target;
        Py_IncRef(m_target);
        m_cb_id = cb_id;
        m_time_ps = time_ps;
    endfunction

    virtual task run();
        PyObject backend, args, callCallback;
        #(m_time_ps * 1ps);
        if (m_cb_id != -1) begin
            backend = pyhdl_pi_if_getBackend();
            args = PyTuple_New(1);
            callCallback = PyObject_GetAttrString(backend, "callCallback");
            void'(PyTuple_SetItem(args, 0, m_target));
            if (pyhdl_pi_if_HandleErr(PyObject_Call(callCallback, args, null)) == null) begin
                $display("Fatal Error: failed to invoke timed callback");
                $finish;
            end
            prv_time_cb[m_cb_id] = null;
        end
    endtask
endclass