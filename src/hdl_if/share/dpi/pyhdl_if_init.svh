
function automatic bit __pyhdl_if_init();
    bit ret = 1;
    PyObject hdl_if_impl, hdl_if_impl_dpi, dpi_init, get_none, args, res;
    PyGILState_STATE state;

    if (pyhdl_if_dpi_entry() != 1) begin
        $display("Fatal: Failed to initialize pyhdl-pi-if DPI interface");
        $finish;
        return 0;
    end

    Py_Initialize();

    state = PyGILState_Ensure();

    __hdl_pi_if = pyhdl_pi_if_HandleErr(PyImport_ImportModule("hdl_if"));
    if (__hdl_pi_if == null) begin
        PyErr_Print();
        $display("Fatal: failed to load hdl_if");
        $finish;
    end

    hdl_if_impl = pyhdl_pi_if_HandleErr(PyImport_ImportModule("hdl_if.impl"));
    if (hdl_if_impl == null) begin
        $display("Fatal: failed to load hdl_if.impl");
        $finish;
    end

    hdl_if_impl_dpi = pyhdl_pi_if_HandleErr(PyImport_ImportModule("hdl_if.impl.dpi"));
    if (hdl_if_impl_dpi == null) begin
        $display("Fatal: failed to load hdl_if.impl.dpi");
        $finish;
    end
    dpi_init = PyObject_GetAttrString(hdl_if_impl_dpi, "dpi_init");
    if (dpi_init == null) begin
        ret = 0;
        $display("Fatal: failed to find dpi_init in hdl_if.impl.dpi");
        $finish;
    end

    args = PyTuple_New(0);

    __ep_h = pyhdl_pi_if_HandleErr(PyObject_Call(dpi_init, args, null));
    if (__ep_h == null) begin
        $display("Fatal: failed to initialize hdl_pi_if package");
        $finish;
    end

    get_none = PyObject_GetAttrString(hdl_if_impl, "get_none");
    args = PyTuple_New(0);
    None = PyObject_Call(get_none, args, null);

    __mkTask = PyObject_GetAttrString(hdl_if_impl, "mkTask");

    ret &= __pyhdl_if_call_init();

    ret &= __pyhdl_if_tlm_init();

    PyGILState_Release(state);

    return ret;
endfunction