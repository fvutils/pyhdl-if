`include "uvm_macros.svh"

package object_registry_smoke_pkg;
  // UVM Object Registry smoke test package
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // Create some test objects to populate the factory
  class test_obj_1 extends uvm_object;
    int value1;

    `uvm_object_utils_begin(test_obj_1)
    `uvm_field_int(value1, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="test_obj_1");
        super.new(name);
        value1 = 42;
    endfunction
  endclass

  class test_obj_2 extends uvm_object;
    string name_str;

    `uvm_object_utils_begin(test_obj_2)
    `uvm_field_string(name_str, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="test_obj_2");
        super.new(name);
        name_str = "test_object_2";
    endfunction
  endclass

  class custom_component extends uvm_component;
    `uvm_component_utils(custom_component)

    function new(string name = "custom_component", uvm_component parent = null);
      super.new(name, parent);
    endfunction : new

    virtual function void build_phase(uvm_phase phase);
      `uvm_info("CUSTOM_COMP", "Custom component build phase", UVM_LOW)
    endfunction
  endclass

  // Main test class that exercises the object registry
  class object_registry_smoke_test extends uvm_test;
    `uvm_component_utils(object_registry_smoke_test)

    pyhdl_uvm_component_proxy       m_proxy;
    custom_component                m_custom_comp;

    // Constructor
    function new(string name = "object_registry_smoke_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction : new

    function void build_phase(uvm_phase phase);
        // Create some objects to ensure they're registered in the factory
        test_obj_1 obj1 = test_obj_1::type_id::create();
        test_obj_2 obj2 = test_obj_2::type_id::create();
        
        // Create custom component
        m_custom_comp = custom_component::type_id::create("m_custom_comp", this);

        // Create the Python proxy component that will test the object registry
        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "pyobj_rgy::PyObjRgyTest";
        
        `uvm_info("OBJ_RGY_TEST", "Object registry smoke test setup complete", UVM_LOW)
    endfunction

    // Run phase - let the proxy component do the work
    virtual task run_phase(uvm_phase phase);
      `uvm_info("OBJ_RGY_TEST", "Running object registry smoke test", UVM_LOW)
      
    endtask : run_phase

  endclass : object_registry_smoke_test

endpackage : object_registry_smoke_pkg
