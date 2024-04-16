
package sv_pkg;
    import pyhdl_dpi_if::*;
    function automatic void exp_func();
        $display("exp_func");
    endfunction
    export "DPI-C" function exp_func;

    import "DPI-C" context function chandle svGetScope();
    import "DPI-C" context function string svGetNameFromScope(chandle s);


    function automatic bit __do_init();
        automatic PyObject test_load_mod, init_m;
        automatic PyObject init_args, res;
        $display("Hello scope=%p (%0s)", svGetScope(), svGetNameFromScope(svGetScope()));
        $display("Hello scope=%p", svGetScope());

        test_load_mod = PyImport_ImportModule("load");
        if (test_load_mod == null) begin
            $display("Fail: failed to load 'load' module");
            $finish;
        end

        init_m = PyObject_GetAttrString(test_load_mod, "dpi_init");
        if (init_m == null) begin
            $display("Fail: failed to get 'init' module");
            $finish;
        end

        init_args = PyTuple_New(1);
        PyTuple_SetItem(init_args, 0, PyLong_FromVoidPtr(svGetScope()));

        res = PyObject_Call(init_m, init_args, null);

        Py_DecRef(init_args);
        Py_DecRef(res);

        return 1;
    endfunction
    bit __is_init = __do_init();
endpackage


module test_load;
    import pyhdl_dpi_if::*;
    import sv_pkg::*;

    initial begin
        #10ns;

        $my_task();

        $finish;
    end
endmodule
