
class py_tuple extends py_object;

    function new(PyObject obj);
        super.new(obj);
    endfunction

    /**
     * Sets the specified tuple element
     */
    function void set_item(int idx, py_object obj);
        void'(PyTuple_SetItem(this.obj, longint'(idx), obj.steal()));
    endfunction

    /**
     * Gets the specified tuple element
     */
    function py_object get_item(int idx);
        py_object ret = new(PyTuple_GetItem(this.obj, longint'(idx)));
        return ret;
    endfunction

    /**
     * Creates a new tuple by wrapping an existing object
     */
    static function py_tuple mk(py_object obj);
        py_tuple ret = new(obj.obj);
        return ret;
    endfunction

    /**
     * Creates a new empty tuple of the specified size
     */
    static function py_tuple mk_new_sz(int sz, py_ctxt ctxt=null);
        PyObject tuple = PyTuple_New(longint'(sz));
        py_tuple ret = new(tuple);

        if (ctxt != null) begin
            void'(ctxt.add(ret));
        end

        return ret;
    endfunction

    /**
     * Creates a new tuple from the specified elements
     */
    static function py_tuple mk_init(py_object elems[$], py_ctxt ctxt=null);
        PyObject tuple = PyTuple_New(longint'(elems.size()));
        py_tuple ret = new(tuple);
        foreach (elems[i]) begin
            PyObject elem = (elems[i] != null)?elems[i].steal():None;
            void'(PyTuple_SetItem(tuple, longint'(i), elem));
        end

        if (ctxt != null) begin
            void'(ctxt.add(ret));
        end

        return ret;
    endfunction

endclass