`include "uvm_macros.svh"

package reseed_pkg;
  import uvm_pkg::*;
  import pyhdl_uvm::*;

  // Simple UVM object with one random field
  class reseed_item extends uvm_object;
    rand bit [7:0] v;

    `uvm_object_utils_begin(reseed_item)
      `uvm_field_int(v, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name="reseed_item");
      super.new(name);
    endfunction

    function string convert2string();
      return $sformatf("v=%0d", v);
    endfunction
  endclass

  // Test that triggers Python to exercise reseed() determinism
  class reseed_test extends uvm_test;
    `uvm_component_utils(reseed_test)

    pyhdl_uvm_component_proxy m_proxy;

    function new(string name="reseed_test", uvm_component parent=null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      reseed_item obj = reseed_item::type_id::create("obj");
      // Provide object to Python side via config DB
      set_config_object("*", "MY_CONFIG", obj);

      // Bridge to Python component that will perform reseed/verify
      m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
      m_proxy.pyclass = "pyreseed::PyReseed";
    endfunction
  endclass

endpackage : reseed_pkg
