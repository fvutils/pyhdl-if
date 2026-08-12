
/**
 * Iterates a Python iterable from SystemVerilog.
 *
 * Wraps a Python iterator and presents it as a `valid`/`next` pair, which
 * maps onto a SystemVerilog `while` loop::
 *
 *     py_iter it = new(PyObject_GetIter(seq));
 *     while (it.valid()) begin
 *         py_object item = it.next();
 *         // ...
 *         item.dispose();
 *     end
 *
 * Both methods fetch the next item if one is not already pending, so calling
 * #valid does not consume an element and it is safe to call more than once
 * between #next calls.
 *
 * @see py_object
 */
class py_iter;
    /// The Python iterator being walked.
    PyObject        obj;
    /// The item fetched but not yet returned by #next, or null.
    PyObject        item;

    /**
     * Construct an iterator over a Python iterator object.
     *
     * @param obj A Python iterator, as returned by `PyObject_GetIter`.
     */
    function new(PyObject obj);
        this.obj = obj;
    endfunction

    /**
     * Report whether another item is available.
     *
     * Fetches the next item if one is not already pending, so the iterator
     * does not advance past it -- the pending item is what #next returns.
     *
     * @return 1 if #next will return an object, 0 at the end of iteration.
     */
    function bit valid();
        if (item == null) begin
            item = PyIter_Next(this.obj);
        end
        return (item != null);
    endfunction

    /**
     * Return the next item and advance.
     *
     * @return The next item, or null at the end of iteration. The caller owns
     *         the returned object and must dispose of it, or add it to a
     *         #py_ctxt.
     */
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
