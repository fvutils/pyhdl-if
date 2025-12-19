
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

/**
 * Macro to register an enum type with the enum registry.
 * This macro introspects the enum type and registers all enumerator names and values.
 *
 * Parameters:
 * - enum_t: The enum type name
 *
 * Usage example:
 *   typedef enum {RED, GREEN, BLUE} color_e;
 *   `pyhdl_uvm_enum_utils(color_e)
 */
`define pyhdl_uvm_enum_utils(enum_t) \
    class pyhdl_enum_``enum_t``_rgy; \
        static bit __registered = register_enum(); \
        \
        static function bit register_enum(); \
            pyhdl_uvm_enum_info info; \
            enum_t e; \
            string enum_str; \
            \
            info = new(`"enum_t`"); \
            \
            e = e.first(); \
            do begin \
                enum_str = e.name(); \
                info.add_enumerator(enum_str, int'(e)); \
                if (e == e.last()) break; \
                e = e.next(); \
            end while (1); \
            \
            pyhdl_uvm_enum_rgy::inst().register_enum(`"enum_t`", info); \
            return 1; \
        endfunction \
    endclass \
    \
    bit __pyhdl_enum_``enum_t``_registered = pyhdl_enum_``enum_t``_rgy::__registered;

`endif /* PYHDL_UVM_MACROS_SVH */
