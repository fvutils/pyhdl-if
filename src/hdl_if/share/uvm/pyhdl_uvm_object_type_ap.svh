
class pyhdl_uvm_object_type_ap #(type T) extends pyhdl_uvm_object_type;
    typedef pyhdl_uvm_type_info_ap #(T) this_t;
    static this_t prv_inst;

    function new(string name);
        super.new(name);
    endfunction

    virtual function bit issubclass(uvm_object obj);
        uvm_analysis_port #(T) test_t;
        return $cast(test_t, obj);
    endfunction

    static function pyhdl_uvm_object_type inst(string name);
        if (prv_inst == null) begin
            prv_inst = new(name);
        end
    endfunction


endclass
