`include "uvm_macros.svh"

package top_pkg;
    import uvm_pkg::*;
//    import pyhdl_if::*;
    import pyhdl_if_via::*;
    import via_uvm::*;

    // First transaction type (memory-like)
    class trans_a extends uvm_sequence_item;
        rand bit [31:0] data;
        rand bit [3:0]  addr;
        rand bit        write;

        `uvm_object_utils_begin(trans_a)
            `uvm_field_int(data, UVM_ALL_ON)
            `uvm_field_int(addr, UVM_ALL_ON)
            `uvm_field_int(write, UVM_ALL_ON)
        `uvm_object_utils_end

        function new(string name = "trans_a");
            super.new(name);
        endfunction
    endclass

    // Second transaction type (stream-like)
    class trans_b extends uvm_sequence_item;
        rand bit [15:0] data;
        rand bit        valid;
        bit            ready;

        `uvm_object_utils_begin(trans_b)
            `uvm_field_int(data, UVM_ALL_ON)
            `uvm_field_int(valid, UVM_ALL_ON)
            `uvm_field_int(ready, UVM_ALL_ON)
        `uvm_object_utils_end

        function new(string name = "trans_b");
            super.new(name);
        endfunction
    endclass

    // Sequence: send a single trans_a (transaction is a field)
    class trans_a_single_seq extends uvm_sequence #(trans_a);
        rand trans_a t;
        `uvm_object_utils_begin(trans_a_single_seq)
            `uvm_field_object(t, UVM_ALL_ON)
        `uvm_object_utils_end
        function new(string name = "trans_a_single_seq");
            super.new(name);
            t = trans_a::type_id::create("t");
        endfunction
        virtual task body();
            start_item(t);
            finish_item(t);
        endtask
    endclass

    // Sequence: send N randomized trans_a (N is configurable)
    class trans_a_multi_seq extends uvm_sequence #(trans_a);
        rand int unsigned num_txn;
        `uvm_object_utils_begin(trans_a_multi_seq)
            `uvm_field_int(num_txn, UVM_ALL_ON)
        `uvm_object_utils_end
        function new(string name = "trans_a_multi_seq");
            super.new(name);
            num_txn = 1;
        endfunction
        virtual task body();
            trans_a t;
            for (int i = 0; i < num_txn; i++) begin
                t = trans_a::type_id::create($sformatf("t_%0d", i));
                start_item(t);
                assert(t.randomize());
                finish_item(t);
            end
        endtask
    endclass

    // Sequence: send a single trans_b (transaction is a field)
    class trans_b_single_seq extends uvm_sequence #(trans_b);
        rand trans_b t;
        `uvm_object_utils_begin(trans_b_single_seq)
            `uvm_field_object(t, UVM_ALL_ON)
        `uvm_object_utils_end
        function new(string name = "trans_b_single_seq");
            super.new(name);
            t = trans_b::type_id::create("t");
        endfunction
        virtual task body();
            start_item(t);
            finish_item(t);
        endtask
    endclass

    // Sequence: send N randomized trans_b (N is configurable)
    class trans_b_multi_seq extends uvm_sequence #(trans_b);
        rand int unsigned num_txn;
        `uvm_object_utils_begin(trans_b_multi_seq)
            `uvm_field_int(num_txn, UVM_ALL_ON)
        `uvm_object_utils_end
        function new(string name = "trans_b_multi_seq");
            super.new(name);
            num_txn = 1;
        endfunction
        virtual task body();
            trans_b t;
            for (int i = 0; i < num_txn; i++) begin
                t = trans_b::type_id::create($sformatf("t_%0d", i));
                start_item(t);
                assert(t.randomize());
                finish_item(t);
            end
        endtask
    endclass
 
    // Agent A Driver
    class driver_a extends uvm_driver #(trans_a);
        `uvm_component_utils(driver_a)

        uvm_analysis_port #(trans_a) ap;

        function new(string name, uvm_component parent);
            super.new(name, parent);
            ap = new("ap", this);
        endfunction

        task run_phase(uvm_phase phase);
`ifdef UNDEFINED
            forever begin
                seq_item_port.get_next_item(req);
                ap.write(req);
                // Drive transaction
                @(posedge vif.clk);
                vif.addr <= req.addr;
                vif.data <= req.data;
                vif.write <= req.write;
                seq_item_port.item_done();
            end
`endif // UNDEFINED
        endtask
    endclass

    // Agent B Driver
    class driver_b extends uvm_driver #(trans_b);
        `uvm_component_utils(driver_b)

        uvm_analysis_port #(trans_b) ap;

        function new(string name, uvm_component parent);
            super.new(name, parent);
            ap = new("ap", this);
        endfunction

        task run_phase(uvm_phase phase);
`ifdef UNDEFINED
            forever begin
                seq_item_port.get_next_item(req);
                ap.write(req);
                // Drive transaction
                @(posedge vif.clk);
                vif.data <= req.data;
                vif.valid <= req.valid;
                req.ready = vif.ready;
                seq_item_port.item_done();
            end
`endif
        endtask
    endclass

    // Agent A (Memory-like agent)
    class agent_a extends uvm_agent;
        driver_a    driver;
        uvm_sequencer #(trans_a) sequencer;

        `uvm_component_utils(agent_a)

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            driver = driver_a::type_id::create("driver", this);
            sequencer = uvm_sequencer#(trans_a)::type_id::create("sequencer", this);
        endfunction

        function void connect_phase(uvm_phase phase);
            driver.seq_item_port.connect(sequencer.seq_item_export);
        endfunction
    endclass

    // Agent B (Stream-like agent)
    class agent_b extends uvm_agent;
        driver_b    driver;
        uvm_sequencer #(trans_b) sequencer;

        `uvm_component_utils(agent_b)

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            driver = driver_b::type_id::create("driver", this);
            sequencer = uvm_sequencer#(trans_b)::type_id::create("sequencer", this);
        endfunction

        function void connect_phase(uvm_phase phase);
            driver.seq_item_port.connect(sequencer.seq_item_export);
        endfunction
    endclass

    // Environment
    class test_env extends uvm_env;
        agent_a    agent_mem;
        agent_b    agent_stream;

        `uvm_component_utils(test_env)

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            agent_mem = agent_a::type_id::create("agent_mem", this);
            agent_stream = agent_b::type_id::create("agent_stream", this);
        endfunction
    endclass

    // Test
    class base_test extends uvm_test;
        test_env env;

        `uvm_component_utils(base_test)

        function new(string name = "base_test", uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            $display("--> test build_phase");
            super.build_phase(phase);
            env = test_env::type_id::create("env", this);
            $display("<-- test build_phase");
        endfunction

        task run_phase(uvm_phase phase);
            $display("--> test run_phase");
            phase.raise_objection(this);
            // Test stimulus would go here
            #100;
            phase.drop_objection(this);
            $display("<-- test run_phase");
        endtask
    endclass

endpackage
