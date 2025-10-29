
typedef interface class pyhdl_uvm_object_if;

`define pyhdl_uvm_object_methods(uvm_obj) \
    virtual function bit _randomize(); \
        return uvm_obj .randomize(); \
    endfunction \
    \
    virtual function string get_name(); \
        return uvm_obj .get_name(); \
    endfunction \
    \
    virtual function string sprint(); \
        return uvm_obj .sprint(); \
    endfunction \
    \
    virtual function uvm_object get_object(); \
        return uvm_obj; \
    endfunction \
    \
    virtual function PyObject pack_ints(); \
        py_list ret = new(); \
        int unsigned data[]; \
        void'(uvm_obj .pack_ints(data)); \
        foreach (data[i]) begin \
            ret.append(py_from_int(data[i])); \
        end \
        return ret.borrow(); \
    endfunction \
    \
    virtual function void unpack_ints(PyObject data); \
        py_list dl = new(data); \
        int unsigned data_arr[] = new[dl.size()]; \
        foreach (data_arr[i]) begin \
            data_arr[i] = dl.get_item(i).as_int(); \
        end \
    endfunction


/**
 * Accessor class for UVM objects. Exposes key UVM features to Python
 */
class pyhdl_uvm_object extends UvmObject implements pyhdl_uvm_object_if;
    uvm_object      m_uvm_obj;

    function new(uvm_object obj);
        super.new();
        m_uvm_obj = obj;
    endfunction

    `pyhdl_uvm_object_methods(m_uvm_obj)

endclass
