typedef class ObjectIF;
typedef class pyhdl_via_object_type;

/**
 * pyhdl_via_object is a wrapper for the via type. It connects 
 * the SV APIs to the pyhdl-if Python APIs
 */
class pyhdl_via_object extends ObjectIF;
    via_object_if m_via_obj;

    function new(via_object_if obj);
        m_via_obj = obj;
    endfunction

    virtual function string get_name();
        return m_via_obj.get_name();
    endfunction

    virtual function pyhdl_if::PyObject get_object_type();
        via_object_type_if t = m_via_obj.get_object_type();
        pyhdl_via_object_type t_w = new(t);
        return t_w.m_obj;
    endfunction

endclass
