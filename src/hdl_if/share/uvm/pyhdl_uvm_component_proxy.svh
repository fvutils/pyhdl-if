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
 * Hosts a UVM component implemented in Python.
 *
 * Instantiate this in place of the component you want written in Python, set
 * #pyclass to name the implementation, and the proxy imports the module,
 * constructs the class, and forwards each phase to it::
 *
 *     pyhdl_uvm_component_proxy m_pycomp;
 *
 *     function void build_phase(uvm_phase phase);
 *         super.build_phase(phase);
 *         m_pycomp = pyhdl_uvm_component_proxy::type_id::create("m_pycomp", this);
 *         m_pycomp.pyclass = "pycomp::PyComp";
 *     endfunction
 *
 * The Python class subclasses `hdl_if.uvm.uvm_component_impl` and receives
 * this proxy as `self.proxy`.
 *
 * @see pyhdl_uvm_sequence_proxy
 * @see pyhdl_uvm_component_proxy_helper
 */
class pyhdl_uvm_component_proxy extends uvm_component;
    `uvm_component_utils(pyhdl_uvm_component_proxy)

    /**
     * The Python class to construct, as `module::Class` or `module:Class`.
     *
     * Must be set before #build_phase runs -- from the parent's build phase,
     * or from a configuration setting. An empty or malformed value, or a
     * module or class that cannot be imported, is fatal.
     */
    string                              pyclass;

    /// Bridge carrying calls between this proxy and the Python object.
    pyhdl_uvm_component_proxy_helper    m_helper;

    /**
     * @param name Leaf name of the component.
     * @param parent Parent component.
     */
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction



    /**
     * Import #pyclass, construct it, and run the Python build phase.
     *
     * @param phase The build phase object.
     */
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

    /**
     * Forward the connect phase to the Python implementation.
     *
     * @param phase The connect phase object.
     */
    function void connect_phase(uvm_phase phase);
        PyObject __ph = pyhdl_uvm_object_rgy::inst().wrap(phase);
        m_helper.m_exp.connect_phase(__ph);
    endfunction

    /**
     * Start the Python task scheduler and run the Python run phase.
     *
     * The phase does not complete until the Python coroutine returns.
     *
     * @param phase The run phase object.
     */
    task run_phase(uvm_phase phase);
        PyObject __ph = pyhdl_uvm_object_rgy::inst().wrap(phase);
        // Ensure that the task scheduler is running
        pyhdl_if_start();

        m_helper.m_exp.run_phase(__ph);
    endtask

endclass


/**
 * Bridge between #pyhdl_uvm_component_proxy and its Python implementation.
 *
 * Implements the component API Python calls into, forwarding each method to
 * the hosted `uvm_component`, and holds the export used to call the Python
 * implementation back. Constructed by the proxy during its build phase; not
 * instantiated directly.
 *
 * @see pyhdl_uvm_component_proxy
 */
class pyhdl_uvm_component_proxy_helper
    extends uvm_component_proxy_imp_impl #(pyhdl_uvm_component_proxy_helper);
    /// The hosting proxy component.
    pyhdl_uvm_component_proxy       m_proxy;
    /// Export used to invoke the Python implementation.
    uvm_component_proxy_exp_impl    m_exp;

    /**
     * Construct the Python implementation and bind it to the proxy.
     *
     * @param impl The hosting proxy component.
     * @param clsname The `module::Class` string, used in error messages.
     * @param cls The imported Python class object to instantiate.
     */
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

    /**
     * Reseed the component's random number generator.
     *
     * @warning Not implemented -- the body is empty and the call does nothing.
     */
    virtual function void reseed();
        m_proxy.reseed();
    endfunction

    /**
     * Set the component's leaf name.
     *
     * @param name The new leaf name.
     */
    virtual function void set_name(string name);
        m_proxy.set_name(name);
    endfunction

    /// @return The component's unique instance id.
    virtual function int get_inst_id();
        return m_proxy.get_inst_id();
    endfunction

    /// @return The number of `uvm_object` instances created so far.
    virtual function int get_inst_count();
        return m_proxy.get_inst_count();
    endfunction

    /// @return The component's registered type name.
    virtual function string get_type_name();
        return m_proxy.get_type_name();
    endfunction

    /// @return A new object of the component's type, wrapped for Python.
    virtual function PyObject create();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.create());
    endfunction

    /// @return A copy of the component, wrapped for Python.
    virtual function PyObject clone();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.clone());
    endfunction

    /// Print the component's fields through the UVM printer.
    virtual function void print();
        m_proxy.print();
    endfunction

    /// @return The component's single-line string form.
    virtual function string convert2string();
        return m_proxy.convert2string();
    endfunction

    /// Record the component's fields to the transaction database.
    virtual function void record();
        m_proxy.record();
    endfunction

    /**
     * Copy field values from another object into this component.
     *
     * @param rhs The Python-side object to copy from.
     */
    virtual function void copy(PyObject rhs);
        m_proxy.copy(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction

    /**
     * Compare this component's fields against another object's.
     *
     * @param rhs The Python-side object to compare against.
     * @return 1 if they compare equal.
     */
    virtual function bit compare(PyObject rhs);
        return m_proxy.compare(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction

    /**
     * Set an integral field by name.
     *
     * @param name The field name.
     * @param value The value to assign.
     *
     * @warning Not implemented -- the body is disabled and the call does
     *          nothing. `set_*_local` came from the UVM-1.1 `uvm_field_*`
     *          macros and is not a member of `uvm_object` under IEEE 1800.2.
     */
    virtual function void set_int_local(string name, int value);
//        m_proxy.set_int_local(name, value);
    endfunction

    /**
     * Set a string field by name.
     *
     * @param name The field name.
     * @param value The value to assign.
     *
     * @warning Not implemented. @see set_int_local
     */
    virtual function void set_string_local(string name, string value);
//        m_proxy.set_string_local(name, value);
    endfunction

    /**
     * Set a object field by name.
     *
     * @param name The field name.
     * @param value The value to assign.
     *
     * @warning Not implemented. @see set_int_local
     */
    virtual function void set_object_local(string name, PyObject value);
//        m_proxy.set_object_local(name, pyhdl_uvm_object_rgy::inst().get_object(value));
    endfunction

    /**
     * Look up an object in the UVM configuration database.
     *
     * @param name The configuration field name.
     * @param clone Whether to return a copy rather than the stored object.
     * @return A Python tuple of (found, object).
     * @warning Not implemented -- the `uvm_config_db` lookup is commented out,
     *          so this always reports not-found and returns (False, None).
     */
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

    /**
     * List the component's children.
     *
     * @return A Python list of the child components, each wrapped.
     */
    virtual function PyObject get_children();
        py_list ret = new();
        uvm_component c[$];

        m_proxy.get_children(c);
        foreach (c[i]) begin
            ret.append_obj(pyhdl_uvm_object_rgy::inst().wrap(c[i]));
        end

        return ret.borrow();
    endfunction

    /**
     * Randomize the component.
     *
     * @return 1 if randomization succeeded.
     */
    virtual function bit _randomize();
        return m_proxy.randomize();
    endfunction

    /**
     * Return the UVM factory.
     *
     * @return Always null.
     * @warning Not implemented. Create through #create_object and
     *          #create_component instead, which do go through the factory.
     */
    virtual function PyObject get_factory();
        return null;
    endfunction

    /**
     * Report an informational message.
     *
     * @param msg The message text.
     * @warning Not implemented -- the body is empty and the message is
     *          discarded. Use the UVM reporting macros on the SystemVerilog
     *          side, or `print` from Python.
     */
    virtual function void info(string msg);
    endfunction

    /// @return The component's parent, wrapped for Python.
    virtual function PyObject get_parent();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.get_parent());
    endfunction

    /// @return The formatted field dump that #print would emit.
    virtual function string sprint();
        return m_proxy.sprint();
    endfunction

    /// @return The component's leaf name.
    virtual function string get_name();
        return m_proxy.get_name();
    endfunction

    /// @return The component's full hierarchical path.
    virtual function string get_full_name();
        return m_proxy.get_full_name();
    endfunction

    /**
     * Pack the component's fields into a Python list of integers.
     *
     * @warning Not implemented -- the body is empty and the return value is
     *          unset. Components are not usually packed; see
     *          `pyhdl_uvm_object::pack_ints` for objects.
     */
    virtual function PyObject pack_ints();
    endfunction

    /**
     * Populate the component's fields from a Python list of integers.
     *
     * @param data The packed field values.
     * @warning Not implemented -- the body is empty. @see pack_ints
     */
    virtual function void unpack_ints(PyObject data);
    endfunction

    /**
     * Create an object through the UVM factory.
     *
     * @param requested_type_name The registered type name to create.
     * @param name Leaf name for the new object.
     * @return The new object wrapped for Python, or Python `None` if the
     *         type is not registered.
     */
    virtual function PyObject create_object(string requested_type_name, string name="");
        uvm_object obj;

        obj = m_proxy.create_object(requested_type_name, name);

        if (obj != null) begin
            return pyhdl_uvm_object_rgy::inst().wrap(obj);
        end else begin
            return None;
        end
    endfunction

    /**
     * Create a child component through the UVM factory.
     *
     * @param requested_type_name The registered type name to create.
     * @param name Leaf name for the new component.
     * @return The new component wrapped for Python, or Python `None` if the
     *         type is not registered.
     */
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
