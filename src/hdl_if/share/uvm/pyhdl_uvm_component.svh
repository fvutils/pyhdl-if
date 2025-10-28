
typedef class pyhdl_uvm_object_rgy;

`define pyhdl_uvm_component_methods(uvm_obj) \
    `pyhdl_uvm_object_methods(uvm_obj) \
    \
    virtual function string get_full_name(); \
        return uvm_obj .get_full_name(); \
    endfunction \
    \
    virtual function PyObject get_children(); \
        py_list ret = new(); \
        uvm_component c[$]; \
        \
        m_comp.get_children(c); \
        foreach (c[i]) begin \
            ret.append_obj(pyhdl_uvm_object_rgy::inst().wrap(c[i])); \
        end \
        \
        return ret.borrow(); \
    endfunction \
    \
    virtual function PyObject get_config_object(string name); \
        py_tuple ret; \
        uvm_object obj; \
        py_object py_obj; \
        bit has = m_comp.get_config_object(name, obj); \
        py_object py_has; \
        \
        $display("has"); \
        \
        if (has && obj != null) begin \
            $display("have object"); \
            py_obj = new(pyhdl_uvm_object_rgy::inst().wrap(obj)); \
        end else begin \
            $display("failed to get object"); \
        end \
        \
        py_has = py_from_bool(has); \
        \
        return py_tuple::mk_init({py_has, py_obj}).borrow(); \
    endfunction \

class pyhdl_uvm_component extends UvmComponent;
    uvm_component       m_comp;

    function new(uvm_component comp);
        super.new();
        m_comp = comp;
    endfunction

    `pyhdl_uvm_component_methods(m_comp)



endclass
