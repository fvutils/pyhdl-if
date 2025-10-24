`include "uvm_macros.svh"

import uvm_pkg::*;
import sequence_smoke_pkg::*;

module top;
  initial begin
    // Launch the UVM test that runs the sequence
    run_test("sequence_smoke_test");
  end
endmodule : top
