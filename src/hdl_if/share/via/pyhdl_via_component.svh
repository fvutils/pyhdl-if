
typedef class ComponentIF;
typedef class pyhdl_via_object;

class pyhdl_via_component extends ComponentIF;
    via_component_if            m_via_obj;

    function new(via_component_if obj);
        m_via_obj = obj;
    endfunction

    virtual function string get_name();
        return m_via_obj.get_name();
    endfunction

    virtual function string get_full_name();
        return m_via_obj.get_full_name();
    endfunction

    virtual function pyhdl_if::PyObject create_object_by_name(
        string typename,
        string name="");
        via_object_if obj;
        pyhdl_via_object pyobj_if;
        pyhdl_if::py_object pobj = pyhdl_if::py_from_int(20);

        $display("create_object_by_name");
        $display("create_object_by_name");
        $display("create_object_by_name");
        $display("create_object_by_name");
        $display("create_object_by_name");
        $display("m_via_obj: %0p", m_via_obj);
        obj = m_via_obj.create_object_by_name(typename, name);

        pyobj_if = new(obj);

        // 'obj' is a new object
        // - Need to persist as long as we hold a pyref
        // - SV will handle persistence as long as SV holds a ref
        $display("obj: %0p", obj);
        return pyobj_if.m_obj;
    endfunction

endclass

