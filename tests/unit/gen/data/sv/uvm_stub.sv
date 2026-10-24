// Just enough of uvm_pkg for front-end tests
package uvm_pkg;
  virtual class uvm_void;
  endclass
  virtual class uvm_object extends uvm_void;
    string m_name;
    int m_inst_id;
    function new(string name="");
      m_name = name;
    endfunction
  endclass
  virtual class uvm_transaction extends uvm_object;
    int m_transaction_id;
    function new(string name="");
      super.new(name);
    endfunction
  endclass
  virtual class uvm_sequence_item extends uvm_transaction;
    int m_sequence_id;
    function new(string name="uvm_sequence_item");
      super.new(name);
    endfunction
  endclass
endpackage
