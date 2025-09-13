package datatypes_int_imp;
    import datatypes_int_imp_pkg::*;

    class IntImpImpl extends IntImp;
        function int add(int a, int b);
            return a+b;
        endfunction
    endclass
endpackage

module top;
    import pyhdl_if::*;
    import datatypes_int_imp::*;

    initial begin
        automatic IntImpImpl int_imp = new();
        automatic int status = 0, fp;

        $display("Hello World!");
        status = int_imp.test();

        fp = $fopen("status.txt", "w");
        if (status == 0) begin
            $fwrite(fp, "PASS:\n");
        end else begin
            $fwrite(fp, "FAIL:\n");
        end
        $fclose(fp);
        $finish;
    end
endmodule
