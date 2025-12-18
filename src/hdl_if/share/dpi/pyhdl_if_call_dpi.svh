
function PyObject pyhdl_call_if_invoke_hdl_f(
    int             obj_id,
    string          method_name,
    PyObject        args);
    PyObject ret;
    `PYHDL_IF_ENTER(("pyhdl_call_if_invoke_hdl_f(obj_id=%0d, method_name=%0s)", obj_id, method_name));
    if (__objects.size() > obj_id && __objects[obj_id] != null) begin
        ret = __objects[obj_id].invokeFunc(method_name, args);
    end else begin
        $display("Fatal: obj_id %0d doesn't exist", obj_id);
    end
    /*if (PyErr_Occurred() != null) begin
        PyErr_Print();
        ret = null;
    end else*/ if (ret == null) begin
        ret = pyhdl_if::None;
    end
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
    `PYHDL_IF_ENTER(("pyhdl_call_if_invoke_hdl_t(obj_id=%0d, method_name=%0s)", obj_id, local_name));

    // Note: py2sv_active is incremented when the closure actually runs,
    // not when it's queued. This ensures accurate tracking for thread support.

    closure = new(
        __objects[obj_id],
        evt_obj,
        local_name,
        args);

    pyhdl_pi_if_queue_runnable(closure);
    `PYHDL_IF_LEAVE(("pyhdl_call_if_invoke_hdl_t(obj_id=%0d, method_name=%0s)", obj_id, local_name));
endfunction
export "DPI-C" function pyhdl_call_if_invoke_hdl_t;

function void pyhdl_call_if_response_py_t(
    int             sem_id,
    PyObject        res);
    `PYHDL_IF_ENTER(("pyhdl_call_if_response_py_t(sem_id=%0d)", sem_id));
    pyhdl_if_setSem(sem_id, res);
    `PYHDL_IF_LEAVE(("pyhdl_call_if_response_py_t(sem_id=%0d)", sem_id));
endfunction
export "DPI-C" function pyhdl_call_if_response_py_t;
