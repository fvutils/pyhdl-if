
`include "uvm_macros.svh"

module tb_top;
  import uvm_pkg::*;
  import object_list_test_pkg::*;

  initial begin
    `uvm_info("TB", "Starting object list test", UVM_LOW)
    run_test("object_list_test");
  end
endmodule : tb_top
