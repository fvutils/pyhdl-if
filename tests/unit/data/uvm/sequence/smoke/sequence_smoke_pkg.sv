`include "uvm_macros.svh"

package sequence_smoke_pkg;
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // Sequence item
  class seq_item extends uvm_sequence_item;
    rand bit [7:0] data;

    `uvm_object_utils(seq_item)

    function new(string name = "seq_item");
      super.new(name);
    endfunction

    function string convert2string();
      return $sformatf("data=%0d", data);
    endfunction
  endclass : seq_item

  // Sequencer typedef
  typedef uvm_sequencer#(seq_item) seqr_t;

  // Sequence
  class seq extends uvm_sequence#(seq_item);
    `uvm_object_utils(seq)

    function new(string name = "seq");
      super.new(name);
    endfunction

    virtual task body();
      seq_item req;
      int i;
      for (i = 0; i < 5; i = i + 1) begin
        req = seq_item::type_id::create($sformatf("req_%0d", i));
        assert(req.randomize());
        `uvm_info("SEQ", $sformatf("Starting item %0d: %s", i, req.convert2string()), UVM_LOW)
        start_item(req);
        finish_item(req);
      end
    endtask
  endclass : seq

  // Driver
  class sequence_driver extends uvm_driver#(seq_item);
    `uvm_component_utils(sequence_driver)

    function new(string name = "sequence_driver", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    virtual task run_phase(uvm_phase phase);
      seq_item req;
      forever begin
        seq_item_port.get_next_item(req);
        `uvm_info("DRV", $sformatf("Driver got item: %s", req.convert2string()), UVM_LOW)
        // Simulate some driving work
        #1ns;
        seq_item_port.item_done();
      end
    endtask
  endclass : sequence_driver

  // Environment
  class sequence_env extends uvm_env;
    `uvm_component_utils(sequence_env)

    seqr_t seqr;
    sequence_driver drv;

    function new(string name = "sequence_env", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      seqr = seqr_t::type_id::create("seqr", this);
      drv  = sequence_driver::type_id::create("drv", this);
    endfunction

    virtual function void connect_phase(uvm_phase phase);
      super.connect_phase(phase);
      drv.seq_item_port.connect(seqr.seq_item_export);
    endfunction
  endclass : sequence_env

  // Test
  class sequence_smoke_test extends uvm_test;
    `uvm_component_utils(sequence_smoke_test)

    sequence_env env;

    function new(string name = "sequence_smoke_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      env = sequence_env::type_id::create("env", this);
    endfunction

    virtual task run_phase(uvm_phase phase);
      typedef pyhdl_uvm_sequence_proxy #(.REQ(seq_item), .PyClass("pyseq::PySeq")) seq_t;
      seq_t s;

      phase.raise_objection(this);

      s = seq_t::type_id::create("s");
      s.start(env.seqr);

      // wait a bit for the sequence to run
      #10ns;
      phase.drop_objection(this);
    endtask
  endclass : sequence_smoke_test

endpackage : sequence_smoke_pkg
