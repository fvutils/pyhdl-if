
`include "uvm_macros.svh"

module tb_top;
  import uvm_pkg::*;
  import object_map_test_pkg::*;

  initial begin
    `uvm_info("TB", "Starting object map test", UVM_LOW)
    run_test("object_map_test");
  end
endmodule : tb_top
