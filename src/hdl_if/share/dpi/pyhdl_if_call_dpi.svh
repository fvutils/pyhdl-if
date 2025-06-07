
function PyObject pyhdl_call_if_invoke_hdl_f(
    int             obj_id,
    string          method_name,
    PyObject        args);
    PyObject ret;
    `PYHDL_IF_ENTER(("pyhdl_call_if_invoke_hdl_f(obj_id=%0d, method_name=%s, args=%p)", obj_id, method_name, args));
    ret = __objects[obj_id].invokeFunc(method_name, args);
    `PYHDL_IF_LEAVE(("pyhdl_call_if_invoke_hdl_f"));
    return ret;
endfunction
export "DPI-C" function pyhdl_call_if_invoke_hdl_f;

function void pyhdl_call_if_invoke_hdl_t(
    int             obj_id,
    PyObject        evt_obj,
    PyObject        method_name,
    PyObject        args);
    TaskCallClosure closure;
    automatic string local_name = PyUnicode_AsUTF8(method_name);
    
    closure = new(
        __objects[obj_id],
        evt_obj,
        local_name,
        args);

    pyhdl_pi_if_queue_runnable(closure);
endfunction
export "DPI-C" function pyhdl_call_if_invoke_hdl_t;

function void pyhdl_call_if_response_py_t(
    int             sem_id,
    PyObject        res);
    pyhdl_if_setSem(sem_id, res);
endfunction
export "DPI-C" function pyhdl_call_if_response_py_t;
