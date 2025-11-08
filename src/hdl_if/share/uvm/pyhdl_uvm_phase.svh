typedef class pyhdl_uvm_object_rgy;

class pyhdl_uvm_phase extends pyhdl_uvm_object;

    function new(uvm_object obj);
        super.new(obj);
    endfunction

    virtual function void raise_objection(input PyObject obj, input int count);
        uvm_phase phase;
        uvm_object o;

        o = pyhdl_uvm_object_rgy::inst().get_object(obj);
        $cast(phase, m_uvm_obj);
        phase.raise_objection(o, "", count);
    endfunction

    virtual function void drop_objection(input PyObject obj, input int count);
        uvm_phase phase;
        uvm_object o;
        o = pyhdl_uvm_object_rgy::inst().get_object(obj);
        $cast(phase, m_uvm_obj);
        phase.drop_objection(o, "", count);

    endfunction
endclass

`pyhdl_uvm_type_utils(uvm_phase, uvm_object)
