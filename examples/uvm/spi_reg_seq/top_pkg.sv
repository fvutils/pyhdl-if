`include "uvm_macros.svh"

package top_pkg;
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // --------------------------------------------
  // Simple bus transaction used by adapter/driver
  // --------------------------------------------
  class seq_item extends uvm_sequence_item;
    rand bit [7:0]   addr;
    rand bit         write; // 1=write, 0=read
    rand bit [31:0]  data;
    rand bit [3:0]   tid;

    constraint addr_c { addr inside {[8'h00:8'hFF]}; }

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

  // --------------------------------------------
  // Sequencer and Driver (emulated memory backend)
  // --------------------------------------------
  class my_sequencer extends uvm_sequencer#(seq_item);
    `uvm_component_utils(my_sequencer)
    function new(string name, uvm_component parent);
      super.new(name, parent);
    endfunction
  endclass

  class my_driver extends uvm_driver#(seq_item);
    `uvm_component_utils(my_driver)

    // Simple register-storage emulation by address
    bit [31:0] mem [bit[7:0]];

    function new(string name, uvm_component parent);
      super.new(name, parent);
    endfunction

    task run_phase(uvm_phase phase);
      seq_item req;
      forever begin
        seq_item_port.get_next_item(req);
        if (req.write) begin
          mem[req.addr] = req.data;
          `uvm_info(get_name(), $sformatf("WRITE @0x%02h = 0x%08h", req.addr, req.data), UVM_MEDIUM)
          #1ns;
          seq_item_port.item_done();
          $display("-- post-item_done");
        end
        else begin
          seq_item rsp = seq_item::type_id::create("rsp");
          bit [31:0] r = (mem.exists(req.addr)) ? mem[req.addr] : '0;
          `uvm_info(get_name(), $sformatf("READ  @0x%02h -> 0x%08h", req.addr, r), UVM_MEDIUM)

          // Return response with read data back to sequencer
          rsp.copy(req);
          rsp.data = r;
          rsp.set_id_info(req);
          seq_item_port.item_done(rsp);
        end
      end
    endtask
  endclass

  // --------------------------------------------
  // UVM RAL bus adapter
  // --------------------------------------------
  class spi_reg_adapter extends uvm_reg_adapter;
    `uvm_object_utils(spi_reg_adapter)

    function new(string name="spi_reg_adapter");
      super.new(name);
      supports_byte_enable = 0;
      provides_responses   = 0; // reads return a response
    endfunction

    virtual function uvm_sequence_item reg2bus(const ref uvm_reg_bus_op rw);
      seq_item t = seq_item::type_id::create("t");
      t.addr  = rw.addr[7:0];
      t.write = (rw.kind == UVM_WRITE);
      t.data  = rw.data;
      return t;
    endfunction

    virtual function void bus2reg(uvm_sequence_item bus_item, ref uvm_reg_bus_op rw);
      seq_item t;
      if (!$cast(t, bus_item)) begin
        rw.status = UVM_NOT_OK;
        return;
      end
      rw.kind   = t.write ? UVM_WRITE : UVM_READ;
      rw.addr   = t.addr;
      rw.data   = t.data;
      rw.status = UVM_IS_OK;
    endfunction
  endclass

  // --------------------------------------------
  // Register definitions
  // --------------------------------------------
  typedef class reg_CTRL;
  typedef class reg_STATUS;
  typedef class reg_CLKDIV;
  typedef class reg_SS;
  typedef class reg_TXDATA;
  typedef class reg_RXDATA;

  class reg_CTRL extends uvm_reg;
    uvm_reg_field enable, master, cpol, cpha, lsb_first, rsvd;
    `uvm_object_utils(reg_CTRL)
    function new(string name="CTRL"); super.new(name, 32, UVM_NO_COVERAGE); endfunction
    virtual function void build();
      enable    = uvm_reg_field::type_id::create("enable");
      master    = uvm_reg_field::type_id::create("master");
      cpol      = uvm_reg_field::type_id::create("cpol");
      cpha      = uvm_reg_field::type_id::create("cpha");
      lsb_first = uvm_reg_field::type_id::create("lsb_first");
      rsvd      = uvm_reg_field::type_id::create("rsvd");

      enable   .configure(this, 1 , 0 , "RW", 0, 0, 1, 0, 0);
      master   .configure(this, 1 , 1 , "RW", 0, 0, 1, 0, 0);
      cpol     .configure(this, 1 , 2 , "RW", 0, 0, 1, 0, 0);
      cpha     .configure(this, 1 , 3 , "RW", 0, 0, 1, 0, 0);
      lsb_first.configure(this, 1 , 4 , "RW", 0, 0, 1, 0, 0);
      rsvd     .configure(this, 27, 5 , "RO", 0, 0, 0, 0, 0);
    endfunction
  endclass

  class reg_STATUS extends uvm_reg;
    uvm_reg_field busy, tx_empty, rx_full, rsvd;
    `uvm_object_utils(reg_STATUS)
    function new(string name="STATUS"); super.new(name, 32, UVM_NO_COVERAGE); endfunction
    virtual function void build();
      busy     = uvm_reg_field::type_id::create("busy");
      tx_empty = uvm_reg_field::type_id::create("tx_empty");
      rx_full  = uvm_reg_field::type_id::create("rx_full");
      rsvd     = uvm_reg_field::type_id::create("rsvd");

      busy    .configure(this, 1 , 0, "RO", 0, 0, 0, 0, 0);
      tx_empty.configure(this, 1 , 1, "RO", 0, 0, 0, 0, 0);
      rx_full .configure(this, 1 , 2, "RO", 0, 0, 0, 0, 0);
      rsvd    .configure(this, 29, 3, "RO", 0, 0, 0, 0, 0);
    endfunction
  endclass

  class reg_CLKDIV extends uvm_reg;
    uvm_reg_field div, rsvd;
    `uvm_object_utils(reg_CLKDIV)
    function new(string name="CLKDIV"); super.new(name, 32, UVM_NO_COVERAGE); endfunction
    virtual function void build();
      div  = uvm_reg_field::type_id::create("div");
      rsvd = uvm_reg_field::type_id::create("rsvd");

      div .configure(this, 16, 0 , "RW", 0, 0, 1, 0, 0);
      rsvd.configure(this, 16, 16, "RO", 0, 0, 0, 0, 0);
    endfunction
  endclass

  class reg_SS extends uvm_reg;
    uvm_reg_field ss_mask, rsvd;
    `uvm_object_utils(reg_SS)
    function new(string name="SS"); super.new(name, 32, UVM_NO_COVERAGE); endfunction
    virtual function void build();
      ss_mask = uvm_reg_field::type_id::create("ss_mask");
      rsvd    = uvm_reg_field::type_id::create("rsvd");

      ss_mask.configure(this, 4 , 0 , "RW", 0, 0, 1, 0, 0);
      rsvd   .configure(this, 28, 4 , "RO", 0, 0, 0, 0, 0);
    endfunction
  endclass

  class reg_TXDATA extends uvm_reg;
    uvm_reg_field data, rsvd;
    `uvm_object_utils(reg_TXDATA)
    function new(string name="TXDATA"); super.new(name, 32, UVM_NO_COVERAGE); endfunction
    virtual function void build();
      data = uvm_reg_field::type_id::create("data");
      rsvd = uvm_reg_field::type_id::create("rsvd");

      data.configure(this, 8 , 0 , "WO", 0, 0, 1, 0, 0);
      rsvd.configure(this, 24, 8 , "RO", 0, 0, 0, 0, 0);
    endfunction
  endclass

  class reg_RXDATA extends uvm_reg;
    uvm_reg_field data, rsvd;
    `uvm_object_utils(reg_RXDATA)
    function new(string name="RXDATA"); super.new(name, 32, UVM_NO_COVERAGE); endfunction
    virtual function void build();
      data = uvm_reg_field::type_id::create("data");
      rsvd = uvm_reg_field::type_id::create("rsvd");

      data.configure(this, 8 , 0 , "RO", 0, 0, 0, 0, 0);
      rsvd.configure(this, 24, 8 , "RO", 0, 0, 0, 0, 0);
    endfunction
  endclass

  // --------------------------------------------
  // Register block with address map (stride 4)
  // --------------------------------------------
  class spi_reg_block extends uvm_reg_block;
    `uvm_object_utils(spi_reg_block)

    rand reg_CTRL   CTRL;
    rand reg_STATUS STATUS;
    rand reg_CLKDIV CLKDIV;
    rand reg_SS     SS;
    rand reg_TXDATA TXDATA;
    rand reg_RXDATA RXDATA;

    uvm_reg_map default_map;

    function new(string name="spi_reg_block");
      super.new(name, UVM_NO_COVERAGE);
    endfunction

    virtual function void build();
      default_map = create_map("map", 'h0, 4, UVM_LITTLE_ENDIAN);

      CTRL   = reg_CTRL  ::type_id::create("CTRL");
      STATUS = reg_STATUS::type_id::create("STATUS");
      CLKDIV = reg_CLKDIV::type_id::create("CLKDIV");
      SS     = reg_SS    ::type_id::create("SS");
      TXDATA = reg_TXDATA::type_id::create("TXDATA");
      RXDATA = reg_RXDATA::type_id::create("RXDATA");

      CTRL  .configure(this, null, "");
      STATUS.configure(this, null, "");
      CLKDIV.configure(this, null, "");
      SS    .configure(this, null, "");
      TXDATA.configure(this, null, "");
      RXDATA.configure(this, null, "");

      CTRL  .build();
      STATUS.build();
      CLKDIV.build();
      SS    .build();
      TXDATA.build();
      RXDATA.build();

      default_map.add_reg(CTRL  , 'h00, "RW");
      default_map.add_reg(STATUS, 'h04, "RO");
      default_map.add_reg(CLKDIV, 'h08, "RW");
      default_map.add_reg(SS    , 'h0C, "RW");
      default_map.add_reg(TXDATA, 'h10, "WO");
      default_map.add_reg(RXDATA, 'h14, "RO");
    endfunction
  endclass

  // --------------------------------------------
  // Environment tying RAL to the bus agent
  // --------------------------------------------
  class my_env extends uvm_env;
    `uvm_component_utils(my_env)

    my_sequencer    m_seqr;
    my_driver       m_drv;

    spi_reg_block   m_reg;
    spi_reg_adapter m_adapter;

    function new(string name, uvm_component parent);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      m_seqr   = my_sequencer ::type_id::create("m_seqr", this);
      m_drv    = my_driver    ::type_id::create("m_drv" , this);

      m_reg    = spi_reg_block::type_id::create("m_reg");
      m_reg.build();
      m_reg.lock_model();

      m_adapter = spi_reg_adapter::type_id::create("m_adapter");
      m_reg.default_map.set_sequencer(m_seqr, m_adapter);
      m_reg.default_map.set_auto_predict(1); // predict on writes
    endfunction

    function void connect_phase(uvm_phase phase);
      super.connect_phase(phase);
      m_drv.seq_item_port.connect(m_seqr.seq_item_export);
    endfunction
  endclass

  // --------------------------------------------
  // Simple RAL exercise sequence
  // --------------------------------------------
  class ral_smoke_seq extends uvm_sequence#(uvm_sequence_item);
    `uvm_object_utils(ral_smoke_seq)

    my_env m_env;

    function new(string name="ral_smoke_seq");
      super.new(name);
    endfunction

    task body();
      uvm_status_e   status;
      uvm_reg_data_t rd;

      if (m_env == null) begin
        uvm_component c = uvm_top.find("uvm_test_top.m_env");
        if (!$cast(m_env, c)) begin
          `uvm_fatal(get_name(), "Failed to find environment")
        end
      end

      // Program CTRL / CLKDIV / SS
      m_env.m_reg.CTRL.enable.write(status, 1);
      m_env.m_reg.CTRL.master.write(status, 1);
      m_env.m_reg.CLKDIV.div.write(status, 16'h0004);
      m_env.m_reg.SS.ss_mask.write(status, 4'h1);

      // Frontdoor write TXDATA
      m_env.m_reg.TXDATA.write(status, 32'h000000A5);

      // Frontdoor reads (driver supplies data from emulated memory)
      m_env.m_reg.STATUS.read(status, rd);
      `uvm_info(get_name(), $sformatf("STATUS = 0x%08h", rd), UVM_LOW)

      m_env.m_reg.CTRL.read(status, rd);
      `uvm_info(get_name(), $sformatf("CTRL   = 0x%08h", rd), UVM_LOW)
    endtask
  endclass

  // --------------------------------------------
  // Test
  // --------------------------------------------
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
      // Optional: Python-driven bus traffic for parity with other examples
      typedef pyhdl_uvm_sequence_proxy #(
        .REQ(seq_item), .PyClass("pyseq:PyRegSeq")) py_seq_t;
      py_seq_t pyseq;
      ral_smoke_seq seq;

      phase.raise_objection(this);

      pyseq = py_seq_t::type_id::create("pyseq");
      pyseq.pyclass = "pyseq::PyRegSeq";
      m_env.m_seqr.set_config_object("", "spi_regs", m_env.m_reg, 0);
      pyseq.start(m_env.m_seqr);

    //   // Exercise the RAL model
    //   $display("--> Running built-in seq");
    //   seq = ral_smoke_seq::type_id::create("seq");
    //   seq.m_env = m_env;
    //   seq.start(null);
    //   $display("<-- Running built-in seq");

      phase.drop_objection(this);
    endtask
  endclass

endpackage
