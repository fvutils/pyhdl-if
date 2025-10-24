
typedef class FieldIF;

class pyhdl_via_field extends FieldIF;
    via_field       m_field;

    function new(via_field field);
        m_field = field;
    endfunction

    virtual function string get_name();
        return m_field.get_name();
    endfunction

    virtual function int _get_kind();
        return int'(m_field.get_kind());
    endfunction

    virtual function int get_size();
        return m_field.get_size();
    endfunction

    virtual function bit get_signed();
        return m_field.get_signed();
    endfunction

    virtual function pyhdl_if::PyObject get_obj_type();
        // TODO: ??
//        return m_field.get_obj_type();
        return null;
    endfunction

endclass

