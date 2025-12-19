/**
 * top.sv - Top module for queue_int test
 */

`include "uvm_macros.svh"

module tb_top;
  import uvm_pkg::*;
  import pyhdl_uvm::*;
  import pyhdl_if::*;
  import queue_int_test_pkg::*;

  initial begin
    // Run the test
    run_test("queue_int_test");
  end

endmodule
