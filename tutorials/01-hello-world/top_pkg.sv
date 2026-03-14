// top_pkg.sv — UVM test package
//
// Defines hello_test, which creates a pyhdl_uvm_component_proxy and
// points it at the Python class HelloComp in hello.py.
`include "uvm_macros.svh"

package top_pkg;
    import uvm_pkg::*;
    import pyhdl_uvm::*;

    class hello_test extends uvm_test;
        `uvm_component_utils(hello_test)

        // The proxy is a standard UVM component.  Set its pyclass field
        // to tell PyHDL-IF which Python class to instantiate.
        pyhdl_uvm_component_proxy m_pycomp;

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            m_pycomp = pyhdl_uvm_component_proxy::type_id::create(
                "m_pycomp", this);
            // Format: "<python_module>::<ClassName>"
            // The module name is the filename without ".py".
            m_pycomp.pyclass = "hello::HelloComp";
        endfunction

        task run_phase(uvm_phase phase);
            // Hold an objection so the simulation stays alive long enough
            // for the Python run_phase coroutine to execute.
            phase.raise_objection(this);
            #1;
            phase.drop_objection(this);
        endtask

    endclass

endpackage
