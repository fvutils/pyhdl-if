
module a_plus_b;
    import pyhdl_if::*;

    initial begin
        py_object a_plus_b, foo;
        py_tuple args;
        PyObject ret_o;
        int ret;

        $display("-- 1");
	    py_gil_enter();

        $display("-- 2");
        a_plus_b = py_import("a_plus_b");
        $display("-- 3");
        foo = a_plus_b.get_attr("a_plus_b");
        $display("-- 4");

        if (foo == null) begin
            $display("foo is null");
        end else begin 
            $display("foo is not null");
            $display("foo: %0p", foo.borrow());
        end

        Py_IncRef(foo.obj);

        args = py_tuple::mk_init('{py_from_int(5), py_from_int(13)});

        $display("args.borrow: %0p", args.borrow());

        ret_o = PyObject_Call(foo.obj, args.borrow(), null);
/*
        ret_o = foo.call(py_tuple::mk_init('{
            py_from_int(5), py_from_int(13)}));
//        ret = foo.call('{py_from_long(5), py_from_long(13)}).to_int();

        $display("-- 5");
        ret = ret_o.to_int();

        $display("-- 6");

	    py_gil_leave();

        $display("-- 6");

        $display("-- 7");
 */

        begin
            int fp = $fopen("status.txt", "w");
            if (ret == 18) begin
                $fwrite(fp, "PASS:\n");
            end else begin
                $fwrite(fp, "FAIL: %0d != 18\n", ret);
            end
            $fclose(fp);
        end
        $finish;
    end

endmodule
