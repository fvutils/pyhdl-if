`include "uvm_macros.svh"

package smoke_pkg;
  // Minimal UVM smoke test package for unit tests
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // Simple UVM test class
  class smoke_test extends uvm_test;
    `uvm_component_utils(smoke_test)

    pyhdl_uvm_component_proxy       m_proxy;

    // Constructor
    function new(string name = "smoke_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction : new

    function void build_phase(uvm_phase phase);
        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "pycomp::PyComp";
    endfunction

    // Run phase - do nothing more than print an info message
    virtual task run_phase(uvm_phase phase);
      `uvm_info("SMOKE", "Running smoke_test (no DUT) .", UVM_LOW)
    endtask : run_phase

  endclass : smoke_test

endpackage : smoke_pkg
