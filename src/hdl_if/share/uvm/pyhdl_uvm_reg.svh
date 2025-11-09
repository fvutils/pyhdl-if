
class pyhdl_uvm_reg extends pyhdl_uvm_object;

    function new(uvm_object obj);
        super.new(obj);
    endfunction

    function PyObject get_fields();
        py_list ret = new();
        uvm_reg u_reg;
        uvm_reg_field fields[$];

        $cast(u_reg, m_uvm_obj);
        u_reg.get_fields(fields);

        foreach (fields[i]) begin
            ret.append_obj(pyhdl_uvm_object_rgy::inst().wrap(fields[i]));
        end

        return ret.borrow();
    endfunction

    function void set(longint unsigned value);
        uvm_reg u_reg;
        $cast(u_reg, m_uvm_obj);

        u_reg.set(value);
    endfunction

    function longint unsigned get();
        uvm_reg u_reg;
        $cast(u_reg, m_uvm_obj);

        return u_reg.get();
    endfunction

    task write(
        output bit      retval,
        input longint   value);
        uvm_reg u_reg;
        uvm_status_e status;
        $cast(u_reg, m_uvm_obj);
        u_reg.write(status, value);

        retval = 0;
    endtask

    task read(
        output PyObject retval);
        uvm_reg u_reg;
        uvm_status_e status;
        uvm_reg_data_t value;
        py_tuple ret = py_tuple::mk_new_sz(2);
        $cast(u_reg, m_uvm_obj);
        u_reg.read(status, value);

        ret.set_item(0, py_from_bool(0));
        ret.set_item(1, py_from_ulong(value));

        retval = ret.borrow();
    endtask

    task update(
        output bit      retval);
        uvm_reg u_reg;
        uvm_status_e status;
        $cast(u_reg, m_uvm_obj);
        u_reg.update(status);
        retval = 0;
    endtask

endclass

`pyhdl_uvm_type_utils(uvm_reg, uvm_object)
