
typedef class pyhdl_uvm_object;
typedef interface class pyhdl_uvm_wrapper_factory;
typedef class pyhdl_uvm_wrapper_factory_t;
typedef class create_t;

class pyhdl_uvm_object_rgy;
    static pyhdl_uvm_object_rgy    m_inst;
    PyObject                       m_obj_type_factory;
    CallEmptyBase                  m_obj_rgy[PyObject];
    pyhdl_uvm_wrapper_factory      m_type2factory_m[uvm_object_wrapper];
    PyObject                       m_type2type_m[uvm_object_wrapper];

    function new();

    endfunction

    function PyObject wrap(uvm_object obj);
        PyObject ret, obj_t;
        uvm_object_wrapper uvm_obj_t = obj.get_object_type();
        pyhdl_uvm_wrapper_factory factory;
        create_t wrapper;

        if (!m_type2factory_m.exists(uvm_obj_t)) begin
            // Create a new object type
            create_object_type(obj);
        end

        factory = m_type2factory_m[uvm_obj_t];
        obj_t = m_type2type_m[uvm_obj_t];

        wrapper = factory.create(obj, obj_t);

        // Save the wrapper object with the registry to prevent GC
        m_obj_rgy[wrapper.second] = wrapper.first;

        return wrapper.second;
    endfunction

    function void create_object_type(uvm_object obj);
        uvm_component comp;
        uvm_sequence_base seq;
        uvm_sequence_item seq_item;
        uvm_reg_field reg_field;
        pyhdl_uvm_wrapper_factory factory;

        if ($cast(comp, obj)) begin
            $display("component");
            factory = pyhdl_uvm_wrapper_factory_t #(
                pyhdl_uvm_component,
                uvm_component)::inst();
        end else if ($cast(seq, obj)) begin
        end else if ($cast(seq_item, obj)) begin
        end else begin
            // Just a plain object
            factory = pyhdl_uvm_wrapper_factory_t #(
                pyhdl_uvm_object,
                uvm_component)::inst();
        end

        if (factory != null) begin
            uvm_object_wrapper obj_t = obj.get_object_type();

            $display("Register");

            m_type2factory_m[obj_t] = factory;
            m_type2type_m[obj_t] = null;
        end
    endfunction

    function void drop(PyObject obj);

    endfunction

    static function pyhdl_uvm_object_rgy inst();
        if (m_inst == null) begin
            m_inst = new();
        end
        return m_inst;
    endfunction

endclass

