
class pyhdl_uvm_object_type;
    pyhdl_uvm_object_type       subtypes[$];
    string                      name;

    function new(string name);
        this.name = name;
    endfunction

    virtual function bit issubclass(uvm_object obj);
        return 0;
    endfunction

    virtual function pyhdl_uvm_object_if create(uvm_object obj);
        $display("Fatal: pyhdl_uvm_object_type base::create called", name);
        return null;
    endfunction

    virtual function int subtype_subclasses(ref pyhdl_uvm_object_type types[$], uvm_object obj);
        types = {};
        foreach (subtypes[i]) begin
            $display("%0s: issubclass(%0s)",
                subtypes[i].name,
                obj.get_type_name());
            if (subtypes[i].issubclass(obj)) begin
                $display("issubtype");
                types.push_back(subtypes[i]);
            end
        end
        return types.size();
    endfunction

endclass

class pyhdl_uvm_object_type_p #(type T=uvm_object, type Tw=pyhdl_uvm_object_w) extends pyhdl_uvm_object_type;
    typedef pyhdl_uvm_object_type_p #(T,Tw) this_t;
    static this_t   prv_inst;

    function new(string name);
        super.new(name);
    endfunction

    virtual function bit issubclass(uvm_object obj);
        T test_t;
        return $cast(test_t, obj);
    endfunction

    virtual function pyhdl_uvm_object_if create(uvm_object obj);
        Tw w = new(obj);

        // Create type on first object creation (?)
        return w;
    endfunction

    static function pyhdl_uvm_object_type inst(string name);
        if (prv_inst == null) begin
            prv_inst = new(name);
        end
        return prv_inst;
    endfunction
endclass

