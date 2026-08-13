
typedef class py_object;

/**
 * Scoped owner for a group of Python object references.
 *
 * Every #py_object holds a reference that must be released, which is easy to
 * leak when a function builds several. Add them to a context instead and
 * release the whole group at once with #dispose.
 *
 * @see py_object
 */
class py_ctxt;
    /// Objects owned by this context, in the order they were added.
    py_object objects[$];

    /**
     * Release every object held by this context.
     *
     * The context may be reused afterwards, but the objects it held must not.
     */
    function void dispose();
        foreach (objects[i]) begin
            objects[i].dispose();
        end
    endfunction

    /**
     * Take ownership of an object.
     *
     * @param obj The object to place under this context's ownership.
     * @return The same object, so the call can wrap an expression:
     *         `py_object o = ctxt.add(py_from_int(4));`
     */
    virtual function py_object add(py_object obj);
        objects.push_back(obj);
        return obj;
    endfunction

endclass
