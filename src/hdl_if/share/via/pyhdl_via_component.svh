
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

endclass

