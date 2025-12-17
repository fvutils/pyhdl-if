
`include "uvm_macros.svh"

module tb_top;
  import uvm_pkg::*;
  import object_string_test_pkg::*;

  initial begin
    `uvm_info("TB", "Starting object string test", UVM_LOW)
    run_test("object_string_test");
  end
endmodule : tb_top
