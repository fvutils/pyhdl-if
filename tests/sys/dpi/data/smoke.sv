
module smoke;
    import pyhdl_call_if::*;
    import pyhdl_dpi_if::*;

    class MyC;
        PyObject        m_obj;
        function new();
            PyObject smoke_obj, smoke_c;
            PyObject args, obj_h;

            if ((smoke_obj = PyImport_ImportModule("smoke")) == null) begin
                $display("Fatal: failed to import smoke");
                $finish;
            end
            if ((smoke_c = PyObject_GetAttrString(smoke_obj, "Smoke")) == null) begin
                $display("Fatal: failed to find Smoke");
                $finish;
            end

            args = PyTuple_New(0);
            Py_IncRef(smoke_c);
            m_obj = pyhdl_call_if_new(smoke_c, args);
        endfunction

        function int sum(int a, int b);
            PyObject args = PyTuple_New(2);
            PyObject func = PyObject_GetAttrString(m_obj, "sum");
            PyObject res;
            int ret;

            PyTuple_SetItem(args, 0, PyLong_FromLong(a));
            PyTuple_SetItem(args, 1, PyLong_FromLong(b));

            res = PyObject_Call(func, args, null);

            ret = PyLong_AsLong(res);

            pyhdl_pi_if_idle();

            return ret;
        endfunction
    endclass

    initial begin
        automatic MyC ci = new();

        $display("smoke");
        $display("1+2 = %0d", ci.sum(1, 2));
    end

endmodule
