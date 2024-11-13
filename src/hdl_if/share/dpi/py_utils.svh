
/********************************************************************
 * Construction utilities for numeric types
 ********************************************************************/

/**
 * Create a Python integer-value object
 */
function automatic py_object py_from_int(int val);
    py_object ret = new(PyLong_FromLong(val));
    return ret;
endfunction

/**
 * Create a Python unsigned integer-value object
 */
function automatic py_object py_from_uint(int unsigned val);
    py_object ret = new(PyLong_FromUnsignedLong(val));
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
    PyObject builtins = PyEval_GetBuiltins();
    PyObject func = PyDict_GetItemString(builtins, name);
    PyObject ret_o;
    py_object ret;

    if (func == null) begin
        PyErr_Print();
        return null;
    end

    ret_o = PyObject_Call(func, args.obj, null);

    if (ret_o == null) begin
        PyErr_Print();
    end else begin
        ret = new(ret_o);
    end

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

