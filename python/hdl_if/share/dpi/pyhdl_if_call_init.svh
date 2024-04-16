
function automatic bit __pyhdl_if_call_init();
    // PyObject __sv_init = null;
    // PyObject res;

    // // Register ourselves with the Python side
    // __hdl_call_if = pyhdl_pi_if_HandleErr(PyImport_ImportModule("hdl_call_if"));
    // if (__hdl_call_if == null) begin
    //     $display("Internal Error: Failed to find Python package hdl_call_if");
    //     $finish;
    // end
    // __sv_init = pyhdl_pi_if_HandleErr(PyObject_GetAttrString(__hdl_call_if, "__sv_init"));
    // if (__sv_init == null) begin
    //     $display("Internal Error: Failed to find __sv_init method");
    //     $finish;
    // end
    // Py_IncRef(__sv_init);
    // begin
    //     PyObject args = PyTuple_New(1);
    //     PyObject scope = PyLong_FromVoidPtr(svGetScope());
    //     int ret;

    //     Py_IncRef(scope);
    //     ret = PyTuple_SetItem(args, 0, scope);
    //     res = PyObject_Call(__sv_init, args, null);

    //     if (res == null) begin
    //         $display("Internal Error: Failed to run __sv_init");
    //         $finish;
    //     end
    //     __ep_h = res;
    // end
    return 1;
endfunction
