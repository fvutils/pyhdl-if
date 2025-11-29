
module a_plus_b;
    import pyhdl_if::*;

    initial begin
        py_object a_plus_b, foo;
        int ret;

	    py_gil_enter();

        a_plus_b = py_import("a_plus_b");
        foo = a_plus_b.get_attr("a_plus_b");

        ret = foo.call(py_tuple::mk_init('{
            py_from_int(5), py_from_int(13)})).to_int();
//        ret = foo.call('{py_from_long(5), py_from_long(13)}).to_int();
	    py_gil_leave();

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
