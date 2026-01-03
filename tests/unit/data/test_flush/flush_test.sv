
module flush_test;
    import pyhdl_if::*;
    import flush_test_pkg::*;

    reg clk = 0;
    
    initial begin
        clk = 0;
        forever begin
            #5ns;
            clk = ~clk;
        end
    end

    SVHelperImpl helper(.clock(clk));

    initial begin
        automatic Test_exp_impl test;

        pyhdl_if_start();

        #50ns;

        $display("[SV %0t] Starting test", $time);
        test = new();
        test.run(helper.m_helper.m_obj);
        $display("[SV %0t] Test completed", $time);
        $finish;
    end

endmodule
