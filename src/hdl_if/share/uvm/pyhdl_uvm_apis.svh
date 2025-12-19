interface class uvm_object_exp_if;
endclass

interface class uvm_object_imp_if;
    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_object_exp_impl implements uvm_object_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object", string clsname="uvm_object");
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
            $display("Fatal Error: Failed to construct class uvm_object");
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

class uvm_object_imp_impl #(type ImpT=uvm_object_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object", string clsname="uvm_object");
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
            $display("Fatal Error: Failed to construct class uvm_object");
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
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
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

interface class uvm_component_exp_if;
endclass

interface class uvm_component_imp_if;
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject get_parent();
    pure virtual function pyhdl_if::PyObject get_children();
    pure virtual function pyhdl_if::PyObject get_config_object(
        input string name,
        input bit clone
    );

    pure virtual function pyhdl_if::PyObject create_object(
        input string requested_type_name,
        input string name
    );

    pure virtual function pyhdl_if::PyObject create_component(
        input string requested_type_name,
        input string name
    );

    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_component_exp_impl implements uvm_component_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_component");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.component", string clsname="uvm_component");
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
            $display("Fatal Error: Failed to construct class uvm_component");
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

class uvm_component_imp_impl #(type ImpT=uvm_component_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_component");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.component", string clsname="uvm_component");
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
            $display("Fatal Error: Failed to construct class uvm_component");
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
            "create_object": begin
                pyhdl_if::PyObject __rval;
                string __requested_type_name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.create_object(
                    __requested_type_name,
                    __name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_component": begin
                pyhdl_if::PyObject __rval;
                string __requested_type_name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.create_component(
                    __requested_type_name,
                    __name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
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

interface class uvm_analysis_port_proxy_exp_if;
endclass

interface class uvm_analysis_port_proxy_imp_if;
    pure virtual function void add_listener(input pyhdl_if::PyObject l);
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject get_parent();
    pure virtual function pyhdl_if::PyObject get_children();
    pure virtual function pyhdl_if::PyObject get_config_object(
        input string name,
        input bit clone
    );

    pure virtual function pyhdl_if::PyObject create_object(
        input string requested_type_name,
        input string name
    );

    pure virtual function pyhdl_if::PyObject create_component(
        input string requested_type_name,
        input string name
    );

    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_analysis_port_proxy_exp_impl implements uvm_analysis_port_proxy_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_analysis_port_proxy");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.analysis_port_proxy", string clsname="uvm_analysis_port_proxy");
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
            $display("Fatal Error: Failed to construct class uvm_analysis_port_proxy");
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

class uvm_analysis_port_proxy_imp_impl #(type ImpT=uvm_analysis_port_proxy_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_analysis_port_proxy");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.analysis_port_proxy", string clsname="uvm_analysis_port_proxy");
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
            $display("Fatal Error: Failed to construct class uvm_analysis_port_proxy");
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
            "add_listener": begin
                pyhdl_if::PyObject __l = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.add_listener(__l);
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
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                bit __clone = pyhdl_if::py_as_bool(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.get_config_object(
                    __name,
                    __clone);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_object": begin
                pyhdl_if::PyObject __rval;
                string __requested_type_name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.create_object(
                    __requested_type_name,
                    __name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_component": begin
                pyhdl_if::PyObject __rval;
                string __requested_type_name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.create_component(
                    __requested_type_name,
                    __name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
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

interface class uvm_cmdline_processor_exp_if;
endclass

interface class uvm_cmdline_processor_imp_if;
    pure virtual function pyhdl_if::PyObject get_plusargs();
    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_cmdline_processor_exp_impl implements uvm_cmdline_processor_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_cmdline_processor");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.cmdline_processor", string clsname="uvm_cmdline_processor");
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
            $display("Fatal Error: Failed to construct class uvm_cmdline_processor");
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

class uvm_cmdline_processor_imp_impl #(type ImpT=uvm_cmdline_processor_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_cmdline_processor");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.cmdline_processor", string clsname="uvm_cmdline_processor");
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
            $display("Fatal Error: Failed to construct class uvm_cmdline_processor");
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
            "get_plusargs": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_plusargs();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
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

interface class uvm_component_proxy_exp_if;
    pure virtual function void build_phase(input pyhdl_if::PyObject phase);
    pure virtual function void connect_phase(input pyhdl_if::PyObject phase);
    pure virtual task run_phase(input pyhdl_if::PyObject phase);
endclass

interface class uvm_component_proxy_imp_if;
    pure virtual function pyhdl_if::PyObject get_config_object(
        input string name,
        input bit clone
    );

    pure virtual function void reseed();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function longint get_inst_count();
    pure virtual function void info(input string msg);
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create();
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function pyhdl_if::PyObject create_object(
        input string requested_type_name,
        input string name
    );

    pure virtual function pyhdl_if::PyObject create_component(
        input string requested_type_name,
        input string name
    );

    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject get_parent();
    pure virtual function pyhdl_if::PyObject get_children();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function string sprint();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_component_proxy_exp_impl implements uvm_component_proxy_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_component_proxy");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.component_proxy", string clsname="uvm_component_proxy");
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
            $display("Fatal Error: Failed to construct class uvm_component_proxy");
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

class uvm_component_proxy_imp_impl #(type ImpT=uvm_component_proxy_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_component_proxy");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.component_proxy", string clsname="uvm_component_proxy");
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
            $display("Fatal Error: Failed to construct class uvm_component_proxy");
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
            "get_config_object": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                bit __clone = pyhdl_if::py_as_bool(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.get_config_object(
                    __name,
                    __clone);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
            end
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "info": begin
                string __msg = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.info(__msg);
                __ret = pyhdl_if::None;
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.create();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "create_object": begin
                pyhdl_if::PyObject __rval;
                string __requested_type_name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.create_object(
                    __requested_type_name,
                    __name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "create_component": begin
                pyhdl_if::PyObject __rval;
                string __requested_type_name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                __rval = m_impl.create_component(
                    __requested_type_name,
                    __name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
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
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
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

interface class uvm_enum_rgy_exp_if;
    pure virtual function pyhdl_if::PyObject get_enum_type(input string type_name);
    pure virtual function pyhdl_if::PyObject get_enum_types();
    pure virtual function bit has_enum_type(input string type_name);
endclass

interface class uvm_enum_rgy_imp_if;
    pure virtual function pyhdl_if::PyObject _get_enum_names(input string type_name);
    pure virtual function pyhdl_if::PyObject _get_enum_values(input string type_name);
    pure virtual function pyhdl_if::PyObject _get_enum_types();
endclass

class uvm_enum_rgy_exp_impl implements uvm_enum_rgy_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_enum_rgy");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.enum_rgy", string clsname="uvm_enum_rgy");
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
            $display("Fatal Error: Failed to construct class uvm_enum_rgy");
            $finish;
            pyhdl_if::PyGILState_Release(state);
            return null;
        end

        pyhdl_if::PyGILState_Release(state);

        return __obj;
    endfunction


    virtual function pyhdl_if::PyObject get_enum_type(input string type_name);
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, pyhdl_if::PyUnicode_FromString(type_name)));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "get_enum_type", __args);
        __ret = (__res);
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction
    virtual function pyhdl_if::PyObject get_enum_types();
        pyhdl_if::PyObject __res;
        pyhdl_if::PyObject __ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(0);
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "get_enum_types", __args);
        __ret = (__res);
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction
    virtual function bit has_enum_type(input string type_name);
        pyhdl_if::PyObject __res;
        bit __ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, pyhdl_if::PyUnicode_FromString(type_name)));
        __res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, "has_enum_type", __args);
        __ret = pyhdl_if::py_as_bool(__res);
        pyhdl_if::PyGILState_Release(state);
        return __ret;
    endfunction

    function void callpy();
        // Prepares arguments and calls Python object
    endfunction
endclass

class uvm_enum_rgy_imp_impl #(type ImpT=uvm_enum_rgy_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_enum_rgy");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.enum_rgy", string clsname="uvm_enum_rgy");
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
            $display("Fatal Error: Failed to construct class uvm_enum_rgy");
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
            "_get_enum_names": begin
                pyhdl_if::PyObject __rval;
                string __type_name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl._get_enum_names(__type_name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "_get_enum_values": begin
                pyhdl_if::PyObject __rval;
                string __type_name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl._get_enum_values(__type_name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "_get_enum_types": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl._get_enum_types();
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

interface class uvm_object_list_exp_if;
endclass

interface class uvm_object_list_imp_if;
    pure virtual function pyhdl_if::PyObject at(input int index);
    pure virtual function void push_back(input pyhdl_if::PyObject obj);
    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_object_list_exp_impl implements uvm_object_list_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object_list");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object_list", string clsname="uvm_object_list");
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
            $display("Fatal Error: Failed to construct class uvm_object_list");
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

class uvm_object_list_imp_impl #(type ImpT=uvm_object_list_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object_list");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object_list", string clsname="uvm_object_list");
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
            $display("Fatal Error: Failed to construct class uvm_object_list");
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
            "at": begin
                pyhdl_if::PyObject __rval;
                int __index = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.at(__index);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "push_back": begin
                pyhdl_if::PyObject __obj = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.push_back(__obj);
                __ret = pyhdl_if::None;
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
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

interface class uvm_object_map_exp_if;
endclass

interface class uvm_object_map_imp_if;
    pure virtual function bit has_key(input string key);
    pure virtual function pyhdl_if::PyObject get(input string key);
    pure virtual function void insert(
        input string key,
        input pyhdl_if::PyObject obj
    );

    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_object_map_exp_impl implements uvm_object_map_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object_map");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object_map", string clsname="uvm_object_map");
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
            $display("Fatal Error: Failed to construct class uvm_object_map");
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

class uvm_object_map_imp_impl #(type ImpT=uvm_object_map_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object_map");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object_map", string clsname="uvm_object_map");
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
            $display("Fatal Error: Failed to construct class uvm_object_map");
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
            "has_key": begin
                bit __rval;
                string __key = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.has_key(__key);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "get": begin
                pyhdl_if::PyObject __rval;
                string __key = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.get(__key);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "insert": begin
                string __key = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __obj = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.insert(
                    __key,
                    __obj);
                __ret = pyhdl_if::None;
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
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

interface class uvm_object_string_exp_if;
endclass

interface class uvm_object_string_imp_if;
    pure virtual function string get_value();
    pure virtual function void set_value(input string val);
    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_object_string_exp_impl implements uvm_object_string_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object_string");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object_string", string clsname="uvm_object_string");
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
            $display("Fatal Error: Failed to construct class uvm_object_string");
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

class uvm_object_string_imp_impl #(type ImpT=uvm_object_string_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object_string");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object_string", string clsname="uvm_object_string");
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
            $display("Fatal Error: Failed to construct class uvm_object_string");
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
            "get_value": begin
                string __rval;
                __rval = m_impl.get_value();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "set_value": begin
                string __val = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_value(__val);
                __ret = pyhdl_if::None;
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
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

interface class uvm_object_rgy_exp_if;
    pure virtual function pyhdl_if::PyObject mk(input pyhdl_if::PyObject obj);
endclass

interface class uvm_object_rgy_imp_if;
    pure virtual function pyhdl_if::PyObject clp();
    pure virtual function string _get_type_dump();
    pure virtual function pyhdl_if::PyObject create_by_name(input string name);
endclass

class uvm_object_rgy_exp_impl implements uvm_object_rgy_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object_rgy");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object_rgy", string clsname="uvm_object_rgy");
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
            $display("Fatal Error: Failed to construct class uvm_object_rgy");
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

class uvm_object_rgy_imp_impl #(type ImpT=uvm_object_rgy_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_object_rgy");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.object_rgy", string clsname="uvm_object_rgy");
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
            $display("Fatal Error: Failed to construct class uvm_object_rgy");
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
            "clp": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clp();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "_get_type_dump": begin
                string __rval;
                __rval = m_impl._get_type_dump();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create_by_name": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create_by_name(__name);
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

interface class uvm_reg_exp_if;
endclass

interface class uvm_reg_imp_if;
    pure virtual function pyhdl_if::PyObject get_fields();
    pure virtual function void set(input longint unsigned value);
    pure virtual function longint unsigned get();
    pure virtual task write(output bit retval, input longint unsigned value);
    pure virtual task read(output pyhdl_if::PyObject retval);
    pure virtual task update(output bit retval);
    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_reg_exp_impl implements uvm_reg_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_reg");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.reg", string clsname="uvm_reg");
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
            $display("Fatal Error: Failed to construct class uvm_reg");
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

class uvm_reg_imp_impl #(type ImpT=uvm_reg_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_reg");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.reg", string clsname="uvm_reg");
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
            $display("Fatal Error: Failed to construct class uvm_reg");
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
            "get_fields": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_fields();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "set": begin
                longint unsigned __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set(__value);
                __ret = pyhdl_if::None;
            end
            "get": begin
                longint unsigned __rval;
                __rval = m_impl.get();
                __ret = pyhdl_if::PyLong_FromUnsignedLongLong(__rval);
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
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
            "write": begin
                bit __retval;
                longint unsigned __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                m_impl.write(__retval, __value);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
                retval = pyhdl_if::PyLong_FromLong(longint'(__retval));
            end
            "read": begin
                pyhdl_if::PyObject __retval;
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                m_impl.read(__retval);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
                retval = (__retval==null)?pyhdl_if::None:__retval;
            end
            "update": begin
                bit __retval;
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                m_impl.update(__retval);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
                retval = pyhdl_if::PyLong_FromLong(longint'(__retval));
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask
endclass

interface class uvm_reg_block_exp_if;
endclass

interface class uvm_reg_block_imp_if;
    pure virtual function pyhdl_if::PyObject get_parent();
    pure virtual function pyhdl_if::PyObject get_root_blocks();
    pure virtual function pyhdl_if::PyObject get_registers();
    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_reg_block_exp_impl implements uvm_reg_block_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_reg_block");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.reg_block", string clsname="uvm_reg_block");
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
            $display("Fatal Error: Failed to construct class uvm_reg_block");
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

class uvm_reg_block_imp_impl #(type ImpT=uvm_reg_block_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_reg_block");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.reg_block", string clsname="uvm_reg_block");
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
            $display("Fatal Error: Failed to construct class uvm_reg_block");
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
            "get_parent": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_parent();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_root_blocks": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_root_blocks();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "get_registers": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.get_registers();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
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

interface class uvm_reg_field_exp_if;
endclass

interface class uvm_reg_field_imp_if;
    pure virtual function void set(input longint unsigned value);
    pure virtual function longint unsigned get();
    pure virtual task write(output bit retval, input longint unsigned value);
    pure virtual task read(output pyhdl_if::PyObject retval);
    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function string get_name();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_reg_field_exp_impl implements uvm_reg_field_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_reg_field");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.reg_field", string clsname="uvm_reg_field");
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
            $display("Fatal Error: Failed to construct class uvm_reg_field");
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

class uvm_reg_field_imp_impl #(type ImpT=uvm_reg_field_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_reg_field");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.reg_field", string clsname="uvm_reg_field");
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
            $display("Fatal Error: Failed to construct class uvm_reg_field");
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
            "set": begin
                longint unsigned __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set(__value);
                __ret = pyhdl_if::None;
            end
            "get": begin
                longint unsigned __rval;
                __rval = m_impl.get();
                __ret = pyhdl_if::PyLong_FromUnsignedLongLong(__rval);
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
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
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
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
            "write": begin
                bit __retval;
                longint unsigned __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                m_impl.write(__retval, __value);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
                retval = pyhdl_if::PyLong_FromLong(longint'(__retval));
            end
            "read": begin
                pyhdl_if::PyObject __retval;
                pyhdl_if::PyGILState_Release(state); // Release the GIL before invoking the task
                m_impl.read(__retval);
                state = pyhdl_if::PyGILState_Ensure(); // Reacquire the GIL after invoking the task
                retval = (__retval==null)?pyhdl_if::None:__retval;
            end
            default: begin
                $display("Fatal: unsupported method call %0s", method);
            end
        endcase
    endtask
endclass

interface class uvm_sequence_proxy_exp_if;
    pure virtual task body();
endclass

interface class uvm_sequence_proxy_imp_if;
    pure virtual function pyhdl_if::PyObject get_userdata();
    pure virtual function pyhdl_if::PyObject create_req();
    pure virtual function pyhdl_if::PyObject create_rsp();
    pure virtual task start_item(input pyhdl_if::PyObject item);
    pure virtual task finish_item(input pyhdl_if::PyObject item);
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create();
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function pyhdl_if::PyObject _get_sequencer();
endclass

class uvm_sequence_proxy_exp_impl implements uvm_sequence_proxy_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_sequence_proxy");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.sequence_proxy", string clsname="uvm_sequence_proxy");
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
            $display("Fatal Error: Failed to construct class uvm_sequence_proxy");
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

class uvm_sequence_proxy_imp_impl #(type ImpT=uvm_sequence_proxy_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_sequence_proxy");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.sequence_proxy", string clsname="uvm_sequence_proxy");
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
            $display("Fatal Error: Failed to construct class uvm_sequence_proxy");
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
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.create();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "_get_sequencer": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl._get_sequencer();
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

interface class uvm_phase_exp_if;
endclass

interface class uvm_phase_imp_if;
    pure virtual function string get_name();
    pure virtual function void raise_objection(
        input pyhdl_if::PyObject obj,
        input longint count
    );

    pure virtual function void drop_objection(
        input pyhdl_if::PyObject obj,
        input longint count
    );

    pure virtual function void reseed();
    pure virtual function bit _randomize();
    pure virtual function void set_name(input string name);
    pure virtual function longint get_inst_id();
    pure virtual function string get_type_name();
    pure virtual function pyhdl_if::PyObject create(input string name);
    pure virtual function pyhdl_if::PyObject clone();
    pure virtual function void print();
    pure virtual function string convert2string();
    pure virtual function void record();
    pure virtual function void copy(input pyhdl_if::PyObject rhs);
    pure virtual function bit compare(input pyhdl_if::PyObject rhs);
    pure virtual function void set_int_local(
        input string name,
        input longint value
    );

    pure virtual function void set_string_local(
        input string name,
        input string value
    );

    pure virtual function void set_object_local(
        input string name,
        input pyhdl_if::PyObject value
    );

    pure virtual function longint get_inst_count();
    pure virtual function string sprint();
    pure virtual function string get_full_name();
    pure virtual function pyhdl_if::PyObject pack_ints();
    pure virtual function void unpack_ints(input pyhdl_if::PyObject data);
endclass

class uvm_phase_exp_impl implements uvm_phase_exp_if;
    pyhdl_if::PyObject m_obj;
    function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_phase");
        m_obj = obj;
        if (create && (m_obj == null)) begin
            m_obj = create_pyobj();
            if (m_obj != null) begin
                pyhdl_if::pyhdl_if_connectObject(m_obj, null);
            end
        end else begin
            m_obj = obj;
        end
    endfunction

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.phase", string clsname="uvm_phase");
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
            $display("Fatal Error: Failed to construct class uvm_phase");
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

class uvm_phase_imp_impl #(type ImpT=uvm_phase_imp_if) implements pyhdl_if::ICallApi;
    ImpT m_impl;
    PyObject m_obj;
    function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1, string clsname="uvm_phase");
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

    static function pyhdl_if::PyObject create_pyobj(string modname="hdl_if.uvm.wrap.phase", string clsname="uvm_phase");
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
            $display("Fatal Error: Failed to construct class uvm_phase");
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
            "get_name": begin
                string __rval;
                __rval = m_impl.get_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "raise_objection": begin
                pyhdl_if::PyObject __obj = (pyhdl_if::PyTuple_GetItem(args, 0));
                longint __count = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.raise_objection(
                    __obj,
                    __count);
                __ret = pyhdl_if::None;
            end
            "drop_objection": begin
                pyhdl_if::PyObject __obj = (pyhdl_if::PyTuple_GetItem(args, 0));
                longint __count = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.drop_objection(
                    __obj,
                    __count);
                __ret = pyhdl_if::None;
            end
            "reseed": begin
                m_impl.reseed();
                __ret = pyhdl_if::None;
            end
            "_randomize": begin
                bit __rval;
                __rval = m_impl._randomize();
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_name": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.set_name(__name);
                __ret = pyhdl_if::None;
            end
            "get_inst_id": begin
                longint __rval;
                __rval = m_impl.get_inst_id();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "get_type_name": begin
                string __rval;
                __rval = m_impl.get_type_name();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "create": begin
                pyhdl_if::PyObject __rval;
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.create(__name);
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "clone": begin
                pyhdl_if::PyObject __rval;
                __rval = m_impl.clone();
                __ret = (__rval==null)?pyhdl_if::None:__rval;
            end
            "print": begin
                m_impl.print();
                __ret = pyhdl_if::None;
            end
            "convert2string": begin
                string __rval;
                __rval = m_impl.convert2string();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "record": begin
                m_impl.record();
                __ret = pyhdl_if::None;
            end
            "copy": begin
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                m_impl.copy(__rhs);
                __ret = pyhdl_if::None;
            end
            "compare": begin
                bit __rval;
                pyhdl_if::PyObject __rhs = (pyhdl_if::PyTuple_GetItem(args, 0));
                __rval = m_impl.compare(__rhs);
                __ret = pyhdl_if::PyLong_FromLong(longint'(__rval));
            end
            "set_int_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                longint __value = pyhdl_if::PyLong_AsLong(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_int_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_string_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                string __value = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_string_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "set_object_local": begin
                string __name = pyhdl_if::PyUnicode_AsUTF8(pyhdl_if::PyTuple_GetItem(args, 0));
                pyhdl_if::PyObject __value = (pyhdl_if::PyTuple_GetItem(args, 1));
                m_impl.set_object_local(
                    __name,
                    __value);
                __ret = pyhdl_if::None;
            end
            "get_inst_count": begin
                longint __rval;
                __rval = m_impl.get_inst_count();
                __ret = pyhdl_if::PyLong_FromLong(__rval);
            end
            "sprint": begin
                string __rval;
                __rval = m_impl.sprint();
                __ret = pyhdl_if::PyUnicode_FromString(__rval);
            end
            "get_full_name": begin
                string __rval;
                __rval = m_impl.get_full_name();
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

