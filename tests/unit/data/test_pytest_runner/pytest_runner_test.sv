/**
 * pytest_runner_test.sv
 *
 * SystemVerilog testbench for pytest runner
 */

module pytest_runner_test;
    import pyhdl_if::*;

    initial begin
        string testpath;
        
        // Start the PyHDL-IF event loop
        pyhdl_if_start();
        
        $display("=== PyHDL-IF Pytest Runner Test ===");
        
        // Get testpath from environment or use default
        if (!$value$plusargs("testpath=%s", testpath)) begin
            testpath = "tests/unit/data/test_pytest_runner/sample_async_tests.py";
        end
        
        $display("Running pytest with testpath: %s", testpath);
        
        // Run all tests in the file
        pyhdl_pytest(testpath);
        
        $display("=== Test Complete ===");
        
        #1000;
        $finish;
    end

endmodule
