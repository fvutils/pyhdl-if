// top.sv — simulation top-level module
//
// The only job of this module is to call run_test(), which hands
// control to the UVM test named by +UVM_TESTNAME.
`include "uvm_macros.svh"

module top;
    import uvm_pkg::*;
    import top_pkg::*;

    initial begin
        run_test();
    end

endmodule
