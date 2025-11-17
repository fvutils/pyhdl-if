`include "uvm_macros.svh"

package top_pkg;
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // First sequence item type
  class seq_item_a extends uvm_sequence_item;
    rand bit [7:0] addr;
    rand bit       write;
    rand bit [15:0] data;

    constraint c_addr { addr inside {[0:255]}; }
    constraint c_data { if (write) data != 16'h0; }

    `uvm_object_utils_begin(seq_item_a)
      `uvm_field_int(addr, UVM_ALL_ON)
      `uvm_field_int(write, UVM_ALL_ON)
      `uvm_field_int(data, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="seq_item_a");
      super.new(name);
    endfunction
  endclass

  // Second sequence item type
  class seq_item_b extends uvm_sequence_item;
    rand bit [7:0] id;
    rand bit [31:0] payload;

    constraint c_id { id < 200; }
    constraint c_payload { payload != 32'hDEADBEEF; }

    `uvm_object_utils_begin(seq_item_b)
      `uvm_field_int(id, UVM_ALL_ON)
      `uvm_field_int(payload, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="seq_item_b");
      super.new(name);
    endfunction
  endclass

  // Producer component with two analysis ports
  class dual_producer extends uvm_component;
    `uvm_component_utils(dual_producer)

    pyhdl_uvm_analysis_port #(seq_item_a) ap_a;
    uvm_analysis_port #(seq_item_b) ap_b;

    function new(string name, uvm_component parent);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      ap_a = new("ap_a", this);
      ap_b = new("ap_b", this);
    endfunction

    task run_phase(uvm_phase phase);
      seq_item_a a;
      seq_item_b b;
      // Periodic generation of items
      for (int i=0;i<50;i++) begin
        a = seq_item_a::type_id::create($sformatf("a%0d", i));
        if (!a.randomize()) `uvm_error(get_name(), "Randomize failed for seq_item_a")
        ap_a.write(a);
        #5; // wait between items
        b = seq_item_b::type_id::create($sformatf("b%0d", i));
        if (!b.randomize()) `uvm_error(get_name(), "Randomize failed for seq_item_b")
        ap_b.write(b);
        #5; // wait between items
      end
      `uvm_info(get_name(), "Finished producing items", UVM_LOW)
    endtask
  endclass

  `uvm_analysis_imp_decl(_a)
  `uvm_analysis_imp_decl(_b)

  // Scoreboard with two analysis imps
  class dual_scoreboard extends uvm_component;
    `uvm_component_utils(dual_scoreboard)

    uvm_analysis_imp_a #(seq_item_a, dual_scoreboard) imp_a;
    uvm_analysis_imp_b #(seq_item_b, dual_scoreboard) imp_b;

    int unsigned count_a = 0;
    int unsigned count_b = 0;

    function new(string name, uvm_component parent);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      imp_a = new("imp_a", this);
      imp_b = new("imp_b", this);
    endfunction

    // Overloaded write methods
    function void write_a(seq_item_a t);
      count_a++;
      `uvm_info(get_name(), $sformatf("Got A item %0d: %s", count_a, t.sprint()), UVM_LOW)
    endfunction

    function void write_b(seq_item_b t);
      count_b++;
      `uvm_info(get_name(), $sformatf("Got B item %0d: %s", count_b, t.sprint()), UVM_LOW)
    endfunction

    function void final_phase(uvm_phase phase);
      `uvm_info(get_name(), $sformatf("Final counts: A=%0d B=%0d", count_a, count_b), UVM_MEDIUM)
    endfunction
  endclass

  // Environment tying producer to scoreboard
  class my_env extends uvm_env;
    `uvm_component_utils(my_env)

    dual_producer prod;
    dual_scoreboard sb;

    pyhdl_uvm_analysis_imp #(seq_item_b)    ap_b_proxy;

    pyhdl_uvm_component_proxy   proxy;

    function new(string name, uvm_component parent);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      prod = dual_producer::type_id::create("prod", this);
      sb   = dual_scoreboard::type_id::create("sb", this);
      proxy = pyhdl_uvm_component_proxy::type_id::create("proxy", this);
      proxy.pyclass = "pycomp::PyComp";

      ap_b_proxy = new("a_proxy", this);

    endfunction

    function void connect_phase(uvm_phase phase);
      pyhdl_uvm_subscriber #(seq_item_a) p;
      super.connect_phase(phase);
      prod.ap_a.connect(sb.imp_a);
      prod.ap_b.connect(sb.imp_b);

      prod.ap_b.connect(ap_b_proxy.analysis_export);

    endfunction
  endclass

  // Test
  class base_test extends uvm_test;
    `uvm_component_utils(base_test)

    my_env m_env;

    function new(string name="base_test", uvm_component parent=null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      m_env = my_env::type_id::create("m_env", this);
    endfunction

    task run_phase(uvm_phase phase);
      phase.raise_objection(this);
      // Allow enough time for producer items
      #600; 
      phase.drop_objection(this);
    endtask
  endclass

endpackage
