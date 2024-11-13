
class py_dict extends py_object;
    function new (PyObject obj);
        super.new(obj);
    endfunction

    /**
     * Constructs a py_dict wrapper around an existing object
     */
    static function py_dict mk(py_object obj);
        py_dict ret;
        if (obj != null) begin
            ret = new(obj.obj);
        end
        return ret;
    endfunction

    /**
     * Obtains a list of keys
     */
    function py_list keys();
        py_list ret = new(PyDict_Keys(obj));
        return ret;
    endfunction

    // typedef py_object dict_t[string];

    // static function py_dict mk_init(dict_t init);
    //     return null;
    // endfunction

endclass