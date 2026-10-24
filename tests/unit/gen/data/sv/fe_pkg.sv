package fe_pkg;
  import uvm_pkg::*;

  typedef enum bit [7:0] { P_ICMP = 1, P_TCP = 6, P_UDP = 17 } proto_e;
  typedef enum int { S_NEG = -1, S_POS = 1 } sign_e;
  typedef byte unsigned bytes_t[$];

  class hdr_c;
    int unsigned src;
    int unsigned dst;
    proto_e proto;
    function new(); endfunction
  endclass

  class base_item extends uvm_sequence_item;
    int unsigned id;
    function new(string name="base_item"); super.new(name); endfunction
  endclass

  class mid_item extends base_item;
    int unsigned mid_only;
    function new(string name="mid_item"); super.new(name); endfunction
  endclass

  class pkt_item extends mid_item;
    rand bit [7:0] ttl;
    rand logic [31:0] addr;
    bit signed [11:0] s12;
    bit [95:0] tag;
    byte data[$];
    byte unsigned udata[];
    bit [7:0] mac[6];
    string names[$];
    int nums[$];
    hdr_c hdrs[$];
    proto_e kind;
    sign_e sgn;
    bit flag;
    real r;
    shortreal sr;
    hdr_c h;
    local int hidden;
    protected int prot;
    static int count;
    const int k = 1;
    function new(string name="pkt_item"); super.new(name); endfunction
  endclass

  interface class cb_if;
    pure virtual function void notify(int v);
  endclass

  interface class base_svc;
    pure virtual function int ping(int v);
  endclass

  interface class pkt_svc extends base_svc;
    pure virtual task send(output int unsigned n, input pkt_item p);
    pure virtual function bytes_t get_bytes(byte unsigned d[$], logic [15:0] w);
    pure virtual function void subscribe(cb_if cb);
    pure virtual function void dispose();
  endclass

  // Unsupported things, for error tests
  class has_event;
    event e;
  endclass
  class has_assoc;
    int a[string];
  endclass
  class needs_args;
    int x;
    function new(int x); this.x = x; endfunction
  endclass
  virtual class abstract_c;
    int x;
  endclass
  interface class bad_dir_if;
    pure virtual function void f(output int x);
  endclass
endpackage
