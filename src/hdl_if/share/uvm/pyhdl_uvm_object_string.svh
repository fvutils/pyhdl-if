
/**
 * pyhdl_uvm_object_string.svh
 *
 * A simple UVM object class that wraps a string value.
 */
class uvm_object_string extends uvm_object;
    `uvm_object_utils(uvm_object_string)
    string          value;

    function new(string name = "uvm_object_string");
      super.new(name);
      value = "";
    endfunction

    function string get_value();
        return value;
    endfunction

    function void set_value(string val);
        value = val;
    endfunction

    static function uvm_object_string mk(string val);
        uvm_object_string ret = uvm_object_string::type_id::create();
        ret.set_value(val);
        return ret;
    endfunction

endclass

class pyhdl_uvm_object_string extends pyhdl_uvm_object;
    function new(uvm_object obj);
        super.new(obj);
    endfunction

    function string get_value();
        uvm_object_string str_obj;
        $cast(str_obj, m_uvm_obj);
        return str_obj.get_value();
    endfunction

    function void set_value(string val);
        uvm_object_string str_obj;
        $cast(str_obj, m_uvm_obj);
        str_obj.set_value(val);
    endfunction

endclass

`pyhdl_uvm_type_utils(uvm_object_string, pyhdl_uvm_object_string, uvm_object, pyhdl_uvm_object)
