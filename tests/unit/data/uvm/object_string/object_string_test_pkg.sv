`include "uvm_macros.svh"

package object_string_test_pkg;
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // Main test class
  class object_string_test extends uvm_test;
    `uvm_component_utils(object_string_test)

    pyhdl_uvm_component_proxy       m_proxy;

    function new(string name = "object_string_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction : new

    function void build_phase(uvm_phase phase);
        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "py_object_string_test::PyObjectStringTest";
        
        `uvm_info("OBJ_STRING_TEST", "Object string test setup complete", UVM_LOW)
    endfunction

    virtual task run_phase(uvm_phase phase);
      `uvm_info("OBJ_STRING_TEST", "Running object string test", UVM_LOW)
    endtask : run_phase

  endclass : object_string_test

endpackage : object_string_test_pkg
