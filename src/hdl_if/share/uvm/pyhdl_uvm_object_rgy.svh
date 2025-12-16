/**
 * pyhdl_uvm_object_rgy.svh
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

`include "pyhdl_if_macros.svh"

typedef class pyhdl_uvm_object;
typedef interface class pyhdl_uvm_object_if;
typedef interface class pyhdl_uvm_wrapper_factory;
typedef class pyhdl_uvm_wrapper_factory_t;
typedef class create_t;
typedef class pyhdl_uvm_object_type;
typedef class pyhdl_uvm_object_type_p;

/**
 * Implements a report catcher to allow capturing the 
 * list of object typenames printed by the factory
 */
class factory_print_catcher extends uvm_report_catcher;
    string  factory_print;

    function new(string name="factory_print_catcher");
        super.new(name);
    endfunction

    function action_e catch();
        factory_print = get_message();

        // Suppress the message
        return CAUGHT;
    endfunction
endclass


class pyhdl_uvm_object_type_rgy;

endclass

class pyhdl_uvm_object_type_rgy_p #(
    type Ct=uvm_object,
    type Ctw=pyhdl_uvm_object_w,
    type Cb=uvm_object,
    type Cbw=pyhdl_uvm_object_w) extends pyhdl_uvm_object_type_rgy;
    typedef pyhdl_uvm_object_type_rgy_p #(Ct,Ctw,Cb,Cbw) this_t;
    pyhdl_uvm_object_type clstype;
    pyhdl_uvm_object_type basetype;

    static this_t prv_inst;

    function new(string classname, string basename);
        clstype = pyhdl_uvm_object_type_p #(Ct,Ctw)::inst(classname);
        basetype = pyhdl_uvm_object_type_p #(Cb,Cbw)::inst(basename);
    endfunction

    static function pyhdl_uvm_object_type_rgy inst(
        string classname,
        string basename);
        if (prv_inst != null) begin
            `PYHDL_IF_FATAL(("multiple registration"))
        end
        prv_inst = new(classname, basename);
        if (prv_inst.clstype != prv_inst.basetype) begin
            // Build the type tree
            prv_inst.basetype.subtypes.push_back(prv_inst.clstype);
        end
        return prv_inst;
    endfunction

endclass

class pyhdl_uvm_object_rgy extends uvm_object_rgy_imp_impl #(pyhdl_uvm_object_rgy);
    static pyhdl_uvm_object_rgy    m_inst;
    uvm_object_rgy_exp_impl        m_exp;
    pyhdl_uvm_object_if            m_obj_rgy[PyObject];
    uvm_object                     m_obj_m[PyObject];
    pyhdl_uvm_object_type          m_type2factory_m[uvm_object_wrapper];
    PyObject                       m_type2type_m[pyhdl_uvm_object_type];
    pyhdl_uvm_object_type          m_clstype_root;

    function new();
        super.new(this);
        m_exp = new(m_obj);
        m_clstype_root = pyhdl_uvm_object_type_p #(uvm_object,pyhdl_uvm_object_w)::inst("uvm_object");
    endfunction

    function PyObject wrap(uvm_object obj);
        PyObject obj_t;
        uvm_object_wrapper uvm_obj_t = obj.get_object_type();
        pyhdl_uvm_object_if obj_if;

        if (obj == null) begin
            return None;
        end 

        if (uvm_obj_t == null || !m_type2factory_m.exists(uvm_obj_t)) begin
            // Create a new object type
            obj_if = create_object_type(obj);

        end else begin
            pyhdl_uvm_object_type pyhdl_obj_t;
            PyObject obj_t;

            pyhdl_obj_t = m_type2factory_m[uvm_obj_t];
            obj_t = m_type2type_m[pyhdl_obj_t];

            obj_if = pyhdl_obj_t.create(obj);

            if (obj_if == null) begin
                `PYHDL_IF_FATAL(("failed to create wrapper from previously-registered type %0s",
                    pyhdl_obj_t.name))
            end

            if (PyObject_SetAttrString(obj_if.get_pyobject(), "_uvm_obj_t", obj_t) != 0) begin
                PyErr_Print();
            end
        end

        if (obj_if == null) begin
            `PYHDL_IF_FATAL(("failed to create a wrapper for UVM object %0s (%0s)",
                obj.get_name(), obj.get_type_name()))
        end

        m_obj_rgy[obj_if.get_pyobject()] = obj_if;

        return obj_if.get_pyobject();
    endfunction

    function void register_object(uvm_object obj, PyObject pyobj);
        m_obj_m[pyobj] = obj;
    endfunction

    function uvm_object get_object(PyObject obj);
        uvm_object ret;
        if (m_obj_rgy.exists(obj)) begin
            pyhdl_uvm_object_if obj_if = m_obj_rgy[obj];
            ret = obj_if.get_object();
        end else if (m_obj_m.exists(obj)) begin
            ret = m_obj_m[obj];
        end else begin
            `PYHDL_IF_FATAL(("Object is not registered"))
            `STACKTRACE;
        end
        return ret;
    endfunction

    function pyhdl_uvm_object_if create_object_type(uvm_object obj);
        uvm_component comp;
        uvm_sequence_base seq;
        uvm_sequence_item seq_item;
        uvm_reg_field reg_field;
        pyhdl_uvm_wrapper_factory factory;
        py_object py_obj_t;
        pyhdl_uvm_object_if obj_if;
        pyhdl_uvm_object_type pyhdl_obj_t;
        string                pyhdl_super_t;
        pyhdl_uvm_object_type subtypes[$];
        uvm_object_wrapper obj_t = obj.get_object_type();

        py_gil_enter();

        if (!m_clstype_root.issubclass(obj)) begin
            `PYHDL_IF_FATAL(("obj must always be a subclass of base"))
        end
        pyhdl_obj_t = m_clstype_root;

        foreach (pyhdl_obj_t.subtypes[i]) begin
            `PYHDL_IF_DEBUG(("Subtype: %0s", pyhdl_obj_t.subtypes[i].name))
        end

        while (pyhdl_obj_t.subtype_subclasses(subtypes, obj) == 1) begin
            pyhdl_super_t = pyhdl_obj_t.name;
            pyhdl_obj_t = subtypes[0];
            `PYHDL_IF_DEBUG(("Found: %0s", pyhdl_obj_t.name))
        end

        if (subtypes.size() > 0) begin
            `PYHDL_IF_FATAL(("found multiple matches"))
        end

        if (pyhdl_obj_t == null) begin
            `PYHDL_IF_FATAL(("Failed to find a type for object %0s (%0s)",
                obj.get_name(), obj.get_type_name()))
        end else begin
//            `PYHDL_IF_DEBUG(("Found type %0s", pyhdl_obj_t.name))
        end

        `PYHDL_IF_DEBUG(("obj.type: %0s ; pyhdl_obj_t: %0s", obj.get_type_name(), pyhdl_obj_t.name))

        m_type2factory_m[obj_t] = pyhdl_obj_t;

        obj_if = pyhdl_obj_t.create(obj);

        if (obj_if == null) begin
            `PYHDL_IF_FATAL(("type %0s returned a null obj_if", pyhdl_obj_t.name))
        end

        py_obj_t = py_object::mk(m_exp.mk(obj_if.get_pyobject()));
        m_type2type_m[pyhdl_obj_t] = py_obj_t.steal();

        void'(PyObject_SetAttrString(
            obj_if.get_pyobject(), "_uvm_obj_t", py_obj_t.borrow()));

        py_gil_leave();

        return obj_if;
    endfunction

    function void drop(PyObject obj);

    endfunction

    function PyObject clp();
        return pyhdl_uvm_object_rgy::inst().wrap(
            uvm_cmdline_processor::get_inst()
        );
    endfunction

    virtual function string _get_type_dump();
        factory_print_catcher catcher = new;
        uvm_factory factory = uvm_factory::get();

        // Attach our custom report catcher so we can 
        // save the message printed by factory.print()
        uvm_report_cb::add(null, catcher);

        factory.print();

        uvm_report_cb::delete(null, catcher);

        return catcher.factory_print;
    endfunction

    virtual function PyObject create_by_name(string name);
        uvm_factory factory = uvm_factory::get();
        uvm_object obj;
        uvm_component comp;
        `PYHDL_IF_DEBUG(("name: %0s", name))
        obj = factory.create_object_by_name(name);
        if (obj == null) begin
            uvm_phase phase = new();
            comp = factory.create_component_by_name(name, "", "", null);
            comp.build_phase(phase);
            `PYHDL_IF_DEBUG(("comp: %0p", comp))
            obj = comp;
        end
        return pyhdl_uvm_object_rgy::inst().wrap(obj);
    endfunction

    static function pyhdl_uvm_object_rgy inst();
        if (m_inst == null) begin
            m_inst = new();
        end
        return m_inst;
    endfunction

endclass

