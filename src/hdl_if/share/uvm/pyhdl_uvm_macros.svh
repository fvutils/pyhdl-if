
`ifndef PYHDL_UVM_MACROS_SVH
`define PYHDL_UVM_MACROS_SVH

`define pyhdl_uvm_type_utils(t, b) \
    class pyhdl_``t``_w extends t``_imp_impl #(pyhdl_``t) implements pyhdl_uvm_object_if; \
    \
        function new(uvm_object obj); \
`ifdef VCS \
            super.new(pyhdl_``t::new(obj)); \
`else \
            pyhdl_``t impl = new(obj); \
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
    static pyhdl_uvm_object_type_rgy __type_``t``_``b`` = pyhdl_uvm_object_type_rgy_p #( \
        t, \
        pyhdl_``t``_w, \
        b, \
        pyhdl_``b``_w)::inst(`"t`", `"b`");


`endif /* PYHDL_UVM_MACROS_SVH */
