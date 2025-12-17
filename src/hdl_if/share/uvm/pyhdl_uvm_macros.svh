
`ifndef PYHDL_UVM_MACROS_SVH
`define PYHDL_UVM_MACROS_SVH

/**
 * Macro to define UVM type wrapper class and register it in the type registry.
 *
 * Parameters:
 * - uvm_t: The UVM type name (e.g., uvm_sequence) being wrapped.
 * - uvm_w_t: The corresponding PyHDL UVM wrapper type name (e.g., pyhdl_uvm_sequence).
 * - base_t: The base UVM type name (e.g., uvm_object).
 * - base_w_t: The corresponding PyHDL UVM base wrapper type name (e.g., pyhdl_uvm_object).
 */
`define pyhdl_uvm_type_utils(uvm_t, uvm_w_t, base_t, base_w_t) \
    class uvm_w_t``_w extends uvm_t``_imp_impl #(uvm_w_t) implements pyhdl_uvm_object_if; \
    \
        function new(uvm_object obj); \
`ifdef VCS \
            super.new(uvm_w_t ::new(obj)); \
`else \
            uvm_w_t impl = new(obj); \
            super.new(impl); \
`endif \
        endfunction \
    \
        virtual function uvm_object get_object(); \
            return m_impl.m_uvm_obj; \
        endfunction \
    \
        virtual function PyObject get_pyobject(); \
            return m_obj; \
        endfunction \
    \
    endclass \
    \
    static pyhdl_uvm_object_type_rgy __type_``uvm_t``_``base_t`` = pyhdl_uvm_object_type_rgy_p #( \
        uvm_t, \
        uvm_w_t``_w, \
        base_t, \
        base_w_t``_w)::inst(`"uvm_t`", `"base_t`");

`endif /* PYHDL_UVM_MACROS_SVH */
