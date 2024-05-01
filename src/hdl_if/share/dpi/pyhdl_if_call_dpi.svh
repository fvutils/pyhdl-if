
function PyObject pyhdl_call_if_invoke_hdl_f(
    int             obj_id,
    string          method_name,
    PyObject        args);
    PyObject ret;
    ret = __objects[obj_id].invokeFunc(method_name, args);
    return ret;
endfunction
export "DPI-C" function pyhdl_call_if_invoke_hdl_f;

function void pyhdl_call_if_invoke_hdl_t(
    int             obj_id,
    PyObject        evt_obj,
    string          method_name,
    PyObject        args);
    TaskCallClosure closure;
    
    closure = new(
        __objects[obj_id],
        evt_obj,
        method_name,
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
