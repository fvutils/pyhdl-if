
typedef class pyhdl_uvm_object;
typedef interface class pyhdl_uvm_object_if;
typedef interface class pyhdl_uvm_wrapper_factory;
typedef class pyhdl_uvm_wrapper_factory_t;
typedef class create_t;

/**
 * Implements a report catcher to allow capturing the 
 * list of object typenames printed by the factory
 */
class factory_print_catcher extends uvm_report_catcher;
    string  factory_print;

    function new(string name="factory_print_catcher");
        super.new(name);
    endfunction

    function action_e catch();
        factory_print = get_message();

        // Suppress the message
        return CAUGHT;
    endfunction
endclass

class pyhdl_uvm_object_rgy extends UvmObjectRgy;
    static pyhdl_uvm_object_rgy    m_inst;
    pyhdl_uvm_object_if            m_obj_rgy[PyObject];
    pyhdl_uvm_wrapper_factory      m_type2factory_m[uvm_object_wrapper];
    PyObject                       m_type2type_m[uvm_object_wrapper];

    function new();
        super.new();
    endfunction

    function PyObject wrap(uvm_object obj);
        PyObject ret, obj_t;
        uvm_object_wrapper uvm_obj_t = obj.get_object_type();
        pyhdl_uvm_wrapper_factory factory;
        pyhdl_uvm_object_if obj_if;
        create_t wrapper;

        if (!m_type2factory_m.exists(uvm_obj_t)) begin
            // Create a new object type
            wrapper = create_object_type(obj);
        end else begin
            factory = m_type2factory_m[uvm_obj_t];
            obj_t = m_type2type_m[uvm_obj_t];

            wrapper = factory.create(obj, obj_t);
        end

        if (wrapper == null) begin
            $display("Fatal: failed to create a wrapper for UVM object %0s",
                obj.get_name());
        end

        if ($cast(obj_if, wrapper.first)) begin
            // Save the wrapper object with the registry to prevent GC
            m_obj_rgy[wrapper.second] = obj_if;
        end else begin
            $display("Fatal: Failed to cast to object_if");
        end

        return wrapper.second;
    endfunction

    function uvm_object get_object(PyObject obj);
        uvm_object ret;
        if (m_obj_rgy.exists(obj)) begin
            pyhdl_uvm_object_if obj_if = m_obj_rgy[obj];
            ret = obj_if.get_object();
        end else begin
            $display("Fatal: Object is not registered");
        end
        return ret;
    endfunction

    function create_t create_object_type(uvm_object obj);
        uvm_component comp;
        uvm_sequence_base seq;
        uvm_sequence_item seq_item;
        uvm_reg_field reg_field;
        pyhdl_uvm_wrapper_factory factory;
        py_object py_obj_t;
        create_t ret;

        py_gil_enter();

        if ($cast(comp, obj)) begin
            $display("component");
            factory = pyhdl_uvm_wrapper_factory_t #(
                pyhdl_uvm_component,
                uvm_component)::inst();
        end else if ($cast(seq, obj)) begin
        end else if ($cast(seq_item, obj)) begin
            // For now, just a plain object
            factory = pyhdl_uvm_wrapper_factory_t #(
                pyhdl_uvm_object,
                uvm_object)::inst();
        end else begin
            // Just a plain object
            factory = pyhdl_uvm_wrapper_factory_t #(
                pyhdl_uvm_object,
                uvm_object)::inst();
        end

        if (factory != null) begin
            uvm_object_wrapper obj_t = obj.get_object_type();

            $display("Register");
//            ret = new();

            m_type2factory_m[obj_t] = factory;

            ret = factory.create(obj, null);

            py_obj_t = py_object::mk(mk(ret.second));

            void'(PyObject_SetAttrString(ret.second, "obj_t", py_obj_t.borrow()));

            py_gil_leave();

            m_type2type_m[obj_t] = null;
        end else begin
            $display("Fatal: no factory found for object %0s", obj.get_name());
        end

        return ret;
    endfunction

    function void drop(PyObject obj);

    endfunction

    virtual function string _get_type_dump();
        factory_print_catcher catcher = new;
        uvm_factory factory = uvm_factory::get();

        // Attach our custom report catcher so we can 
        // save the message printed by factory.print()
        uvm_report_cb::add(null, catcher);

        $display("--> print");
        factory.print();
        $display("<-- print\n%0s", catcher.factory_print);

        uvm_report_cb::delete(null, catcher);

        return catcher.factory_print;
    endfunction

    static function pyhdl_uvm_object_rgy inst();
        if (m_inst == null) begin
            m_inst = new();
        end
        return m_inst;
    endfunction

endclass

