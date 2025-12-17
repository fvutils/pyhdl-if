

class uvm_object_map extends uvm_object;
    `uvm_object_utils(uvm_object_map)
    uvm_object          map[string];

    function new(string name = "uvm_object_map");
      super.new(name);
    endfunction

    function bit has_key(string key);
        return map.exists(key);
    endfunction

    function uvm_object get(string key);
        return map[key];
    endfunction

    function void insert(string key, uvm_object obj);
        map[key] = obj;
    endfunction

endclass

class pyhdl_uvm_object_map extends pyhdl_uvm_object;
    function new(uvm_object obj);
        super.new(obj);
    endfunction

    function bit has_key(string key);
        uvm_object_map map;
        $cast(map, m_uvm_obj);

        return map.has_key(key);
    endfunction

    function PyObject get(string key);
        uvm_object_map map;
        $cast(map, m_uvm_obj);
        return pyhdl_uvm_object_rgy::inst().wrap(map.get(key));
    endfunction

    function void insert(string key, PyObject obj);
        uvm_object_map map;
        uvm_object uvm_obj;
        $cast(map, m_uvm_obj);
        uvm_obj = pyhdl_uvm_object_rgy::inst().get_object(obj);
        map.insert(key, uvm_obj);
    endfunction

endclass

`pyhdl_uvm_type_utils(uvm_object_map, pyhdl_uvm_object_map, uvm_object, pyhdl_uvm_object)

