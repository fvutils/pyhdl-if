`include "uvm_macros.svh"

package top_pkg;
    import uvm_pkg::*;
    import pyhdl_uvm::*;

    // Test
    class base_test extends uvm_test;

        pyhdl_uvm_component_proxy   m_pycomp;

        `uvm_component_utils(base_test)

        function new(string name = "base_test", uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            m_pycomp = pyhdl_uvm_component_proxy::type_id::create("m_pycomp", this);
            m_pycomp.pyclass = "pycomp::PyComp";
        endfunction

        task run_phase(uvm_phase phase);
            $display("--> test run_phase");
            phase.raise_objection(this);
            // Test stimulus would go here
            #100;
            phase.drop_objection(this);
            $display("<-- test run_phase");
        endtask
    endclass

endpackage
