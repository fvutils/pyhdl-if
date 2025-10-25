`include "uvm_macros.svh"

package smoke_pkg;
  // Minimal UVM smoke test package for unit tests
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  class my_obj extends uvm_object;
    int a;
    int b;

    `uvm_object_utils_begin(my_obj)
    `uvm_field_int(a, UVM_ALL_ON)
    `uvm_field_int(b, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="my_obj");
        super.new(name);
    endfunction

  endclass

  // Simple UVM test class
  class smoke_test extends uvm_test;
    `uvm_component_utils(smoke_test)

    pyhdl_uvm_component_proxy       m_proxy;

    // Constructor
    function new(string name = "smoke_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction : new

    function void build_phase(uvm_phase phase);
        my_obj obj = my_obj::type_id::create();

        set_config_object("*", "MY_CONFIG", obj);

        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "pycomp::PyComp";
    endfunction

    // Run phase - do nothing more than print an info message
    virtual task run_phase(uvm_phase phase);
      `uvm_info("SMOKE", "Running smoke_test (no DUT) .", UVM_LOW)
    endtask : run_phase

  endclass : smoke_test

endpackage : smoke_pkg
