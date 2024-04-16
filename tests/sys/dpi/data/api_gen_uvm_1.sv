`include "uvm_macros.svh"

package api_pkg;
    import uvm_pkg::*;
    import pyhdl_dpi_if::*;
    import pyhdl_call_if::*;

    `include "api_gen_uvm_1.svh"

endpackage

module api_gen_uvm_1;
    import uvm_pkg::*;
    import api_pkg::*;

    class MyCls extends MyC #(.CREATE(0));
        `uvm_object_utils(MyCls)

        function new(string name="MyCls");
            super.new(name);
        endfunction

        function void startup();
            m_obj = create_pyobj();
            init(m_obj);
        endfunction

    endclass

    initial begin
        automatic MyCls c = new();
        c.startup();
        $display("val: %0d", c.get_py_val(20));
        $finish;
    end

endmodule
