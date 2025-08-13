
typedef class pyhdl_via_field;
typedef class ObjectTypeIF;

class pyhdl_via_object_type extends ObjectTypeIF;
    via_object_type_if      obj_t;

    function new(via_object_type_if t);
        obj_t = t;
    endfunction

    function string get_name();
        return obj_t.get_name();
    endfunction

    function pyhdl_if::PyObject get_fields();
        pyhdl_if::py_list ret = new();
        via_field fields[$];
        obj_t.get_fields(fields);

        foreach (fields[i]) begin
            pyhdl_via_field field = new(fields[i]);
            ret.append_obj(field.m_obj);
        end

        return ret.borrow();
    endfunction

//    virtual function void 



endclass


