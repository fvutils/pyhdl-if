/**
 * top_data.sv - Top module for queue_int data test with populated queues
 */

`include "uvm_macros.svh"

module tb_top_data;
  import uvm_pkg::*;
  import pyhdl_uvm::*;
  import pyhdl_if::*;
  import queue_int_data_test_pkg::*;

  initial begin
    // Run the test
    run_test("queue_int_data_test");
  end

endmodule
