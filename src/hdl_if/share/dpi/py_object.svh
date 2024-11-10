
//typedef class py_str;
typedef class py_tuple;

/**
 * Convenience wrapper class for PyObject handles
 */
class py_object;
    PyObject            obj;

    function new(PyObject obj);
        this.obj = obj;
    endfunction

    /**
     * Drops ownership of handle
     */
    virtual function void dispose();
        Py_DecRef(obj);
        obj = null;
    endfunction

    /**
     * Returns the named Python attribute as a py_object
     */
    virtual function py_object get_attr(string name);
        PyObject ret_o = PyObject_GetAttrString(obj, name);
        py_object ret = null;

        if (ret_o == null) begin
            PyErr_Print();
        end else begin
            ret = new(ret_o);
        end

        return ret;
    endfunction

    // TODO: add in kwargs
    /**
     * Calls the object as a Python callable
     */
    virtual function py_object call(py_tuple args=null, py_object kwargs=null);
        PyObject ret_o = PyObject_Call(obj, (args!=null)?args.obj:PyTuple_New(0), (kwargs!=null)?kwargs.obj:PyObject'(null));
        py_object ret = null;

        if (args != null) begin
            args.dispose();
        end

        if (ret_o == null) begin
            PyErr_Print();
        end else begin
            ret = new(ret_o);
        end
        return ret;
    endfunction

    virtual function int to_int();
        int ret = PyLong_AsLong(obj);
        Py_DecRef(obj);
        obj = null;
        return ret;
    endfunction

    virtual function longint to_long();
        longint ret = PyLong_AsLongLong(obj);
        Py_DecRef(obj);
        obj = null;
        return ret;
    endfunction

    virtual function void to_void();
        Py_DecRef(obj);
        obj = null;
    endfunction

    function int as_int();
        return PyLong_AsLong(obj);
    endfunction

    function longint as_long();
        return PyLong_AsLongLong(obj);
    endfunction

endclass
