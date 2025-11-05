
typedef interface class pyhdl_uvm_object_if;

/**
 * Accessor class for UVM objects. Exposes key UVM features to Python
 */
class pyhdl_uvm_object implements pyhdl_uvm_object_if;
    uvm_object      m_uvm_obj;

    function new(uvm_object obj);
        m_uvm_obj = obj;
    endfunction

    virtual function bit _randomize();
        return m_uvm_obj .randomize();
    endfunction

    virtual function string get_name();
        return m_uvm_obj .get_name();
    endfunction

    virtual function string sprint();
        return m_uvm_obj .sprint();
    endfunction

    virtual function uvm_object get_object();
        return m_uvm_obj;
    endfunction

    virtual function PyObject pack_ints();
        py_list ret = new();
        int unsigned data[];
        void'(m_uvm_obj .pack_ints(data));
        foreach (data[i]) begin
            ret.append(py_from_int(data[i]));
        end
        return ret.borrow();
    endfunction

    virtual function void unpack_ints(PyObject data);
        py_list dl = new(data);
        int unsigned data_arr[] = new[dl.size()];
        foreach (data_arr[i]) begin
            data_arr[i] = dl.get_item(i).as_int();
        end
        void'(m_uvm_obj .unpack_ints(data_arr));
    endfunction

endclass

class pyhdl_uvm_object_w extends UvmObject_imp_impl #(pyhdl_uvm_object) implements pyhdl_uvm_object_if;

    function new(uvm_object obj);
        super.new(null);
        m_impl = new(obj);
        pyhdl_if_connectObject(m_obj, this);
    endfunction

    virtual function uvm_object get_object();
        return m_impl.m_uvm_obj;
    endfunction

endclass
