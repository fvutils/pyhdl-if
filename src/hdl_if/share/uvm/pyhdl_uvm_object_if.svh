
interface class pyhdl_uvm_object_if;
    pure virtual function uvm_object get_object();
    pure virtual function PyObject get_pyobject();
endclass

