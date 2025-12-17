
/**
 * pyhdl_uvm_list.svh
 *
 * A simple UVM object class definition for pyhdl UVM list.
 */
class uvm_object_list extends uvm_object;
    `uvm_object_utils(uvm_object_list)
    uvm_object          items[$];

    function new(string name = "pyhdl_uvm_list");
      super.new(name);
    endfunction

    function uvm_object at(int index);
        return items[index];
    endfunction

    function void push_back(uvm_object obj);
        items.push_back(obj);
    endfunction

endclass

class pyhdl_uvm_object_list extends pyhdl_uvm_object;
    function new(uvm_object obj);
        super.new(obj);
    endfunction

    function PyObject at(int index);
        uvm_object_list list;
        $cast(list, m_uvm_obj);
        return pyhdl_uvm_object_rgy::inst().wrap(list.at(index));
    endfunction

    function void push_back(PyObject obj);
        uvm_object_list list;
        uvm_object uvm_obj;
        $cast(list, m_uvm_obj);
        uvm_obj = pyhdl_uvm_object_rgy::inst().get_object(obj);
        list.push_back(uvm_obj);
    endfunction

endclass

`pyhdl_uvm_type_utils(uvm_object_list, pyhdl_uvm_object_list, uvm_object, pyhdl_uvm_object)