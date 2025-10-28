
typedef interface class pyhdl_uvm_object_if;

`define pyhdl_uvm_object_methods(uvm_obj) \
    virtual function bit _randomize(); \
        return this.randomize(); \
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
