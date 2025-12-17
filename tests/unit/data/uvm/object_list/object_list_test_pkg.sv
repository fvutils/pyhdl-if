`include "uvm_macros.svh"

package object_list_test_pkg;
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // Test objects to store in the list
  class test_data_obj extends uvm_object;
    int value;
    string name_str;

    `uvm_object_utils_begin(test_data_obj)
    `uvm_field_int(value, UVM_ALL_ON)
    `uvm_field_string(name_str, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="test_data_obj");
        super.new(name);
        value = 0;
        name_str = "";
    endfunction

    function void set_values(int v, string s);
        value = v;
        name_str = s;
    endfunction
  endclass

  // Main test class
  class object_list_test extends uvm_test;
    `uvm_component_utils(object_list_test)

    pyhdl_uvm_component_proxy       m_proxy;

    function new(string name = "object_list_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction : new

    function void build_phase(uvm_phase phase);
        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "py_object_list_test::PyObjectListTest";
        
        `uvm_info("OBJ_LIST_TEST", "Object list test setup complete", UVM_LOW)
    endfunction

    virtual task run_phase(uvm_phase phase);
      `uvm_info("OBJ_LIST_TEST", "Running object list test", UVM_LOW)
    endtask : run_phase

  endclass : object_list_test

endpackage : object_list_test_pkg
