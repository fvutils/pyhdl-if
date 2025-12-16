
module perf_bfm;
    import pyhdl_if::*;
    import perf_test_pkg::*;

    // Call counter
    int unsigned call_count = 0;

    // BFM implementation class
    class PerfBfmImpl extends PerfBfm_imp_impl #(PerfBfmImpl);

        function new();
            super.new(this);
        endfunction

        virtual task do_work(output int unsigned retval);
            // Simple task that consumes 1ns and returns call count
            call_count++;
            retval = call_count;
            #1ns;
        endtask

    endclass

    PerfBfmImpl m_bfm;

    initial begin
        automatic PerfTest_exp_impl test;

        // Start the PyHDL-IF event loop
        pyhdl_if_start();

        // Create the BFM implementation
        m_bfm = new();

        // Register the BFM object
        pyhdl_if::pyhdl_if_registerObject(m_bfm.m_obj, $sformatf("%m.m_bfm"), 1);

        // Small delay
        #10ns;

        // Create test instance and run
        $display("[SV] %0t --> Starting perf test", $time);
        test = new();
        test.run(m_bfm.m_obj);
        $display("[SV] %0t <-- Perf test complete", $time);
        
        $finish;
    end

endmodule
