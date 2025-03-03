
/********************************************************************
 * Construction utilities for numeric types
 ********************************************************************/

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


    $display("--> PyObject_Call");
    $display("func: %0p", func);
    $display("args: %0p", args.obj);
    $display("kwargs: %0p", kwargs.obj);
    ret_o = PyObject_Call(
        func, 
        args.obj, 
        kwargs.obj);
    $display("<-- PyObject_Call");

    $display("ret_o=%0p", ret_o);

    if (ret_o == null) begin
        $display("ret_o is null");
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

