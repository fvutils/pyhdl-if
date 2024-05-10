/**
 * pyhdl_if_call_api.sv
 *
 * Copyright 2024 Matthew Ballance and Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may 
 * not use this file except in compliance with the License.  
 * You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software 
 * distributed under the License is distributed on an "AS IS" BASIS, 
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
 * See the License for the specific language governing permissions and 
 * limitations under the License.
 *
 * Created on:
 *     Author: 
 */

    task automatic pyhdl_if_invokePyTask(
        output PyObject     res,
        input PyObject      obj,
        input string        method,
        input PyObject      args);
        int sem_id = pyhdl_if_allocSem();
        PyObject proxy_h, invoke_py_t, proxy_args;
        PyGILState_STATE state;

        state = PyGILState_Ensure();

        proxy_h = PyObject_GetAttrString(obj, "_proxy");
        invoke_py_t = PyObject_GetAttrString(proxy_h, "invoke_py_t");
        proxy_args = PyTuple_New(3);

        void'(PyTuple_SetItem(proxy_args, 0, PyLong_FromLong(sem_id)));
        void'(PyTuple_SetItem(proxy_args, 1, PyUnicode_FromString(method)));
        void'(PyTuple_SetItem(proxy_args, 2, args));
        
        void'(pyhdl_pi_if_HandleErr(PyObject_Call(invoke_py_t, proxy_args, null)));

        pyhdl_if_waitSem(sem_id, res);

        PyGILState_Release(state);
    endtask

    function automatic PyObject pyhdl_if_invokePyFunc(
        input PyObject      obj,
        input string        method,
        input PyObject      args);
        PyObject res, proxy_h, invoke_py_f, proxy_args;
        PyGILState_STATE state;

        state = PyGILState_Ensure();

        proxy_h = PyObject_GetAttrString(obj, "_proxy");
        invoke_py_f = PyObject_GetAttrString(proxy_h, "invoke_py_f");
        proxy_args = PyTuple_New(2);

        void'(PyTuple_SetItem(proxy_args, 0, PyUnicode_FromString(method)));
        void'(PyTuple_SetItem(proxy_args, 1, args));
        
        res = pyhdl_pi_if_HandleErr(PyObject_Call(invoke_py_f, proxy_args, null));

        PyGILState_Release(state);

        return res;
    endfunction

    function automatic int allocObjId(ICallApi sv_api_if);
        int ret = -1, i;

        for (i=0; i<__objects.size(); i++) begin
            if (__objects[i] == null) begin
                ret = i;
                break;
            end
        end

        if (ret == -1) begin
            __objects = new[__objects.size()+64](__objects);
            ret = i;
        end

        __objects[ret] = sv_api_if;

        return ret;
    endfunction

    function automatic int pyhdl_if_allocSem();
        int ret = -1, i;

        for (i=0; i<__callsem_res.size(); i++) begin
            if (__callsem_res[i] == null) begin
                ret = i;
                break;
            end
        end

        if (ret == -1) begin
            __callsem = new[__callsem.size()+64](__callsem);
            __callsem_res = new[__callsem_res.size()+64](__callsem_res);
            for (int j=i; j<__callsem.size(); j++) begin
                __callsem[j] = new();
            end
            ret = i;
        end

        __callsem_res[ret] = None;

        return ret;
    endfunction

    task automatic pyhdl_if_waitSem(
        input int           id,
        output PyObject     res);
        __callsem[id].get();
        res = __callsem_res[id];
        __callsem[id] = null;
    endtask

    function automatic void pyhdl_if_setSem(
        input int           id,
        input PyObject      res);
        __callsem_res[id] = res;
        __callsem[id].put(1);
    endfunction

    function automatic PyObject pyhdl_if_newObject(
        PyObject        cls_t,
        ICallApi        sv_api_if,
        PyObject        init_args);
        int obj_id;
        PyObject args, ret, new_obj;
        PyGILState_STATE state;

        state = PyGILState_Ensure();

        new_obj = PyObject_GetAttrString(__ep_h, "newObj");
        args = PyTuple_New(3);

        obj_id = (sv_api_if != null)?allocObjId(sv_api_if):-1;

        Py_IncRef(new_obj);

        void'(PyTuple_SetItem(args, 0, cls_t));
        void'(PyTuple_SetItem(args, 1, PyLong_FromLong(obj_id)));
        void'(PyTuple_SetItem(args, 2, init_args));

        ret = pyhdl_pi_if_HandleErr(PyObject_Call(new_obj, args, null));

        Py_DecRef(new_obj);

        PyGILState_Release(state);

        return ret;
    endfunction

    function automatic void pyhdl_if_registerObject(
        PyObject            obj,
        string              inst_path,
        int                 trim_elems=0);
        PyObject args, ret, reg_obj;
        PyGILState_STATE state = PyGILState_Ensure();

        reg_obj = PyObject_GetAttrString(__ep_h, "registerObj");
        args = PyTuple_New(3);

        void'(PyTuple_SetItem(args, 0, obj));
        void'(PyTuple_SetItem(args, 1, PyUnicode_FromString(inst_path)));
        void'(PyTuple_SetItem(args, 2, PyLong_FromLong(trim_elems)));

        ret = pyhdl_pi_if_HandleErr(PyObject_Call(reg_obj, args, null));

        Py_DecRef(reg_obj);

        PyGILState_Release(state);
    endfunction

    function automatic void pyhdl_if_connectObject(
        PyObject        obj,
        ICallApi        sv_api_if);
        int obj_id = (sv_api_if != null)?allocObjId(sv_api_if):-1;
        PyObject args, ret, connect;
        PyGILState_STATE state = PyGILState_Ensure();
        
        connect = PyObject_GetAttrString(__ep_h, "connectObj");
        args = PyTuple_New(2);

        void'(PyTuple_SetItem(args, 0, obj));
        void'(PyTuple_SetItem(args, 1, PyLong_FromLong(obj_id)));
        ret = PyObject_Call(connect, args, null);
        PyGILState_Release(state);
    endfunction
