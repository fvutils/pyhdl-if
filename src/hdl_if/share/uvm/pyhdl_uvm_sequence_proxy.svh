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

/**
 * Grants access to a sequence's sequencer without knowing its parameters.
 *
 * #pyhdl_uvm_sequence_proxy is parameterized, so the helper cannot hold a
 * typed handle to it. This interface exposes the one method the helper needs.
 */
interface class pyhdl_uvm_sequence_proxy_if;
    /// @return The sequencer this sequence is running on.
    pure virtual function uvm_sequencer_base _get_sequencer();
endclass

/**
 * Hosts a UVM sequence whose body is written in Python.
 *
 * Start this in place of the sequence you want written in Python. On
 * #body it imports the class named by #pyclass, constructs it, and awaits its
 * Python `body()` coroutine. Name the class either as a parameter::
 *
 *     typedef pyhdl_uvm_sequence_proxy #(
 *       .REQ(seq_item),
 *       .PyClass("pyseq:PyRandSeq")) py_seq_t;
 *
 * or by assigning #pyclass after construction::
 *
 *     py_seq_t seq = py_seq_t::type_id::create("seq");
 *     seq.pyclass = "pyseq::PyRandSeq";
 *     seq.start(m_env.m_seqr);
 *
 * The Python class subclasses `hdl_if.uvm.uvm_sequence_impl` and drives items
 * through `self.proxy`.
 *
 * @param REQ Request item type.
 * @param RSP Response item type. Defaults to REQ.
 * @param UserDataT Type of the optional #userdata object.
 * @param PyClass Default value for #pyclass.
 *
 * @see pyhdl_uvm_component_proxy
 * @see pyhdl_uvm_sequence_proxy_helper
 */
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

    /**
     * The Python class to construct, as `module::Class` or `module:Class`.
     *
     * Defaults to the `PyClass` parameter. Must be non-empty and resolvable
     * by the time #body runs; anything else is fatal.
     */
    string      pyclass = PyClass;

    /// Optional object passed through to the Python implementation.
    UserDataT   userdata;

    /// Bridge carrying calls between this sequence and the Python object.
    helper_t    m_helper;

    /**
     * @param name Leaf name of the sequence.
     */
    function new(string name="pyhdl_uvm_sequence_proxy");
        super.new(name);
    endfunction

    /// @return The #userdata object, or null if none was set.
    virtual function uvm_object get_userdata();
        return userdata;
    endfunction

    /// @return The sequencer this sequence is running on.
    virtual function uvm_sequencer_base _get_sequencer();
        return m_sequencer;
    endfunction

    /**
     * Import #pyclass, construct it, and run its Python `body()`.
     *
     * Starts the Python task scheduler first. The task does not return until
     * the Python coroutine completes. A missing, malformed or unresolvable
     * #pyclass is fatal.
     */
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

/**
 * Bridge between #pyhdl_uvm_sequence_proxy and its Python implementation.
 *
 * Implements the sequence API Python calls into -- item creation and the UVM
 * handshake -- and holds the export used to call the Python body. Constructed
 * by the proxy; not instantiated directly. This is what a Python sequence
 * sees as `self.proxy`.
 *
 * @param REQ Request item type.
 * @param RSP Response item type.
 *
 * @see pyhdl_uvm_sequence_proxy
 */
class pyhdl_uvm_sequence_proxy_helper #(type REQ=uvm_sequence_item, type RSP=REQ)
        extends uvm_sequence_proxy_imp_impl #(pyhdl_uvm_sequence_proxy_helper #(REQ,REQ))
        implements pyhdl_uvm_object_if;
    /// The hosting sequence.
    uvm_sequence_base               m_proxy;
    /// Export used to invoke the Python implementation.
    uvm_sequence_proxy_exp_impl     m_exp;
    /// The sequence's user-data object, if any.
    uvm_object                      m_userdata;

    /**
     * Construct the Python implementation and bind it to the sequence.
     *
     * @param clsname The `module::Class` string, used in error messages.
     * @param cls The imported Python class object to instantiate.
     */
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

    /// @return The hosting sequence as a `uvm_object`.
    virtual function uvm_object get_object();
        return m_proxy;
    endfunction

    /// @return The Python object bound to the hosting sequence.
    virtual function PyObject get_pyobject();
        return m_obj;
    endfunction

    /// @return The sequence's leaf name.
    virtual function string get_name();
        `PYHDL_IF_DEBUG(("get_name"))
        return m_proxy.get_name();
    endfunction

    /// Reseed the sequence's random number generator.
    virtual function void reseed();
        m_proxy.reseed();
    endfunction

    /**
     * Set the sequence's leaf name.
     *
     * @param name The new leaf name.
     */
    virtual function void set_name(string name);
        m_proxy.set_name(name);
    endfunction

    /// @return The sequence's unique instance id.
    virtual function int get_inst_id();
        return m_proxy.get_inst_id();
    endfunction

    /// @return The number of `uvm_object` instances created so far.
    virtual function int get_inst_count();
        return m_proxy.get_inst_count();
    endfunction

    /// @return The sequence's registered type name.
    virtual function string get_type_name();
        return m_proxy.get_type_name();
    endfunction

    /// @return A new object of the sequence's type, wrapped for Python.
    virtual function PyObject create();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.create());
    endfunction

    /// @return A copy of the sequence, wrapped for Python.
    virtual function PyObject clone();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.clone());
    endfunction

    /// Print the sequence's fields through the UVM printer.
    virtual function void print();
        m_proxy.print();
    endfunction

    /// @return The sequence's single-line string form.
    virtual function string convert2string();
        return m_proxy.convert2string();
    endfunction

    /// Record the sequence's fields to the transaction database.
    virtual function void record();
        m_proxy.record();
    endfunction

    /**
     * Copy field values from another object into the sequence.
     *
     * @param rhs The Python-side object to copy from.
     */
    virtual function void copy(PyObject rhs);
        m_proxy.copy(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction

    /**
     * Compare the sequence's fields against another object's.
     *
     * @param rhs The Python-side object to compare against.
     * @return 1 if they compare equal.
     */
    virtual function bit compare(PyObject rhs);
        return m_proxy.compare(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction

    // set_*_local were generated on uvm_object by the UVM-1.1 `uvm_field_*
    // macros and are not members of uvm_object under IEEE 1800.2, which
    // replaced them with uvm_object::set_local(uvm_resource_base).  The bodies
    // are disabled here to match pyhdl_uvm_object.svh and
    // pyhdl_uvm_component_proxy.svh, where the same change was already made.
    virtual function void set_int_local(string name, int value);
//        m_proxy.set_int_local(name, value);
    endfunction

    virtual function void set_string_local(string name, string value);
//        m_proxy.set_string_local(name, value);
    endfunction

    virtual function void set_object_local(string name, PyObject value);
//        m_proxy.set_object_local(name, pyhdl_uvm_object_rgy::inst().get_object(value));
    endfunction

    /// @return The sequencer this sequence is running on, wrapped for Python.
    virtual function PyObject _get_sequencer();
        pyhdl_uvm_sequence_proxy_if proxy;
        $cast (proxy, m_proxy);
        `PYHDL_IF_DEBUG(("-- _get_sequencer"))
        return pyhdl_uvm_object_rgy::inst().wrap(proxy._get_sequencer());
    endfunction

    /**
     * Return the sequence's user-data object.
     *
     * @return The object wrapped for Python, or Python `None` if none was set.
     */
    virtual function PyObject get_userdata();
        if (m_userdata != null) begin
            return pyhdl_uvm_object_rgy::inst().wrap(m_userdata);
        end else begin
            return None;
        end
    endfunction

    /**
     * Create a request item of type `REQ` through the factory.
     *
     * @return The new item, wrapped for Python. Randomize or assign its
     *         fields, then pass it to #start_item.
     */
    virtual function PyObject create_req();
        REQ req = REQ::type_id::create();
        return pyhdl_uvm_object_rgy::inst().wrap(req);
    endfunction

    /**
     * Create a response item of type `RSP` through the factory.
     *
     * @return The new item, wrapped for Python.
     */
    virtual function PyObject create_rsp();
        RSP rsp = REQ::type_id::create();
        return pyhdl_uvm_object_rgy::inst().wrap(rsp);
    endfunction

    /**
     * Begin the UVM handshake for an item.
     *
     * Blocks until the sequencer grants access to the driver. Set the item's
     * fields after this returns and before #finish_item.
     *
     * @param item The Python-side item to send. Must wrap a
     *        `uvm_sequence_item`, or the call is fatal.
     */
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

    /**
     * Complete the UVM handshake for an item.
     *
     * Blocks until the driver signals it is done with the item.
     *
     * @param item The item passed to the matching #start_item. Must wrap a
     *        `uvm_sequence_item`, or the call is fatal.
     */
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