
class py_list extends py_object;

    function new(PyObject obj=null);
        super.new(obj);
        if (obj == null) begin
            this.obj = PyList_New(longint'(0));
        end
    endfunction

    /**
     * Returns the number of elements in the list
     */
    function int size();
        return int'(PyList_Size(obj));
    endfunction

    /**
     * Gets the item at the specified list index
     */
    function py_object get_item(int idx);
        py_object ret = new(PyList_GetItem(obj, longint'(idx)));
        return ret;
    endfunction

    /**
     * Appends a new element to the list
     */
    function void append(py_object obj);
        void'(PyList_Append(this.obj, obj.steal()));
    endfunction

    function void append_obj(PyObject obj);
        void'(PyList_Append(this.obj, obj));
    endfunction

    /**
     * Creates a new list object that wraps an existing object
     */
    static function py_list mk(py_object obj);
        py_list ret = new(obj.obj);
        return ret;
    endfunction

    /**
     * Creates a new list object from an initial list of items
     */
    static function py_list mk_init(py_object objs[$]);
        py_list ret = new(PyList_New(longint'(objs.size())));
        foreach (objs[i]) begin
            void'(PyList_Append(ret.obj, objs[i].steal()));
        end
        return ret;
    endfunction

endclass
