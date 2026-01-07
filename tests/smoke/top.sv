
module top;
    import pyhdl_if::*;

    initial begin
        $display("=== PyHDL-IF Smoke Test ===");
        
        // Start the PyHDL-IF event loop
        pyhdl_if_start();
        
        $display("PyHDL-IF started successfully");
        
        // Simple test - just verify startup works
        #100ns;
        
        $display("=== Smoke Test Complete ===");
        $finish;
    end

endmodule
