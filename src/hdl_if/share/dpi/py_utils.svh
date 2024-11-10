
/********************************************************************
 * Construction utilities for numeric types
 ********************************************************************/
function automatic py_object py_from_int(int val);
    py_object ret = new(PyLong_FromLong(val));
    return ret;
endfunction

function automatic py_object py_from_uint(int unsigned val);
    py_object ret = new(PyLong_FromUnsignedLong(val));
    return ret;
endfunction

function automatic py_object py_from_long(longint val);
    py_object ret = new(PyLong_FromLongLong(val));
    return ret;
endfunction

function automatic py_object py_from_ulong(longint unsigned val);
    py_object ret = new(PyLong_FromUnsignedLongLong(val));
    return ret;
endfunction

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
