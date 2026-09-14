

/********************************************************************
 * Construction utilities for numeric types
 ********************************************************************/

/**
 * Creates a Python bool.
 *
 * @param val The value to convert.
 * @return A new reference to Python's `True` or `False`.
 */
function automatic py_object py_from_bool(bit val);
    py_object ret = new(PyBool_FromLong(longint'(val)));
    return ret;
endfunction

/**
 * Create a Python integer-value object
 */
function automatic py_object py_from_int(int val);
    py_object ret = new(PyLong_FromLong(longint'(val)));
    return ret;
endfunction

/**
 * Create a Python unsigned integer-value object
 */
function automatic py_object py_from_uint(int unsigned val);
    py_object ret = new(PyLong_FromUnsignedLong(longint'(val)));
    return ret;
endfunction

/**
 * Create a Python longint-value object
 */
function automatic py_object py_from_long(longint val);
    py_object ret = new(PyLong_FromLongLong(val));
    return ret;
endfunction

/**
 * Create a Python unsigned longint-value object
 */
function automatic py_object py_from_ulong(longint unsigned val);
    py_object ret = new(PyLong_FromUnsignedLongLong(val));
    return ret;
endfunction

/**
 * Create a Python string object
 */
function automatic py_object py_from_str(string str);
    py_object ret = new(PyUnicode_FromString(str));
    return ret;
endfunction

/**
 * Reads a Python string as a SystemVerilog string.
 *
 * @param hndl A Python `str`. Passing any other type is an error CPython
 *        reports on its own.
 * @return The UTF-8 contents. The buffer belongs to @p hndl, so the result is
 *         only valid while that object lives.
 */
function automatic string py_as_str(PyObject hndl);
    string ret = PyUnicode_AsUTF8(hndl);
    return ret;
endfunction

/**
 * Reads a Python integer as a single bit.
 *
 * Tests the value against zero rather than asking Python for its truthiness,
 * so a non-integer does not convert the way `bool(obj)` would.
 *
 * @param hndl A Python integer.
 * @return 0 when the value is zero, 1 otherwise. Prints the exception and
 *         returns 1 if the conversion failed.
 */
function automatic bit py_as_bool(PyObject hndl);
    longint ret = PyLong_AsLong(hndl);

    if (ret == -1 && PyErr_Occurred() != null) begin
        PyErr_Print();
    end

    return (ret != 0);
endfunction

/**
 * Reads a Python integer as a 64-bit signed value.
 *
 * @param hndl A Python integer.
 * @return The value, or -1 if the conversion failed -- which is also a valid
 *         result, so the exception is printed rather than signalled. Values too
 *         large for 64 bits raise `OverflowError`.
 */
function automatic longint py_as_long(PyObject hndl);
    longint ret = PyLong_AsLong(hndl);

    if (ret == -1 && PyErr_Occurred() != null) begin
        PyErr_Print();
    end

    return ret;
endfunction

/**
 * Reads a Python float as a real.
 *
 * @param hndl A Python float, or anything implementing `__float__`.
 * @return The value, or -1.0 if the conversion failed, with the exception
 *         printed.
 */
function automatic real py_as_double(PyObject hndl);
    real ret = 0.0;

    ret = PyFloat_AsDouble(hndl);
    if (ret == -1 && PyErr_Occurred() != null) begin
        $display("Error occurred");
        PyErr_Print();
    end

    return ret;
endfunction


/**
 * Import a module
 */
function automatic py_object py_import(string mod);
    py_object ret = null;
    PyObject imp_o = PyImport_ImportModule(mod);
    if (imp_o == null) begin
        PyErr_Print();
    end else begin
        ret = new(imp_o);
    end
    return ret;
endfunction

/**
 * Call a built-in function
 */
function automatic py_object py_call_builtin(string name, py_tuple args, py_dict kwargs=null);
    PyObject builtins;
    PyObject func;
    PyObject ret_o;
    py_object ret = null;

    `PYHDL_IF_ENTER(("py_call_builtin %0s", name));

    Py_IncRef(args.obj);
    builtins = PyEval_GetBuiltins();
    Py_IncRef(builtins);

    func = PyDict_GetItemString(builtins, name);
    Py_IncRef(func);

    if (func == null) begin
        PyErr_Print();
        return null;
    end

    if (kwargs == null) begin
        kwargs = py_dict::mk_init('{});
    end

    if (args == null) begin
        $display("PyHDL-IF Fatal: args passed to call of %0s is null", name);
        return null;
    end else if (args.obj == null) begin
        $display("PyHDL-IF Fatal: args.obj passed to call of %0s is null", name);
        return null;
    end

    ret_o = PyObject_Call(
        func,
        args.obj,
        kwargs.obj);

    if (ret_o == null) begin
        PyErr_Print();
    end else begin
        ret = new(ret_o);
    end

    `PYHDL_IF_LEAVE(("py_call_builtin %0s", name));

    return ret;
endfunction

int prv_gil_ensure_count = 0;
PyGILState_STATE prv_gil_state;

/**
 * Acquire the GIL
 */
function automatic void py_gil_enter();
    if (prv_gil_ensure_count == 0) begin
        prv_gil_state = PyGILState_Ensure();
    end
    prv_gil_ensure_count++;
endfunction

/**
 * Release the GIL
 */
function automatic void py_gil_leave();
    prv_gil_ensure_count--;
    if (prv_gil_ensure_count == 0) begin
        PyGILState_Release(prv_gil_state);
    end
endfunction

/**
 * Reports a pending Python exception when a wrapper came back null.
 *
 * Wrap a call that returns a #py_object in this to get the traceback printed at
 * the point of failure rather than a null handle surfacing somewhere else.
 *
 * @param obj The object to check.
 * @return @p obj unchanged, or null -- having printed the exception.
 */
function automatic py_object py_check(py_object obj);
    if (obj == null) begin
        $display("Error:");
        PyErr_Print();
        return null; 
    end else begin
        return obj;
    end
endfunction

