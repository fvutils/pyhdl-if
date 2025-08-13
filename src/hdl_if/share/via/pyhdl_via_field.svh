
typedef class FieldIF;

class pyhdl_via_field extends FieldIF;
    via_field       m_field;

    function new(via_field field);
        m_field = field;
    endfunction

    function string get_name();
        return m_field.get_name();
    endfunction

endclass

