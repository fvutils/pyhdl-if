
package datatypes_real_exp;
endpackage


module top;
    import pyhdl_if::*;
    import datatypes_real_exp_pkg::*;

    initial begin
        automatic RealExp real_exp = new();
        automatic int i, j;
        automatic real result;
        automatic int status = 0, fp;

        $display("Hello World!");
        for (i=0; i<10; i++) begin
            for (j=0; j<10; j++) begin
                result = real_exp.add(real'(i), real'(j));
                if (result != (real'(i) + real'(j))) begin
                    $display("Error: %0d+%0d: expect %0f ; receive %0f",
                        i, j, (real'(i) + real'(j)), result);
                    status = 1;
                end
            end
        end

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

