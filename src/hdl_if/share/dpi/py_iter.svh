
class py_iter;
    PyObject        obj;
    PyObject        item;

    function new(PyObject obj);
        this.obj = obj;
    endfunction

    function bit valid();
        if (item == null) begin
            item = PyIter_Next(this.obj);
        end
        return (item != null);
    endfunction

    function py_object next();
        py_object ret;
        if (item == null) begin
            item = PyIter_Next(this.obj);
        end
        if (item != null) begin
            ret = new(item);
            item = null;
        end
        return ret;
    endfunction

endclass