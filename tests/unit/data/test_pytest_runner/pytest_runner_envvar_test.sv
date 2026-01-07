/**
 * Test environment variable expansion in pyhdl_pytest
 */
module pytest_runner_envvar_test;
    import pyhdl_if::*;

    initial begin
        pyhdl_if_start();
        
        $display("=== PyHDL-IF Pytest Runner Test ===");
        $display("Testing environment variable expansion");
        $display("Set TEST_ROOT environment variable to the test directory");
        
        // This should expand ${TEST_ROOT} to the actual path
        pyhdl_pytest("${TEST_ROOT}/sample_async_tests.py");
        
        $display("=== Test Complete ===");
        $finish;
    end

endmodule
