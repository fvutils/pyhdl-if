
class create_t;
    CallEmptyBase   first;
    PyObject        second;

    function new(CallEmptyBase first, PyObject second);
        this.first = first;
        this.second = second;
    endfunction
endclass


interface class pyhdl_uvm_wrapper_factory;

    pure virtual function create_t create(
        uvm_object      obj,
        PyObject        obj_t);
endclass

class pyhdl_uvm_wrapper_factory_t #(type WrapperT, type UvmObjT=uvm_object) implements pyhdl_uvm_wrapper_factory;
    static pyhdl_uvm_wrapper_factory_t #(WrapperT, UvmObjT) m_inst;

    virtual function create_t create(uvm_object obj, PyObject obj_t);
        UvmObjT o;
        create_t ret;
        WrapperT wrapper;

        $cast(o, obj);
        wrapper = new(o);

        ret = new(wrapper, wrapper.m_obj);

        if (obj_t != null) begin
            void'(PyObject_SetAttrString(ret.second, "obj_t", obj_t));
        end

        return ret;
    endfunction

    static function pyhdl_uvm_wrapper_factory inst();
        if (m_inst == null) begin
            m_inst = new();
        end
        return m_inst;
    endfunction

endclass


