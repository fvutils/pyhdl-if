
typedef class pyhdl_uvm_object_rgy;

class pyhdl_uvm_component extends UvmComponent;
    uvm_component       m_comp;

    function new(uvm_component comp);
        super.new();
        m_comp = comp;
    endfunction

    virtual function string get_name();
        return m_comp.get_name();
    endfunction

    virtual function string get_full_name();
        return m_comp.get_full_name();
    endfunction

    virtual function PyObject get_children();
        py_list ret = new();
        uvm_component c[$];

        m_comp.get_children(c);
        foreach (c[i]) begin
            ret.append_obj(pyhdl_uvm_object_rgy::inst().wrap(c[i]));
        end

        return ret.borrow();
    endfunction

endclass
