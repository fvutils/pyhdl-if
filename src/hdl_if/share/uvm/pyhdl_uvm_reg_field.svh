
class pyhdl_uvm_reg_field extends pyhdl_uvm_object;

    function new(uvm_object obj);
        super.new(obj);
    endfunction

    function void set(longint unsigned value);
        uvm_reg_field field;
        $cast(field, m_uvm_obj);

        field.set(value);
    endfunction

    function longint unsigned get();
        uvm_reg_field field;
        $cast(field, m_uvm_obj);

        return field.get();
    endfunction

    task write(
        output bit      retval,
        input longint   value);
        retval = 0;
    endtask

    task read(
        output PyObject retval);
    endtask

endclass

`pyhdl_uvm_type_utils(uvm_reg_field, uvm_object)