typedef class ObjectIF;

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

endclass
