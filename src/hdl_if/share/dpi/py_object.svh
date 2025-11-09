
//typedef class py_str;
typedef class py_dict;
typedef class py_tuple;

/**
 * Convenience wrapper class for PyObject handles
 */
class py_object;
    PyObject            obj;

    function new(PyObject obj);
        this.obj = obj;
    endfunction

    static function py_object mk(PyObject obj);
        py_object ret = new(obj);
        return ret;
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

    /**
     * Calls the object as a Python callable
     */
    virtual function py_object call(py_tuple args=null, py_object kwargs=null);
        PyObject ret_o, kwargs_o;
        py_object ret = null;

        if (kwargs != null) begin
            kwargs_o = kwargs.obj;
        end

        ret_o = PyObject_Call(obj, (args!=null)?args.obj:PyTuple_New(0), kwargs_o);

        if (args != null) begin
            args.dispose();
        end

        if (kwargs != null) begin
            kwargs.dispose();
        end

        if (ret_o == null) begin
            PyErr_Print();
        end else begin
            ret = new(ret_o);
        end
        return ret;
    endfunction

    /**
     * Creates an iterator for the given object
     */
    function py_iter iter();
        PyObject iter_o = PyObject_GetIter(obj);
        py_iter ret;

        if (iter_o == null) begin
            PyErr_Print();
        end else begin
            ret = new(iter_o);
        end
        return ret;
    endfunction

    /**
     * Calls a named attribute of the object as a method
     */
    virtual function py_object call_attr(string name, py_tuple args=null, py_object kwargs=null);
        PyObject attr;
        PyObject ret_o;
        py_object ret = null;
        py_gil_enter();

        attr = PyObject_GetAttrString(obj, name);
        if (attr == null) begin
            PyErr_Print();
            py_gil_leave();
            return null;
        end

        if (args == null) begin
            args = new(PyTuple_New(0));
        end

        if (kwargs == null) begin
            kwargs = py_dict::mk_init('{});
        end

        ret_o = PyObject_Call(attr, args.obj, kwargs.obj);

        if (ret_o == null) begin
            PyErr_Print();
        end else begin
            ret = new(ret_o);
        end

        py_gil_leave();
        return ret;
    endfunction

    /**
     * Returns a borrowed reference to this object
     * (ie just returns the object handle)
     */
    virtual function PyObject borrow();
        return this.obj;
    endfunction

    /**
     * Returns a stolen reference to this object. 
     * Specifically, this method increments the ref count, such
     * that stealing a reference doesn't invalidate this object
     */
    virtual function PyObject steal();
        Py_IncRef(obj);
        return obj;
    endfunction

    /**
     * Obtains the integer value of this object and releases ownership
    */
    virtual function int to_int();
        int ret = int'(PyLong_AsLong(obj));
        return ret;
    endfunction

    /**
     * Obtains the long-int value of this object and releases ownership
     */
    virtual function longint to_long();
        longint ret = PyLong_AsLongLong(obj);
        return ret;
    endfunction

    /**
     * Disposes of the object
     */
    virtual function void to_void();
        Py_DecRef(obj);
        obj = null;
    endfunction

    /**
     * Obtains the string value of the object and disposes of the object
     */
    virtual function string to_str();
        string ret = PyUnicode_AsUTF8(obj);
        return ret;
    endfunction

    /**
     * Obtains the integer value of the object
     */
    function int as_int();
        return int'(PyLong_AsLong(obj));
    endfunction

    /**
     * Obtains the long-int value of the object
     */
    function longint as_long();
        return PyLong_AsLongLong(obj);
    endfunction

    /**
     * Obtains the string value of the object
     */
    virtual function string as_str();
        return PyUnicode_AsUTF8(obj);
    endfunction

endclass
