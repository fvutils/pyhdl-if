`include "uvm_macros.svh"

package object_map_test_pkg;
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // Test objects to store in the map
  class test_config_obj extends uvm_object;
    int cfg_value;
    string cfg_name;

    `uvm_object_utils_begin(test_config_obj)
    `uvm_field_int(cfg_value, UVM_ALL_ON)
    `uvm_field_string(cfg_name, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="test_config_obj");
        super.new(name);
        cfg_value = 0;
        cfg_name = "";
    endfunction

    function void set_config(int v, string s);
        cfg_value = v;
        cfg_name = s;
    endfunction
  endclass

  // Main test class
  class object_map_test extends uvm_test;
    `uvm_component_utils(object_map_test)

    pyhdl_uvm_component_proxy       m_proxy;

    function new(string name = "object_map_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction : new

    function void build_phase(uvm_phase phase);
        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "py_object_map_test::PyObjectMapTest";
        
        `uvm_info("OBJ_MAP_TEST", "Object map test setup complete", UVM_LOW)
    endfunction

    virtual task run_phase(uvm_phase phase);
      `uvm_info("OBJ_MAP_TEST", "Running object map test", UVM_LOW)
    endtask : run_phase

  endclass : object_map_test

endpackage : object_map_test_pkg
