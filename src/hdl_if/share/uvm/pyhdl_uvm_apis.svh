virtual class UvmCmdlineProcessor #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_cmdline_processor", string clsname="UvmCmdlineProcessor");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmCmdlineProcessor");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    virtual function pyhdl_if::PyObject _get_plusargs();
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "_get_plusargs": begin
                pyhdl_if::PyObject __rval;
                __rval = _get_plusargs();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

virtual class UvmCmdlineProcessor_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new(pyhdl_if::PyObject obj=null);
        if (obj != null) begin
            init(obj);
        end
    endfunction

    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_cmdline_processor", string clsname="UvmCmdlineProcessor");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmCmdlineProcessor");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject _get_plusargs();
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "_get_plusargs": begin
                pyhdl_if::PyObject __rval;
                __rval = _get_plusargs();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

interface class UvmCmdlineProcessor_exp_if;
endclass

interface class UvmCmdlineProcessor_imp_if;
    pure virtual function pyhdl_if::PyObject _get_plusargs();
endclass

class UvmCmdlineProcessor_exp_impl implements UvmCmdlineProcessor_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmCmdlineProcessor");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_cmdline_processor", string clsname="UvmCmdlineProcessor");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmCmdlineProcessor");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction



    function void callpy();
        // Prepares arguments and calls Python object
    endfunction
endclass

class UvmCmdlineProcessor_imp_impl #(type ImpT=UvmCmdlineProcessor_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmCmdlineProcessor");
        m_impl = impl;
        if (obj == null && create) begin
            // Create an instance of the Python class
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
        if (m_obj != null && m_impl != null) begin
            pyhdl_if::pyhdl_if_connectObject(m_obj, this);
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_cmdline_processor", string clsname="UvmCmdlineProcessor");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmCmdlineProcessor");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "_get_plusargs": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl._get_plusargs();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    virtual task invokeTask(
        output pyhdl_if::PyObject retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string method,
        input pyhdl_if::PyObject args);
        retval = pyhdl_if::None;
        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask
endclass

virtual class UvmObject #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_object", string clsname="UvmObject");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmObject");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    virtual function bit _randomize();
    endfunction

    virtual function string get_name();
    endfunction

    virtual function string sprint();
    endfunction

    virtual function pyhdl_if::PyObject pack_ints();
    endfunction

    virtual function void unpack_ints(input pyhdl_if::PyObject data);
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "_randomize": begin
                bit __rval;
                __rval = _randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "pack_ints": begin
                pyhdl_if::PyObject __rval;
                __rval = pack_ints();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "unpack_ints": begin
                pyhdl_if::PyObject __data = (pyhdl_if::PyTuple_GetItem(args, 0));
                unpack_ints(__data);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

virtual class UvmObject_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new(pyhdl_if::PyObject obj=null);
        if (obj != null) begin
            init(obj);
        end
    endfunction

    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_object", string clsname="UvmObject");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmObject");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function bit _randomize();
    endfunction

    virtual function string get_name();
    endfunction

    virtual function string sprint();
    endfunction

    virtual function pyhdl_if::PyObject pack_ints();
    endfunction

    virtual function void unpack_ints(input pyhdl_if::PyObject data);
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "_randomize": begin
                bit __rval;
                __rval = _randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "pack_ints": begin
                pyhdl_if::PyObject __rval;
                __rval = pack_ints();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "unpack_ints": begin
                pyhdl_if::PyObject __data = (pyhdl_if::PyTuple_GetItem(args, 0));
                unpack_ints(__data);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

interface class UvmObject_exp_if;
endclass

interface class UvmObject_imp_if;
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function string sprint();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class UvmObject_exp_impl implements UvmObject_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmObject");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_object", string clsname="UvmObject");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmObject");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction



    function void callpy();
        // Prepares arguments and calls Python object
    endfunction
endclass

class UvmObject_imp_impl #(type ImpT=UvmObject_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmObject");
        m_impl = impl;
        if (obj == null && create) begin
            // Create an instance of the Python class
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
        if (m_obj != null && m_impl != null) begin
            pyhdl_if::pyhdl_if_connectObject(m_obj, this);
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_object", string clsname="UvmObject");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmObject");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "_randomize": begin
                bit __rval;
                __rval = m_impl._randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get_name": begin
                string __rval;
                __rval = m_impl.get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "pack_ints": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.pack_ints();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "unpack_ints": begin
                pyhdl_if::PyObject __data = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.unpack_ints(__data);
                __ret = pyhdl_if::None;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    virtual task invokeTask(
        output pyhdl_if::PyObject retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string method,
        input pyhdl_if::PyObject args);
        retval = pyhdl_if::None;
        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask
endclass

virtual class UvmComponent #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_component", string clsname="UvmComponent");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmComponent");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    virtual function string get_full_name();
    endfunction

    virtual function pyhdl_if::PyObject get_parent();
    endfunction

    virtual function pyhdl_if::PyObject get_children();
    endfunction

    virtual function pyhdl_if::PyObject get_config_object(
        input string name,
        input bit clone
    );

    endfunction

    virtual function bit _randomize();
    endfunction

    virtual function string get_name();
    endfunction

    virtual function string sprint();
    endfunction

    virtual function pyhdl_if::PyObject pack_ints();
    endfunction

    virtual function void unpack_ints(input pyhdl_if::PyObject data);
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "get_full_name": begin
                string __rval;
                __rval = get_full_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_parent": begin
                pyhdl_if::PyObject __rval;
                __rval = get_parent();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_children": begin
                pyhdl_if::PyObject __rval;
                __rval = get_children();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                bit __clone = pyhdl_if::py_as_bool(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = get_config_object(
                    __name,
                    __clone);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "_randomize": begin
                bit __rval;
                __rval = _randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "pack_ints": begin
                pyhdl_if::PyObject __rval;
                __rval = pack_ints();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "unpack_ints": begin
                pyhdl_if::PyObject __data = (pyhdl_if::PyTuple_GetItem(args, 0));
                unpack_ints(__data);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

virtual class UvmComponent_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new(pyhdl_if::PyObject obj=null);
        if (obj != null) begin
            init(obj);
        end
    endfunction

    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_component", string clsname="UvmComponent");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmComponent");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function string get_full_name();
    endfunction

    virtual function pyhdl_if::PyObject get_parent();
    endfunction

    virtual function pyhdl_if::PyObject get_children();
    endfunction

    virtual function pyhdl_if::PyObject get_config_object(
        input string name,
        input bit clone
    );

    endfunction

    virtual function bit _randomize();
    endfunction

    virtual function string get_name();
    endfunction

    virtual function string sprint();
    endfunction

    virtual function pyhdl_if::PyObject pack_ints();
    endfunction

    virtual function void unpack_ints(input pyhdl_if::PyObject data);
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "get_full_name": begin
                string __rval;
                __rval = get_full_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_parent": begin
                pyhdl_if::PyObject __rval;
                __rval = get_parent();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_children": begin
                pyhdl_if::PyObject __rval;
                __rval = get_children();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                bit __clone = pyhdl_if::py_as_bool(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = get_config_object(
                    __name,
                    __clone);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "_randomize": begin
                bit __rval;
                __rval = _randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "pack_ints": begin
                pyhdl_if::PyObject __rval;
                __rval = pack_ints();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "unpack_ints": begin
                pyhdl_if::PyObject __data = (pyhdl_if::PyTuple_GetItem(args, 0));
                unpack_ints(__data);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

interface class UvmComponent_exp_if;
endclass

interface class UvmComponent_imp_if;
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject get_parent();
    pure virtual function pyhdl_if::PyObject get_children();
    pure virtual function pyhdl_if::PyObject get_config_object(
        input string name,
        input bit clone
    );

    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function string sprint();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class UvmComponent_exp_impl implements UvmComponent_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmComponent");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_component", string clsname="UvmComponent");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmComponent");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction



    function void callpy();
        // Prepares arguments and calls Python object
    endfunction
endclass

class UvmComponent_imp_impl #(type ImpT=UvmComponent_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmComponent");
        m_impl = impl;
        if (obj == null && create) begin
            // Create an instance of the Python class
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
        if (m_obj != null && m_impl != null) begin
            pyhdl_if::pyhdl_if_connectObject(m_obj, this);
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_component", string clsname="UvmComponent");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmComponent");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_parent": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_parent();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_children": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_children();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                bit __clone = pyhdl_if::py_as_bool(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.get_config_object(
                    __name,
                    __clone);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "_randomize": begin
                bit __rval;
                __rval = m_impl._randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get_name": begin
                string __rval;
                __rval = m_impl.get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "pack_ints": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.pack_ints();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "unpack_ints": begin
                pyhdl_if::PyObject __data = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.unpack_ints(__data);
                __ret = pyhdl_if::None;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    virtual task invokeTask(
        output pyhdl_if::PyObject retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string method,
        input pyhdl_if::PyObject args);
        retval = pyhdl_if::None;
        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask
endclass

virtual class UvmFactory #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_factory", string clsname="UvmFactory");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmFactory");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    virtual function pyhdl_if::PyObject typenames();
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "typenames": begin
                pyhdl_if::PyObject __rval;
                __rval = typenames();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

virtual class UvmFactory_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new(pyhdl_if::PyObject obj=null);
        if (obj != null) begin
            init(obj);
        end
    endfunction

    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_factory", string clsname="UvmFactory");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmFactory");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject typenames();
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "typenames": begin
                pyhdl_if::PyObject __rval;
                __rval = typenames();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

interface class UvmFactory_exp_if;
endclass

interface class UvmFactory_imp_if;
    pure virtual function pyhdl_if::PyObject typenames();
endclass

class UvmFactory_exp_impl implements UvmFactory_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmFactory");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_factory", string clsname="UvmFactory");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmFactory");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction



    function void callpy();
        // Prepares arguments and calls Python object
    endfunction
endclass

class UvmFactory_imp_impl #(type ImpT=UvmFactory_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmFactory");
        m_impl = impl;
        if (obj == null && create) begin
            // Create an instance of the Python class
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
        if (m_obj != null && m_impl != null) begin
            pyhdl_if::pyhdl_if_connectObject(m_obj, this);
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_factory", string clsname="UvmFactory");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmFactory");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "typenames": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.typenames();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    virtual task invokeTask(
        output pyhdl_if::PyObject retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string method,
        input pyhdl_if::PyObject args);
        retval = pyhdl_if::None;
        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask
endclass

virtual class UvmComponentProxy #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_component_proxy", string clsname="UvmComponentProxy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmComponentProxy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    virtual function void build_phase(input pyhdl_if::PyObject phase);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (phase==null)?pyhdl_if::None:phase));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "build_phase", __args);
        pyhdl_if::Py_DecRef(__res);
        pyhdl_if::PyGILState_Release(state);
    endfunction

    virtual function void connect_phase(input pyhdl_if::PyObject phase);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (phase==null)?pyhdl_if::None:phase));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "connect_phase", __args);
        pyhdl_if::Py_DecRef(__res);
        pyhdl_if::PyGILState_Release(state);
    endfunction

    virtual task run_phase(input pyhdl_if::PyObject phase);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (phase==null)?pyhdl_if::None:phase));
        pyhdl_if::pyhdl_if_invokePyTask(__res, m_obj, "run_phase", __args);
        pyhdl_if::PyGILState_Release(state);
    endtask

    virtual function pyhdl_if::PyObject get_factory();
    endfunction

    virtual function pyhdl_if::PyObject get_config_object(
        input string name,
        input bit clone
    );

    endfunction

    virtual function void info(input string msg);
    endfunction

    virtual function string get_full_name();
    endfunction

    virtual function pyhdl_if::PyObject get_parent();
    endfunction

    virtual function pyhdl_if::PyObject get_children();
    endfunction

    virtual function bit _randomize();
    endfunction

    virtual function string get_name();
    endfunction

    virtual function string sprint();
    endfunction

    virtual function pyhdl_if::PyObject pack_ints();
    endfunction

    virtual function void unpack_ints(input pyhdl_if::PyObject data);
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "get_factory": begin
                pyhdl_if::PyObject __rval;
                __rval = get_factory();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                bit __clone = pyhdl_if::py_as_bool(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = get_config_object(
                    __name,
                    __clone);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "info": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                info(__msg);
            end
            "get_full_name": begin
                string __rval;
                __rval = get_full_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_parent": begin
                pyhdl_if::PyObject __rval;
                __rval = get_parent();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_children": begin
                pyhdl_if::PyObject __rval;
                __rval = get_children();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "_randomize": begin
                bit __rval;
                __rval = _randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "pack_ints": begin
                pyhdl_if::PyObject __rval;
                __rval = pack_ints();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "unpack_ints": begin
                pyhdl_if::PyObject __data = (pyhdl_if::PyTuple_GetItem(args, 0));
                unpack_ints(__data);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

virtual class UvmComponentProxy_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new(pyhdl_if::PyObject obj=null);
        if (obj != null) begin
            init(obj);
        end
    endfunction

    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_component_proxy", string clsname="UvmComponentProxy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmComponentProxy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function void build_phase(input pyhdl_if::PyObject phase);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (phase==null)?pyhdl_if::None:phase));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "build_phase", __args);
        pyhdl_if::Py_DecRef(__res);
        pyhdl_if::PyGILState_Release(state);
    endfunction

    virtual function void connect_phase(input pyhdl_if::PyObject phase);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (phase==null)?pyhdl_if::None:phase));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "connect_phase", __args);
        pyhdl_if::Py_DecRef(__res);
        pyhdl_if::PyGILState_Release(state);
    endfunction

    virtual task run_phase(input pyhdl_if::PyObject phase);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (phase==null)?pyhdl_if::None:phase));
        pyhdl_if::pyhdl_if_invokePyTask(__res, m_obj, "run_phase", __args);
        pyhdl_if::PyGILState_Release(state);
    endtask

    virtual function pyhdl_if::PyObject get_factory();
    endfunction

    virtual function pyhdl_if::PyObject get_config_object(
        input string name,
        input bit clone
    );

    endfunction

    virtual function void info(input string msg);
    endfunction

    virtual function string get_full_name();
    endfunction

    virtual function pyhdl_if::PyObject get_parent();
    endfunction

    virtual function pyhdl_if::PyObject get_children();
    endfunction

    virtual function bit _randomize();
    endfunction

    virtual function string get_name();
    endfunction

    virtual function string sprint();
    endfunction

    virtual function pyhdl_if::PyObject pack_ints();
    endfunction

    virtual function void unpack_ints(input pyhdl_if::PyObject data);
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "get_factory": begin
                pyhdl_if::PyObject __rval;
                __rval = get_factory();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                bit __clone = pyhdl_if::py_as_bool(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = get_config_object(
                    __name,
                    __clone);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "info": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                info(__msg);
            end
            "get_full_name": begin
                string __rval;
                __rval = get_full_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_parent": begin
                pyhdl_if::PyObject __rval;
                __rval = get_parent();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_children": begin
                pyhdl_if::PyObject __rval;
                __rval = get_children();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "_randomize": begin
                bit __rval;
                __rval = _randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "pack_ints": begin
                pyhdl_if::PyObject __rval;
                __rval = pack_ints();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "unpack_ints": begin
                pyhdl_if::PyObject __data = (pyhdl_if::PyTuple_GetItem(args, 0));
                unpack_ints(__data);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

interface class UvmComponentProxy_exp_if;
    pure virtual function void build_phase(input pyhdl_if::PyObject phase);
    pure virtual function void connect_phase(input pyhdl_if::PyObject phase);
    pure virtual task run_phase(input pyhdl_if::PyObject phase);
endclass

interface class UvmComponentProxy_imp_if;
    pure virtual function pyhdl_if::PyObject get_factory();
    pure virtual function pyhdl_if::PyObject get_config_object(
        input string name,
        input bit clone
    );

    pure virtual function void info(input string msg);
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject get_parent();
    pure virtual function pyhdl_if::PyObject get_children();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function string sprint();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class UvmComponentProxy_exp_impl implements UvmComponentProxy_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmComponentProxy");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_component_proxy", string clsname="UvmComponentProxy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmComponentProxy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function void build_phase(input pyhdl_if::PyObject phase);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (phase==null)?pyhdl_if::None:phase));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "build_phase", __args);
        pyhdl_if::Py_DecRef(__res);
        pyhdl_if::PyGILState_Release(state);
    endfunction
    virtual function void connect_phase(input pyhdl_if::PyObject phase);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (phase==null)?pyhdl_if::None:phase));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "connect_phase", __args);
        pyhdl_if::Py_DecRef(__res);
        pyhdl_if::PyGILState_Release(state);
    endfunction
    virtual task run_phase(input pyhdl_if::PyObject phase);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (phase==null)?pyhdl_if::None:phase));
        pyhdl_if::pyhdl_if_invokePyTask(__res, m_obj, "run_phase", __args);
        pyhdl_if::PyGILState_Release(state);
    endtask

    function void callpy();
        // Prepares arguments and calls Python object
    endfunction
endclass

class UvmComponentProxy_imp_impl #(type ImpT=UvmComponentProxy_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmComponentProxy");
        m_impl = impl;
        if (obj == null && create) begin
            // Create an instance of the Python class
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
        if (m_obj != null && m_impl != null) begin
            pyhdl_if::pyhdl_if_connectObject(m_obj, this);
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_component_proxy", string clsname="UvmComponentProxy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmComponentProxy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "get_factory": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_factory();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                bit __clone = pyhdl_if::py_as_bool(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.get_config_object(
                    __name,
                    __clone);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "info": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.info(__msg);
                __ret = pyhdl_if::None;
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_parent": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_parent();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_children": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_children();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "_randomize": begin
                bit __rval;
                __rval = m_impl._randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get_name": begin
                string __rval;
                __rval = m_impl.get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "pack_ints": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.pack_ints();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "unpack_ints": begin
                pyhdl_if::PyObject __data = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.unpack_ints(__data);
                __ret = pyhdl_if::None;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    virtual task invokeTask(
        output pyhdl_if::PyObject retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string method,
        input pyhdl_if::PyObject args);
        retval = pyhdl_if::None;
        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask
endclass

virtual class UvmObjectRgy #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_object_rgy", string clsname="UvmObjectRgy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmObjectRgy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    virtual function pyhdl_if::PyObject mk(input pyhdl_if::PyObject obj);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (obj==null)?pyhdl_if::None:obj));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "mk", __args);
        __ret = (__res);
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    virtual function string _get_type_dump();
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "_get_type_dump": begin
                string __rval;
                __rval = _get_type_dump();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

virtual class UvmObjectRgy_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new(pyhdl_if::PyObject obj=null);
        if (obj != null) begin
            init(obj);
        end
    endfunction

    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_object_rgy", string clsname="UvmObjectRgy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmObjectRgy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject mk(input pyhdl_if::PyObject obj);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (obj==null)?pyhdl_if::None:obj));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "mk", __args);
        __ret = (__res);
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    virtual function string _get_type_dump();
    endfunction


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "_get_type_dump": begin
                string __rval;
                __rval = _get_type_dump();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

interface class UvmObjectRgy_exp_if;
    pure virtual function pyhdl_if::PyObject mk(input pyhdl_if::PyObject obj);
endclass

interface class UvmObjectRgy_imp_if;
    pure virtual function string _get_type_dump();
endclass

class UvmObjectRgy_exp_impl implements UvmObjectRgy_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmObjectRgy");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_object_rgy", string clsname="UvmObjectRgy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmObjectRgy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject mk(input pyhdl_if::PyObject obj);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, (obj==null)?pyhdl_if::None:obj));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "mk", __args);
        __ret = (__res);
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    function void callpy();
        // Prepares arguments and calls Python object
    endfunction
endclass

class UvmObjectRgy_imp_impl #(type ImpT=UvmObjectRgy_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmObjectRgy");
        m_impl = impl;
        if (obj == null && create) begin
            // Create an instance of the Python class
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
        if (m_obj != null && m_impl != null) begin
            pyhdl_if::pyhdl_if_connectObject(m_obj, this);
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_object_rgy", string clsname="UvmObjectRgy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmObjectRgy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "_get_type_dump": begin
                string __rval;
                __rval = m_impl._get_type_dump();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    virtual task invokeTask(
        output pyhdl_if::PyObject retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string method,
        input pyhdl_if::PyObject args);
        retval = pyhdl_if::None;
        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask
endclass

virtual class UvmSequenceProxy #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_sequence_proxy", string clsname="UvmSequenceProxy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmSequenceProxy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    virtual task body();
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(0);
        pyhdl_if::pyhdl_if_invokePyTask(__res, m_obj, "body", __args);
        pyhdl_if::PyGILState_Release(state);
    endtask

    virtual function pyhdl_if::PyObject get_userdata();
    endfunction

    virtual function pyhdl_if::PyObject create_req();
    endfunction

    virtual function pyhdl_if::PyObject create_rsp();
    endfunction

    virtual task start_item(input pyhdl_if::PyObject item);
    endtask

    virtual task finish_item(input pyhdl_if::PyObject item);
    endtask


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            "start_item": begin
                pyhdl_if::PyObject __item = (pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                start_item(__item);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
            end
            "finish_item": begin
                pyhdl_if::PyObject __item = (pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                finish_item(__item);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "get_userdata": begin
                pyhdl_if::PyObject __rval;
                __rval = get_userdata();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_req": begin
                pyhdl_if::PyObject __rval;
                __rval = create_req();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_rsp": begin
                pyhdl_if::PyObject __rval;
                __rval = create_rsp();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

virtual class UvmSequenceProxy_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements pyhdl_if::ICallApi;

    pyhdl_if::PyObject       m_obj;

    function new(pyhdl_if::PyObject obj=null);
        if (obj != null) begin
            init(obj);
        end
    endfunction

    function void init(pyhdl_if::PyObject obj);
        pyhdl_if::pyhdl_if_connectObject(obj, this);
        m_obj = obj;
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_sequence_proxy", string clsname="UvmSequenceProxy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmSequenceProxy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual task body();
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(0);
        pyhdl_if::pyhdl_if_invokePyTask(__res, m_obj, "body", __args);
        pyhdl_if::PyGILState_Release(state);
    endtask

    virtual function pyhdl_if::PyObject get_userdata();
    endfunction

    virtual function pyhdl_if::PyObject create_req();
    endfunction

    virtual function pyhdl_if::PyObject create_rsp();
    endfunction

    virtual task start_item(input pyhdl_if::PyObject item);
    endtask

    virtual task finish_item(input pyhdl_if::PyObject item);
    endtask


    virtual task invokeTask(
        output pyhdl_if::PyObject        retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string                     method,
        input pyhdl_if::PyObject         args);

        retval = pyhdl_if::None;

        case (method)
            "start_item": begin
                pyhdl_if::PyObject __item = (pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                start_item(__item);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
            end
            "finish_item": begin
                pyhdl_if::PyObject __item = (pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                finish_item(__item);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask

    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "get_userdata": begin
                pyhdl_if::PyObject __rval;
                __rval = get_userdata();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_req": begin
                pyhdl_if::PyObject __rval;
                __rval = create_req();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_rsp": begin
                pyhdl_if::PyObject __rval;
                __rval = create_rsp();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

interface class UvmSequenceProxy_exp_if;
    pure virtual task body();
endclass

interface class UvmSequenceProxy_imp_if;
    pure virtual function pyhdl_if::PyObject get_userdata();
    pure virtual function pyhdl_if::PyObject create_req();
    pure virtual function pyhdl_if::PyObject create_rsp();
    pure virtual task start_item(input pyhdl_if::PyObject item);
    pure virtual task finish_item(input pyhdl_if::PyObject item);
endclass

class UvmSequenceProxy_exp_impl implements UvmSequenceProxy_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmSequenceProxy");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_sequence_proxy", string clsname="UvmSequenceProxy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmSequenceProxy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual task body();
        pyhdl_if::PyObject __res;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(0);
        pyhdl_if::pyhdl_if_invokePyTask(__res, m_obj, "body", __args);
        pyhdl_if::PyGILState_Release(state);
    endtask

    function void callpy();
        // Prepares arguments and calls Python object
    endfunction
endclass

class UvmSequenceProxy_imp_impl #(type ImpT=UvmSequenceProxy_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="UvmSequenceProxy");
        m_impl = impl;
        if (obj == null && create) begin
            // Create an instance of the Python class
            m_obj = create_pyobj();
        end else begin
            m_obj = obj;
        end
        if (m_obj != null && m_impl != null) begin
            pyhdl_if::pyhdl_if_connectObject(m_obj, this);
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.uvm_sequence_proxy", string clsname="UvmSequenceProxy");
        pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        __args = pyhdl_if::PyTuple_New(0);
        __cls_m = pyhdl_if::PyImport_ImportModule(modname);

        if (__cls_m == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find module %%s", modname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);
        if (__cls_t == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to find class %%s", clsname);
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        __obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);
        if (__obj == null) begin
            pyhdl_if::PyErr_Print();
            $display("Fatal Error: Failed to construct class UvmSequenceProxy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
        pyhdl_if::PyObject __ret = pyhdl_if::None;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        case (method)
            "get_userdata": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_userdata();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_req": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.create_req();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_rsp": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.create_rsp();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    virtual task invokeTask(
        output pyhdl_if::PyObject retval,
        inout pyhdl_if::PyGILState_STATE state,
        input string method,
        input pyhdl_if::PyObject args);
        retval = pyhdl_if::None;
        case (method)
            "start_item": begin
                pyhdl_if::PyObject __item = (pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                m_impl.start_item(__item);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
            end
            "finish_item": begin
                pyhdl_if::PyObject __item = (pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                m_impl.finish_item(__item);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask
endclass

