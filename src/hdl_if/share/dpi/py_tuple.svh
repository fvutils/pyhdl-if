
class py_tuple extends py_object;

    function new(PyObject obj);
        super.new(obj);
    endfunction

    function void set_item(int idx, py_object obj);
        PyTuple_SetItem(this.obj, idx, obj.obj);
    endfunction

    function py_object get_item(int idx);
        py_object ret = new(PyTuple_GetItem(this.obj, idx));
        return ret;
    endfunction

    static function py_tuple mk(py_object obj);
        py_tuple ret = new(obj.obj);
        return ret;
    endfunction

    static function py_tuple mk_new_sz(int sz);
        PyObject tuple = PyTuple_New(sz);
        py_tuple ret = new(tuple);
        return ret;
    endfunction

    static function py_tuple mk_init(py_object elems[$]);
        PyObject tuple = PyTuple_New(elems.size());
        py_tuple ret = new(tuple);
        foreach (elems[i]) begin
            PyTuple_SetItem(tuple, i, elems[i].obj);
            Py_DecRef(elems[i].obj);
            elems[i].obj = null;
        end
        return ret;
    endfunction

endclass