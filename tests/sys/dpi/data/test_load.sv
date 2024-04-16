
module test_load;
    import pyhdl_dpi_if::*;

    initial begin
        automatic PyObject test_load_mod, init_m;
        automatic PyObject init_args, res;
        $display("Hello");

        test_load_mod = PyImport_ImportModule("test_load");
        if (test_load_mod == null) begin
            $display("Fail: failed to load 'test_load' module");
            $finish;
        end

        init_m = PyObject_GetAttrString(test_load_mod, "init");
        if (init_m == null) begin
            $display("Fail: failed to get 'init' module");
            $finish;
        end

        init_args = PyTuple_New(0);

        res = PyObject_Call(init_m, init_args, null);

        Py_DecRef(init_args);
        Py_DecRef(res);

        $finish;
    end
endmodule
