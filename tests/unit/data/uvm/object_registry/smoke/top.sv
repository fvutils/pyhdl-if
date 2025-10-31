`timescale 1ns/1ps

`include "uvm_macros.svh"

module tb_top;
  // Import UVM and the object registry smoke test package
  import uvm_pkg::*;
  import object_registry_smoke_pkg::*;

  initial begin
    `uvm_info("TB", "Starting object registry smoke test", UVM_LOW)
    // Run the registered object_registry_smoke_test
    run_test("object_registry_smoke_test");
  end
endmodule : tb_top
