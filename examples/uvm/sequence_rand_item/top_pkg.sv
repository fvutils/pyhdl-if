`include "uvm_macros.svh"

package top_pkg;
    import uvm_pkg::*;
    import pyhdl_uvm::*;

    // Sequence item with several rand fields
    class seq_item extends uvm_sequence_item;
        rand bit [7:0]   addr;
        rand bit         write; // 1=write, 0=read
        rand bit [31:0]  data;
        rand bit [3:0]   tid;

        // Simple constraints
        constraint addr_c { addr inside {[8'h00:8'hFF]}; }
        constraint data_c { if (write) data != 32'h0; }

        `uvm_object_utils_begin(seq_item)
            `uvm_field_int(addr , UVM_ALL_ON)
            `uvm_field_int(write, UVM_ALL_ON)
            `uvm_field_int(data , UVM_ALL_ON)
            `uvm_field_int(tid  , UVM_ALL_ON)
        `uvm_object_utils_end

        function new(string name = "seq_item");
            super.new(name);
        endfunction
    endclass


    // Basic sequencer
    class my_sequencer extends uvm_sequencer#(seq_item);
        `uvm_component_utils(my_sequencer)
        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction
    endclass

    // Simple driver that consumes items and prints them
    class my_driver extends uvm_driver#(seq_item);
        `uvm_component_utils(my_driver)

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        task run_phase(uvm_phase phase);
            seq_item req;
            forever begin
                seq_item_port.get_next_item(req);
                `uvm_info(get_name(), $sformatf("DRV got item:\n%s", req.sprint()), UVM_MEDIUM)
                seq_item_port.item_done();
            end
        endtask
    endclass

    // Environment with sequencer and driver
    class my_env extends uvm_env;
        `uvm_component_utils(my_env)

        my_sequencer m_seqr;
        my_driver    m_drv;

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            m_seqr = my_sequencer::type_id::create("m_seqr", this);
            m_drv  = my_driver::type_id::create("m_drv", this);
        endfunction

        function void connect_phase(uvm_phase phase);
            super.connect_phase(phase);
            m_drv.seq_item_port.connect(m_seqr.seq_item_export);
        endfunction
    endclass

    // Test that starts the Python sequence on the sequencer
    class base_test extends uvm_test;
        `uvm_component_utils(base_test)

        my_env m_env;

        function new(string name = "base_test", uvm_component parent = null);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            m_env = my_env::type_id::create("m_env", this);
        endfunction

        task run_phase(uvm_phase phase);
            // Python-driven sequence proxy specialized to seq_item
            typedef pyhdl_uvm_sequence_proxy #(
                .REQ(seq_item), .PyClass("pyseq:PyRandSeq")) py_seq_t;
            py_seq_t seq;

            phase.raise_objection(this);
            seq = py_seq_t::type_id::create("seq");
            seq.pyclass = "pyseq::PyRandSeq";
            seq.start(m_env.m_seqr);
            phase.drop_objection(this);
        endtask
    endclass

endpackage
