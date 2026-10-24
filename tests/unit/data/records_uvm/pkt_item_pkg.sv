// Ordinary user UVM code: nothing here knows about Python.
`include "uvm_macros.svh"
package pkt_item_pkg;
  import uvm_pkg::*;

  typedef enum bit [1:0] { K_DATA, K_CTRL, K_ERR } pkt_kind_e;

  class opt_c;
    bit [7:0] code;
    function new(); endfunction
  endclass

  class pkt_item extends uvm_sequence_item;
    `uvm_object_utils(pkt_item)
    rand bit [31:0] src;
    rand bit [31:0] dst;
    rand bit [7:0]  ttl;
    byte            payload[$];
    pkt_kind_e      kind;
    byte unsigned   udata[];
    bit [7:0]       mac[6];
    int             nums[$];
    opt_c           opts[$];

    function new(string name="pkt_item");
      super.new(name);
    endfunction
  endclass

  // What a monitor writes to
  interface class pkt_sink_if;
    pure virtual function void write(pkt_item t);
  endclass
endpackage
