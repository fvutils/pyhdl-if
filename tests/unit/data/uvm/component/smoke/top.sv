`timescale 1ns/1ps

`include "uvm_macros.svh"

module tb_top;
  // Import UVM and the smoke test package
  import uvm_pkg::*;
  import smoke_pkg::*;

  initial begin
    `uvm_info("TB", "Starting smoke smoke_test", UVM_LOW)
    // Run the registered smoke_test
    run_test("smoke_test");
  end
endmodule : tb_top
