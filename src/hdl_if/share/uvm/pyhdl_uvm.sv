`include "uvm_macros.svh"
`include "pyhdl_uvm_macros.svh"

package pyhdl_uvm;
    import uvm_pkg::*;
    import pyhdl_if::*;

    typedef class pyhdl_uvm_object_type_rgy;
    typedef class pyhdl_uvm_object_type_rgy_p;

    `include "pyhdl_uvm_apis.svh"
    `include "pyhdl_uvm_object_if.svh"

    `include "pyhdl_uvm_analysis_port.svh"
    `include "pyhdl_uvm_object.svh"
    `include "pyhdl_uvm_object_type.svh"
    `include "pyhdl_uvm_cmdline_processor.svh"
    `include "pyhdl_uvm_component.svh"
    `include "pyhdl_uvm_component_proxy.svh"
    `include "pyhdl_uvm_object_rgy.svh"
    `include "pyhdl_uvm_sequence_proxy.svh"
    `include "pyhdl_uvm_phase.svh"
    `include "pyhdl_uvm_reg.svh"
    `include "pyhdl_uvm_reg_block.svh"
    `include "pyhdl_uvm_reg_field.svh"
    `include "pyhdl_uvm_wrapper_factory.svh"
    `include "pyhdl_uvm_pygen.svh"

endpackage
