`include "uvm_macros.svh"

package queue_int_test_pkg;
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // Test object with queue_int fields
  class test_queue_data extends uvm_object;
    int unsigned queue_8bit[$];
    int unsigned queue_16bit[$];
    int queue_signed[$];
    int unsigned scalar_field;

    `uvm_object_utils_begin(test_queue_data)
    `uvm_field_queue_int(queue_8bit, UVM_ALL_ON)
    `uvm_field_queue_int(queue_16bit, UVM_ALL_ON)
    `uvm_field_queue_int(queue_signed, UVM_ALL_ON)
    `uvm_field_int(scalar_field, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="test_queue_data");
        super.new(name);
        scalar_field = 0;
    endfunction

    function void set_queue_8bit(int unsigned values[$]);
        queue_8bit = values;
    endfunction

    function void set_queue_16bit(int unsigned values[$]);
        queue_16bit = values;
    endfunction

    function void set_queue_signed(int values[$]);
        queue_signed = values;
    endfunction

    function int unsigned get_queue_8bit_size();
        return queue_8bit.size();
    endfunction

    function int unsigned get_queue_16bit_size();
        return queue_16bit.size();
    endfunction

    function int unsigned get_queue_signed_size();
        return queue_signed.size();
    endfunction
  endclass

  // Main test class
  class queue_int_test extends uvm_test;
    `uvm_component_utils(queue_int_test)

    pyhdl_uvm_component_proxy       m_proxy;

    function new(string name = "queue_int_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction : new

    function void build_phase(uvm_phase phase);
        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "py_queue_int_test::PyQueueIntTest";
        
        `uvm_info("QUEUE_INT_TEST", "Queue int test setup complete", UVM_LOW)
    endfunction

    virtual task run_phase(uvm_phase phase);
      `uvm_info("QUEUE_INT_TEST", "Running queue int test", UVM_LOW)
    endtask : run_phase

  endclass : queue_int_test

endpackage : queue_int_test_pkg
