
class py_dict extends py_object;
    function new (PyObject obj);
        super.new(obj);
    endfunction

    static function py_dict mk(py_object obj);
        py_dict ret = new(obj.obj);
        return ret;
    endfunction

    typedef py_object dict_t[string];

    static function py_dict mk_init(dict_t init);
        return null;
    endfunction

endclass