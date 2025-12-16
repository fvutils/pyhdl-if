/**
 * pyhdl_uvm_component_proxy.svh
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

typedef class pyhdl_uvm_component;
typedef class pyhdl_uvm_component_proxy_helper;
typedef class pyhdl_uvm_object_rgy;
typedef class pyhdl_uvm_phase;


/**
 * Class used to implement a UVM component in Python
 * Set the value of the pyclass field to specify the
 * class to create
 */
class pyhdl_uvm_component_proxy extends uvm_component;
    `uvm_component_utils(pyhdl_uvm_component_proxy)

    string                              pyclass;
    pyhdl_uvm_component_proxy_helper    m_helper;

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction



    function void build_phase(uvm_phase phase);
        string modname, clsname;
        PyObject mod, cls;
        int i;
        PyObject __ph = pyhdl_uvm_object_rgy::inst().wrap(phase);

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

        m_helper = new(this, pyclass, cls);

        // Allow the component/proxy to be located via the 'helper' 
        // handle
        pyhdl_uvm_object_rgy::inst().register_object(this, m_helper.m_obj);

        m_helper.m_exp.build_phase(__ph);
    endfunction

    function void connect_phase(uvm_phase phase);
        PyObject __ph = pyhdl_uvm_object_rgy::inst().wrap(phase);
        m_helper.m_exp.connect_phase(__ph);
    endfunction

    task run_phase(uvm_phase phase);
        PyObject __ph = pyhdl_uvm_object_rgy::inst().wrap(phase);
        // Ensure that the task scheduler is running
        pyhdl_if_start();

        m_helper.m_exp.run_phase(__ph);
    endtask

endclass


class pyhdl_uvm_component_proxy_helper 
    extends uvm_component_proxy_imp_impl #(pyhdl_uvm_component_proxy_helper);
    pyhdl_uvm_component_proxy       m_proxy;
    uvm_component_proxy_exp_impl    m_exp;

    function new(pyhdl_uvm_component_proxy impl, string clsname, PyObject cls);
        PyObject impl_o, args;

        super.new(this);
//        $cast(m_impl, this);

//        pyhdl_if_connectObject(m_obj, m_impl);

        m_proxy = impl;

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
//        m_proxy.set_int_local(name, value);
    endfunction

    virtual function void set_string_local(string name, string value);
//        m_proxy.set_string_local(name, value);
    endfunction

    virtual function void set_object_local(string name, PyObject value);
//        m_proxy.set_object_local(name, pyhdl_uvm_object_rgy::inst().get_object(value));
    endfunction

    virtual function PyObject get_config_object(string name, bit clone=0);
        py_tuple ret;
        uvm_object obj;
        py_object py_obj;
        bit has = 0; //uvm_config_db #(uvm_object)::get(m_proxy, name, obj);
        py_object py_has;

        if (has && obj != null) begin
            py_obj = new(pyhdl_uvm_object_rgy::inst().wrap(obj));
        end

        py_has = py_from_bool(has);

        return py_tuple::mk_init({py_has, py_obj}).borrow();
    endfunction

    virtual function PyObject get_children();
        py_list ret = new();
        uvm_component c[$];

        m_proxy.get_children(c);
        foreach (c[i]) begin
            ret.append_obj(pyhdl_uvm_object_rgy::inst().wrap(c[i]));
        end

        return ret.borrow();
    endfunction

    virtual function bit _randomize();
        return m_proxy.randomize();
    endfunction

    virtual function PyObject get_factory();
        return null;
    endfunction

    virtual function void info(string msg);
    endfunction

    virtual function PyObject get_parent();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.get_parent());
    endfunction

    virtual function string sprint();
        return m_proxy.sprint();
    endfunction

    virtual function string get_name();
        return m_proxy.get_name();
    endfunction

    virtual function string get_full_name();
        return m_proxy.get_full_name();
    endfunction

    virtual function PyObject pack_ints();
    endfunction

    virtual function void unpack_ints(PyObject data);
    endfunction

    virtual function PyObject create_object(string requested_type_name, string name="");
        uvm_object obj;

        obj = m_proxy.create_object(requested_type_name, name);

        if (obj != null) begin
            return pyhdl_uvm_object_rgy::inst().wrap(obj);
        end else begin
            return None;
        end
    endfunction

    virtual function PyObject create_component(string requested_type_name, string name);
        uvm_object obj;

        obj = m_proxy.create_component(requested_type_name, name);

        if (obj != null) begin
            return pyhdl_uvm_object_rgy::inst().wrap(obj);
        end else begin
            return None;
        end
    endfunction

endclass
