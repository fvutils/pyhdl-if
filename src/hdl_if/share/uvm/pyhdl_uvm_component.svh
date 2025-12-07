
typedef class pyhdl_uvm_object_rgy;

class pyhdl_uvm_component extends pyhdl_uvm_object;

    function new(uvm_object comp);
        super.new(comp);
    endfunction

    virtual function PyObject get_parent();
        uvm_component comp;
        $cast(comp, m_uvm_obj);
        return pyhdl_uvm_object_rgy::inst().wrap(comp.get_parent());
    endfunction


    virtual function string get_full_name();
        uvm_component comp;
        $cast(comp, m_uvm_obj);
        return comp.get_full_name();
    endfunction

    virtual function PyObject get_children();
        uvm_component comp;
        py_list ret = new();
        uvm_component c[$];

        $cast(comp, m_uvm_obj);

        comp.get_children(c);
        foreach (c[i]) begin
            ret.append_obj(pyhdl_uvm_object_rgy::inst().wrap(c[i]));
        end

        return ret.borrow();
    endfunction

    virtual function PyObject get_config_object(string name, bit clone=1);
        py_tuple ret;
        uvm_object obj;
        py_object py_obj;
        bit has;
        py_object py_has;
        uvm_component comp;

        $cast(comp, m_uvm_obj);
        has = uvm_config_db #(uvm_object)::get(comp, name, "", obj);

        if (has && obj != null) begin
            py_obj = new(pyhdl_uvm_object_rgy::inst().wrap(obj));
        end

        py_has = py_from_bool(has);

        return py_tuple::mk_init({py_has, py_obj}).borrow();
    endfunction


endclass

`pyhdl_uvm_type_utils(uvm_component, uvm_object)
