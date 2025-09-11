
package datatypes_real_imp;
    import datatypes_real_imp_pkg::*;

    class RealImpImpl extends RealImp;
        function real add(real a, real b);
            $display("Hello from add");
            return a+b;
        endfunction
    endclass
endpackage


module top;
    import pyhdl_if::*;
    import datatypes_real_imp::*;

    initial begin
        automatic RealImpImpl real_imp = new();
        automatic int status = 0, fp;

        $display("Hello World!");
        status = real_imp.test();

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

