interface class IUvmCmdlineProcessor extends pyhdl_if::ICallApi;

    pure virtual function pyhdl_if::PyObject _get_plusargs();

endclass

virtual class UvmCmdlineProcessor #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmCmdlineProcessor;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_cmdline_processor", string clsname="UvmCmdlineProcessor");
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

virtual class UvmCmdlineProcessor_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmCmdlineProcessor;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_cmdline_processor", string clsname="UvmCmdlineProcessor");
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
interface class IUvmObject extends pyhdl_if::ICallApi;

    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function string sprint();

endclass

virtual class UvmObject #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmObject;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_object", string clsname="UvmObject");
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
                __ret = pyhdl_if::PyLong_FromLong(__rval);
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
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

virtual class UvmObject_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmObject;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_object", string clsname="UvmObject");
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
                __ret = pyhdl_if::PyLong_FromLong(__rval);
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
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass
interface class IUvmComponent extends pyhdl_if::ICallApi;

    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject get_children();
    pure virtual function pyhdl_if::PyObject get_config_object(input string name);

endclass

virtual class UvmComponent #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmComponent;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_component", string clsname="UvmComponent");
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

    virtual function pyhdl_if::PyObject get_children();
    endfunction

    virtual function pyhdl_if::PyObject get_config_object(input string name);
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
            "get_children": begin
                pyhdl_if::PyObject __rval;
                __rval = get_children();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = get_config_object(__name);
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

virtual class UvmComponent_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmComponent;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_component", string clsname="UvmComponent");
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

    virtual function pyhdl_if::PyObject get_children();
    endfunction

    virtual function pyhdl_if::PyObject get_config_object(input string name);
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
            "get_children": begin
                pyhdl_if::PyObject __rval;
                __rval = get_children();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = get_config_object(__name);
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
interface class IUvmFactory extends pyhdl_if::ICallApi;

    pure virtual function pyhdl_if::PyObject typenames();

endclass

virtual class UvmFactory #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmFactory;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_factory", string clsname="UvmFactory");
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

virtual class UvmFactory_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmFactory;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_factory", string clsname="UvmFactory");
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
interface class IUvmComponentProxy extends pyhdl_if::ICallApi;

    pure virtual function void build_phase(input pyhdl_if::PyObject phase);
    pure virtual function void connect_phase(input pyhdl_if::PyObject phase);
    pure virtual task run_phase(input pyhdl_if::PyObject phase);
    pure virtual function pyhdl_if::PyObject get_parent();
    pure virtual function pyhdl_if::PyObject get_factory();
    pure virtual function pyhdl_if::PyObject get_config_object(input string name);
    pure virtual function void info(input string msg);

endclass

virtual class UvmComponentProxy #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmComponentProxy;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_component_proxy", string clsname="UvmComponentProxy");
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

    virtual function pyhdl_if::PyObject get_parent();
    endfunction

    virtual function pyhdl_if::PyObject get_factory();
    endfunction

    virtual function pyhdl_if::PyObject get_config_object(input string name);
    endfunction

    virtual function void info(input string msg);
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
            "get_parent": begin
                pyhdl_if::PyObject __rval;
                __rval = get_parent();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_factory": begin
                pyhdl_if::PyObject __rval;
                __rval = get_factory();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = get_config_object(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "info": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                info(__msg);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass

virtual class UvmComponentProxy_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmComponentProxy;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_component_proxy", string clsname="UvmComponentProxy");
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

    virtual function pyhdl_if::PyObject get_parent();
    endfunction

    virtual function pyhdl_if::PyObject get_factory();
    endfunction

    virtual function pyhdl_if::PyObject get_config_object(input string name);
    endfunction

    virtual function void info(input string msg);
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
            "get_parent": begin
                pyhdl_if::PyObject __rval;
                __rval = get_parent();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_factory": begin
                pyhdl_if::PyObject __rval;
                __rval = get_factory();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = get_config_object(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "info": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                info(__msg);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

endclass
interface class IUvmSequenceProxy extends pyhdl_if::ICallApi;

    pure virtual task body();
    pure virtual function pyhdl_if::PyObject get_userdata();
    pure virtual function pyhdl_if::PyObject create_req();
    pure virtual function pyhdl_if::PyObject create_rsp();
    pure virtual task start_item(input pyhdl_if::PyObject item);
    pure virtual task finish_item(input pyhdl_if::PyObject item);

endclass

virtual class UvmSequenceProxy #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmSequenceProxy;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_sequence_proxy", string clsname="UvmSequenceProxy");
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

virtual class UvmSequenceProxy_wrap #(type BASE_T=CallEmptyBase) extends BASE_T implements IUvmSequenceProxy;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.uvm_sequence_proxy", string clsname="UvmSequenceProxy");
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
