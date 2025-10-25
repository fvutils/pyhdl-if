
/**
 * Accessor class for UVM objects. Exposes key UVM features to Python
 */
class pyhdl_uvm_object extends UvmObject;
    uvm_object      m_uvm_obj;

    function new(uvm_object obj);
        super.new();
        m_uvm_obj = obj;
    endfunction

    virtual function string get_name();
        return m_uvm_obj.get_name();
    endfunction

    virtual function string sprint();
        return m_uvm_obj.sprint();
    endfunction

endclass
