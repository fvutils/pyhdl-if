/**
 * pyhdl_uvm_sequence_proxy.svh
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

typedef class pyhdl_uvm_sequence_proxy_helper;
typedef class pyhdl_uvm_object_rgy;

interface class pyhdl_uvm_sequence_proxy_if;
    pure virtual function uvm_sequencer_base _get_sequencer();
endclass

class pyhdl_uvm_sequence_proxy #(
        type REQ=uvm_sequence_item,
        type RSP=REQ,
        type UserDataT=uvm_object,
        string PyClass="")
    extends uvm_sequence #(.REQ(REQ), .RSP(RSP))
    implements pyhdl_uvm_sequence_proxy_if;
    typedef pyhdl_uvm_sequence_proxy #(.REQ(REQ), .RSP(RSP), .UserDataT(UserDataT), .PyClass(PyClass)) this_t;
    `uvm_object_param_utils(this_t);

    typedef pyhdl_uvm_sequence_proxy_helper #(.REQ(REQ), .RSP(RSP)) helper_t;

    string      pyclass = PyClass;
    UserDataT   userdata;
    helper_t    m_helper;

    function new(string name="pyhdl_uvm_sequence_proxy");
        super.new(name);
    endfunction

    virtual function uvm_object get_userdata();
        return userdata;
    endfunction

    virtual function uvm_sequencer_base _get_sequencer();
        return m_sequencer;
    endfunction

    task body();
        string modname, clsname;
        PyObject mod, cls;
        int i;

        // Ensure that the task scheduler is running
        pyhdl_if_start();

        if (pyclass == "") begin
            `uvm_fatal(get_name(), "No value specified for 'pyclass'");
        end

        for (i=pyclass.len()-1; i>=0; i--) begin
            if (pyclass[i] == ":") begin
                clsname = pyclass.substr(i+1, pyclass.len()-1);
                break;
            end
        end

        if (clsname == "") begin
            `uvm_fatal(get_name(), $sformatf("Failed to find '::' in pyclass %0s", pyclass))
        end

        while (i>=0) begin
            if (pyclass[i] != ":") begin
                break;
            end
            i--;
        end

        modname = pyclass.substr(0, i);

        `PYHDL_IF_DEBUG(("modname=%0s clsname=%0s", modname, clsname))

        mod = PyImport_ImportModule(modname);
        if (mod == null) begin
            PyErr_Print();
            `uvm_fatal(get_name, $sformatf("Failed to load Python module %0s", modname));
            return;
        end

        cls = PyObject_GetAttrString(mod, clsname);

        if (cls == null) begin
            PyErr_Print();
            `uvm_fatal(get_name, $sformatf("Failed to find class %0s in Python module %0s", 
                clsname, modname));
            return;
        end

        m_helper = new(pyclass, cls);
        m_helper.m_proxy = this;
        m_helper.m_userdata = userdata;

        // Associate the Python object for the helper with the sequence object
        pyhdl_uvm_object_rgy::inst().register_object(this, m_helper.m_obj);

        m_helper.m_exp.body();
    endtask

endclass

class pyhdl_uvm_sequence_proxy_helper #(type REQ=uvm_sequence_item, type RSP=REQ)
        extends uvm_sequence_proxy_imp_impl #(pyhdl_uvm_sequence_proxy_helper #(REQ,REQ)) 
        implements pyhdl_uvm_object_if;
    uvm_sequence_base               m_proxy;
    uvm_sequence_proxy_exp_impl     m_exp;
    uvm_object                      m_userdata;

    function new(string clsname, PyObject cls);
        PyObject impl_o, args;
        super.new(this);

        m_exp = new(m_obj);

        args = PyTuple_New(1);
        void'(PyTuple_SetItem(args, 0, m_obj));

        impl_o = PyObject_Call(cls, args, null);
        if (impl_o == null) begin
            PyErr_Print();
            `PYHDL_IF_FATAL(("Failed to construct user class %0s", clsname))
            $finish;
        end

        if (PyObject_SetAttrString(m_obj, "_impl", impl_o) != 0) begin
            PyErr_Print();
            `PYHDL_IF_FATAL(("Failed to set _impl on proxy wrapper"))
            $finish;
        end
    endfunction

    virtual function uvm_object get_object();
        return m_proxy;
    endfunction

    virtual function PyObject get_pyobject();
        return m_obj;
    endfunction

    virtual function string get_name();
        `PYHDL_IF_DEBUG(("get_name"))
        return m_proxy.get_name();
    endfunction

    virtual function void reseed();
        m_proxy.reseed();
    endfunction

    virtual function void set_name(string name);
        m_proxy.set_name(name);
    endfunction

    virtual function int get_inst_id();
        return m_proxy.get_inst_id();
    endfunction

    virtual function int get_inst_count();
        return m_proxy.get_inst_count();
    endfunction

    virtual function string get_type_name();
        return m_proxy.get_type_name();
    endfunction

    virtual function PyObject create();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.create());
    endfunction

    virtual function PyObject clone();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.clone());
    endfunction

    virtual function void print();
        m_proxy.print();
    endfunction

    virtual function string convert2string();
        return m_proxy.convert2string();
    endfunction

    virtual function void record();
        m_proxy.record();
    endfunction

    virtual function void copy(PyObject rhs);
        m_proxy.copy(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction

    virtual function bit compare(PyObject rhs);
        return m_proxy.compare(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction

    virtual function void set_int_local(string name, int value);
        m_proxy.set_int_local(name, value);
    endfunction

    virtual function void set_string_local(string name, string value);
        m_proxy.set_string_local(name, value);
    endfunction

    virtual function void set_object_local(string name, PyObject value);
        m_proxy.set_object_local(name, pyhdl_uvm_object_rgy::inst().get_object(value));
    endfunction

    virtual function PyObject _get_sequencer();
        pyhdl_uvm_sequence_proxy_if proxy;
        $cast (proxy, m_proxy);
        `PYHDL_IF_DEBUG(("-- _get_sequencer"))
        return pyhdl_uvm_object_rgy::inst().wrap(proxy._get_sequencer());
    endfunction

    virtual function PyObject get_userdata();
        if (m_userdata != null) begin
            return pyhdl_uvm_object_rgy::inst().wrap(m_userdata);
        end else begin
            return None;
        end
    endfunction

    virtual function PyObject create_req();
        REQ req = REQ::type_id::create();
        return pyhdl_uvm_object_rgy::inst().wrap(req);
    endfunction

    virtual function PyObject create_rsp();
        RSP rsp = REQ::type_id::create();
        return pyhdl_uvm_object_rgy::inst().wrap(rsp);
    endfunction

    virtual task start_item(PyObject item);
        uvm_object item_o;
        uvm_sequence_item uvm_item;

        item_o = pyhdl_uvm_object_rgy::inst().get_object(item);
        if ($cast(uvm_item, item_o)) begin
            m_proxy.start_item(uvm_item);
        end else begin
            `PYHDL_IF_FATAL(("can't cast back to a sequence item"))
        end
    endtask

    virtual task finish_item(PyObject item);
        uvm_object item_o;
        uvm_sequence_item uvm_item;

        item_o = pyhdl_uvm_object_rgy::inst().get_object(item);
        if ($cast(uvm_item, item_o)) begin
            m_proxy.finish_item(uvm_item);
        end else begin
            `PYHDL_IF_FATAL(("can't cast back to a sequence item"))
        end
    endtask

endclass