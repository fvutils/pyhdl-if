interface class IFieldIF extends pyhdl_if::ICallApi;

    pure virtual function string get_name();

endclass

virtual class FieldIF #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IFieldIF;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.field_if", string clsname="FieldIF");
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
            $display("Fatal Error: Failed to construct class FieldIF");
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

    virtual function string get_name();
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
        case (method)
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass

virtual class FieldIF_wrap #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IFieldIF;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.field_if", string clsname="FieldIF");
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
            $display("Fatal Error: Failed to construct class FieldIF");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function string get_name();
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
        case (method)
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass
interface class IObjectTypeIF extends pyhdl_if::ICallApi;

    pure virtual function string get_name();
    pure virtual function pyhdl_if::PyObject get_fields();

endclass

virtual class ObjectTypeIF #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IObjectTypeIF;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.object_type_if", string clsname="ObjectTypeIF");
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
            $display("Fatal Error: Failed to construct class ObjectTypeIF");
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

    virtual function string get_name();
    endfunction

    virtual function pyhdl_if::PyObject get_fields();
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
        case (method)
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_fields": begin
                pyhdl_if::PyObject __rval;
                __rval = get_fields();
                __ret = __rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass

virtual class ObjectTypeIF_wrap #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IObjectTypeIF;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.object_type_if", string clsname="ObjectTypeIF");
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
            $display("Fatal Error: Failed to construct class ObjectTypeIF");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function string get_name();
    endfunction

    virtual function pyhdl_if::PyObject get_fields();
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
        case (method)
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_fields": begin
                pyhdl_if::PyObject __rval;
                __rval = get_fields();
                __ret = __rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass
interface class IObjectIF extends pyhdl_if::ICallApi;

    pure virtual function string get_name();
    pure virtual function pyhdl_if::PyObject get_object_type();

endclass

virtual class ObjectIF #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IObjectIF;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.object_if", string clsname="ObjectIF");
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
            $display("Fatal Error: Failed to construct class ObjectIF");
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

    virtual function string get_name();
    endfunction

    virtual function pyhdl_if::PyObject get_object_type();
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
        case (method)
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_object_type": begin
                pyhdl_if::PyObject __rval;
                __rval = get_object_type();
                __ret = __rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass

virtual class ObjectIF_wrap #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IObjectIF;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.object_if", string clsname="ObjectIF");
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
            $display("Fatal Error: Failed to construct class ObjectIF");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function string get_name();
    endfunction

    virtual function pyhdl_if::PyObject get_object_type();
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
        case (method)
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_object_type": begin
                pyhdl_if::PyObject __rval;
                __rval = get_object_type();
                __ret = __rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass
interface class IComponentIF extends pyhdl_if::ICallApi;

    pure virtual function string get_name();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject create_object_by_name(
        input string typename,
        input string name
    );


endclass

virtual class ComponentIF #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IComponentIF;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.component_if", string clsname="ComponentIF");
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
            $display("Fatal Error: Failed to construct class ComponentIF");
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

    virtual function string get_name();
    endfunction

    virtual function string get_full_name();
    endfunction

    virtual function pyhdl_if::PyObject create_object_by_name(
        input string typename,
        input string name
    );

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
        case (method)
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = get_full_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create_object_by_name": begin
                pyhdl_if::PyObject __rval;
                string __typename = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = create_object_by_name(
                    __typename,
                    __name);
                __ret = __rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass

virtual class ComponentIF_wrap #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IComponentIF;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.component_if", string clsname="ComponentIF");
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
            $display("Fatal Error: Failed to construct class ComponentIF");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function string get_name();
    endfunction

    virtual function string get_full_name();
    endfunction

    virtual function pyhdl_if::PyObject create_object_by_name(
        input string typename,
        input string name
    );

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
        case (method)
            "get_name": begin
                string __rval;
                __rval = get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = get_full_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create_object_by_name": begin
                pyhdl_if::PyObject __rval;
                string __typename = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = create_object_by_name(
                    __typename,
                    __name);
                __ret = __rval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass
interface class IRoot extends pyhdl_if::ICallApi;

    pure virtual function void post_build(input pyhdl_if::PyObject root);
    pure virtual function void post_connect(input pyhdl_if::PyObject root);
    pure virtual task run(input pyhdl_if::PyObject root);

endclass

class Root #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IRoot;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.root", string clsname="Root");
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
            $display("Fatal Error: Failed to construct class Root");
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

    virtual function void post_build(input pyhdl_if::PyObject root);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, root));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "post_build", __args);
        pyhdl_if::Py_DecRef(__res);
    endfunction

    virtual function void post_connect(input pyhdl_if::PyObject root);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, root));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "post_connect", __args);
        pyhdl_if::Py_DecRef(__res);
    endfunction

    virtual task run(input pyhdl_if::PyObject root);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, root));
        pyhdl_if::pyhdl_if_invokePyTask(__res, m_obj, "run", __args);
    endtask


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
        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass

class Root_wrap #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IRoot;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.root", string clsname="Root");
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
            $display("Fatal Error: Failed to construct class Root");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function void post_build(input pyhdl_if::PyObject root);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, root));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "post_build", __args);
        pyhdl_if::Py_DecRef(__res);
    endfunction

    virtual function void post_connect(input pyhdl_if::PyObject root);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, root));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "post_connect", __args);
        pyhdl_if::Py_DecRef(__res);
    endfunction

    virtual task run(input pyhdl_if::PyObject root);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, root));
        pyhdl_if::pyhdl_if_invokePyTask(__res, m_obj, "run", __args);
    endtask


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
        case (method)
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass
interface class IRootIF extends pyhdl_if::ICallApi;

    pure virtual function void info(
        input int level,
        input string msg
    );

    pure virtual function void error(input string msg);
    pure virtual function void fatal(input string msg);

endclass

virtual class RootIF #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IRootIF;

    pyhdl_if::PyObject       m_obj;

    function new();
        m_obj = create_pyobj();
        pyhdl_if::pyhdl_if_connectObject(m_obj, this);
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.root_if", string clsname="RootIF");
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
            $display("Fatal Error: Failed to construct class RootIF");
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

    virtual function void info(
        input int level,
        input string msg
    );

    endfunction

    virtual function void error(input string msg);
    endfunction

    virtual function void fatal(input string msg);
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
        case (method)
            "info": begin
                int __level = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 0));
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                info(
                    __level,
                    __msg);
            end
            "error": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                error(__msg);
            end
            "fatal": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                fatal(__msg);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass

virtual class RootIF_wrap #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements IRootIF;

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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.via.root_if", string clsname="RootIF");
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
            $display("Fatal Error: Failed to construct class RootIF");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function void info(
        input int level,
        input string msg
    );

    endfunction

    virtual function void error(input string msg);
    endfunction

    virtual function void fatal(input string msg);
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
        case (method)
            "info": begin
                int __level = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 0));
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                info(
                    __level,
                    __msg);
            end
            "error": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                error(__msg);
            end
            "fatal": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                fatal(__msg);
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase

        return __ret;
    endfunction

endclass
