
module test_smoke;
    import pyhdl_if::*;

    initial begin
        py_object smoke_test_m = py_import("smoke_test");
        py_object foo = smoke_test_m.get_attr("foo");
        int ret = foo.call().to_long();

        begin
            int fp = $fopen("status.txt", "w");
            if (ret == 27) begin
                $fwrite(fp, "PASS:\n");
            end else begin
                $fwrite(fp, "FAIL: %0d != 27\n", ret);
            end
            $fclose(fp);
        end
        $finish;
    end
endmodule