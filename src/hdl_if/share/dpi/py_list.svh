
class py_list extends py_object;

    function new(PyObject obj);
        super.new(obj);
    endfunction

    function int size();
        return PyList_Size(obj);
    endfunction

    function void append(py_object obj);
        PyList_Append(this.obj, obj.obj);
    endfunction

    static function py_list mk(py_object obj);
        py_list ret = new(obj.obj);
        return ret;
    endfunction

    static function py_list mk_init(py_object objs[$]);
        py_list ret = new(PyList_New(objs.size()));
        foreach (objs[i]) begin
            PyList_Append(ret.obj, objs[i].obj);
        end
        return ret;
    endfunction

endclass
