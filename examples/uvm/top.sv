`include "uvm_macros.svh"

module top;
  import uvm_pkg::*;
  import top_pkg::*;

  initial begin
//    uvm_root root = uvm_root::get();
//    $display("root: %0p", root);
    run_test();
  end

endmodule


