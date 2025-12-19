`include "uvm_macros.svh"

package queue_int_data_test_pkg;
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // Test object with queue_int fields and helper methods
  class test_queue_data_with_helpers extends uvm_object;
    int unsigned queue_8bit[$];
    int unsigned queue_16bit[$];
    int queue_signed[$];
    int unsigned scalar_field;

    `uvm_object_utils_begin(test_queue_data_with_helpers)
    `uvm_field_queue_int(queue_8bit, UVM_ALL_ON)
    `uvm_field_queue_int(queue_16bit, UVM_ALL_ON)
    `uvm_field_queue_int(queue_signed, UVM_ALL_ON)
    `uvm_field_int(scalar_field, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="test_queue_data_with_helpers");
        super.new(name);
        scalar_field = 0;
    endfunction

    // Helper to populate with test data
    function void populate_test_data();
        queue_8bit = {8'h12, 8'h34, 8'h56, 8'h78};
        queue_16bit = {16'h100, 16'h200, 16'h300};
        queue_signed = {32'sd127, -32'sd128, 32'sd0, -32'sd1};
        scalar_field = 32'hDEADBEEF;
    endfunction

    // Helper to populate with single element
    function void populate_single();
        queue_8bit = {8'hAA};
        queue_16bit = {16'h5555};
        queue_signed = {32'sd42};
        scalar_field = 32'hCAFE;
    endfunction

    // Helper to populate with many elements
    function void populate_many();
        for (int i = 0; i < 20; i++) begin
            queue_8bit.push_back(i);
        end
        for (int i = 0; i < 10; i++) begin
            queue_16bit.push_back(i * 100);
        end
        for (int i = -5; i < 5; i++) begin
            queue_signed.push_back(i);
        end
        scalar_field = 32'hBEEF;
    endfunction

  endclass

  // Main test class with helper functions callable from Python
  class queue_int_data_test extends uvm_test;
    `uvm_component_utils(queue_int_data_test)

    pyhdl_uvm_component_proxy       m_proxy;
    
    // Store test objects for Python access
    test_queue_data_with_helpers test_obj_1;
    test_queue_data_with_helpers test_obj_2;
    test_queue_data_with_helpers test_obj_3;

    function new(string name = "queue_int_data_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction : new

    function void build_phase(uvm_phase phase);
        // Create test objects and populate them
        test_obj_1 = test_queue_data_with_helpers::type_id::create("test_obj_1");
        test_obj_1.populate_test_data();
        
        test_obj_2 = test_queue_data_with_helpers::type_id::create("test_obj_2");
        test_obj_2.populate_single();
        
        test_obj_3 = test_queue_data_with_helpers::type_id::create("test_obj_3");
        test_obj_3.populate_many();
        
        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "py_queue_int_data_test::PyQueueIntDataTest";
        
        `uvm_info("QUEUE_DATA_TEST", "Queue int data test setup complete", UVM_LOW)
    endfunction

    virtual task run_phase(uvm_phase phase);
      `uvm_info("QUEUE_DATA_TEST", "Running queue int data test", UVM_LOW)
    endtask : run_phase

  endclass : queue_int_data_test

endpackage : queue_int_data_test_pkg
