/**
 * pyhdl_uvm_analysis_port.svh
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
typedef class pyhdl_uvm_object_rgy;
typedef class pyhdl_uvm_component_w;

/**
 * Fans an analysis-port write out to Python listeners.
 *
 * Holds the Python callables registered against one analysis port. Each
 * #write wraps the transaction once and calls every listener with it. With no
 * listeners registered the write is skipped entirely, so an unobserved port
 * costs nothing.
 *
 * Instantiated by #pyhdl_uvm_analysis_port and #pyhdl_uvm_analysis_imp rather
 * than directly.
 *
 * @see pyhdl_uvm_analysis_port
 * @see pyhdl_uvm_analysis_imp
 */
class uvm_analysis_port_proxy extends uvm_component;
    `uvm_component_utils(uvm_analysis_port_proxy)
    /// Registered Python callables, each holding a reference.
    PyObject            listeners[$];

    /**
     * @param name Leaf name of the component.
     * @param parent Parent component.
     */
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    /**
     * Handle the connect phase.
     *
     * Nothing to do -- listeners register at run time through #add_listener.
     *
     * @param phase The connect phase object.
     */
    function void connect_phase(uvm_phase phase);
    endfunction

    /**
     * Deliver a transaction to every registered listener.
     *
     * Acquires the GIL, wraps the transaction once, and calls each listener
     * with it. A listener that raises has its traceback printed; the
     * remaining listeners still run.
     *
     * @param t The transaction to publish.
     */
    function void write(uvm_object t);
        if (listeners.size() > 0) begin
            // Only wrap the object if there are listeners waiting
            PyObject obj = pyhdl_uvm_object_rgy::inst().wrap(t);
            PyGILState_STATE state;

            state = PyGILState_Ensure();

            Py_IncRef(obj);
            foreach (listeners[i]) begin
                // Call each of the listeners in turn
                PyObject args = PyTuple_New(1);
                PyObject ret;
                void'(PyTuple_SetItem(args, 0, obj));
                ret = PyObject_Call(listeners[i], args, null);
                if (ret == null) begin
                    PyErr_Print();
                end
            end
            Py_DecRef(obj);

            PyGILState_Release(state);
        end
    endfunction

    /**
     * Register a Python callable to receive writes.
     *
     * @param l The callable, invoked with the wrapped transaction. A
     *        reference is taken and held for the port's lifetime.
     */
    virtual function void add_listener(PyObject l);
        Py_IncRef(l);
        listeners.push_back(l);
    endfunction

endclass

/**
 * Exposes an #uvm_analysis_port_proxy to Python.
 *
 * The Python-side wrapper: `connect`-ing a listener from Python arrives here
 * and is forwarded to the wrapped component.
 *
 * @see uvm_analysis_port_proxy
 */
class pyhdl_uvm_analysis_port_proxy extends pyhdl_uvm_component;
    /**
     * @param obj The `uvm_analysis_port_proxy` to wrap.
     */
    function new(uvm_object obj);
        super.new(obj);
    endfunction

    /**
     * Register a Python callable against the wrapped port.
     *
     * @param l The callable to register.
     */
    virtual function void add_listener(PyObject l);
        uvm_analysis_port_proxy p;
        $cast(p, m_uvm_obj);
        p.add_listener(l);
    endfunction

endclass
`pyhdl_uvm_type_utils(uvm_analysis_port_proxy, pyhdl_uvm_analysis_port_proxy, uvm_component, pyhdl_uvm_component)

/**
 * A `uvm_subscriber` whose writes are observable from Python.
 *
 * Connect this to any analysis port to let Python observe the traffic:
 * register listeners on its #proxy.
 *
 * @param T Transaction type.
 *
 * @see pyhdl_uvm_analysis_port
 */
class pyhdl_uvm_analysis_imp #(type T=int) extends uvm_subscriber #(T);
    typedef pyhdl_uvm_analysis_imp #(T) this_t;
    `uvm_component_param_utils(this_t);

    /// Fans writes out to the registered Python listeners.
    uvm_analysis_port_proxy           proxy;

    /**
     * @param name Leaf name of the component.
     * @param parent Parent component.
     */
    function new(string name, uvm_component parent);
        super.new(name, parent);
        proxy = new("proxy", this);
    endfunction

    /**
     * Receive a transaction and publish it to Python.
     *
     * @param t The transaction written to this subscriber.
     */
    virtual function void write(T t);
        proxy.write(t);
    endfunction

endclass

/**
 * A `uvm_analysis_port` whose writes are also visible to Python.
 *
 * Drop-in replacement for `uvm_analysis_port`: writes still reach every
 * connected SystemVerilog subscriber, and additionally reach any Python
 * listeners registered on #proxy.
 *
 * @param T Transaction type.
 *
 * @see pyhdl_uvm_analysis_imp
 */
class pyhdl_uvm_analysis_port #(type T=int) extends uvm_analysis_port #(T);
    /// Fans writes out to the registered Python listeners.
    uvm_analysis_port_proxy proxy;

    /**
     * @param name Leaf name of the port.
     * @param parent Component the port belongs to.
     */
    function new(string name, uvm_component parent);
        super.new(name, parent);
        proxy = new("proxy", m_comp);
    endfunction

    /**
     * Publish a transaction to SystemVerilog subscribers and Python listeners.
     *
     * @param t The transaction to publish.
     */
    function void write(T t);
        super.write(t);
        proxy.write(t);
    endfunction

endclass

/**
 * Adapter delivering analysis writes to a single Python callable.
 *
 * @param T Transaction type.
 *
 * @warning Unfinished -- #write is an empty stub, so nothing is delivered.
 *          The working route is #pyhdl_uvm_analysis_port or
 *          #pyhdl_uvm_analysis_imp, whose listeners are called through
 *          #uvm_analysis_port_proxy.
 */
class pyhdl_uvm_subscriber #(type T=int) extends uvm_tlm_if_base #(T,T);
    typedef pyhdl_uvm_subscriber #(T) this_t;
    /// The Python callable to deliver to.
    PyObject            m_listener;

    /**
     * @param listener The Python callable to deliver transactions to.
     */
    function new(PyObject listener);
        m_listener = listener;
    endfunction

    /**
     * Deliver a transaction to the listener.
     *
     * @param t The transaction.
     * @warning Not implemented -- the body is empty.
     */
    virtual function void write(input T t);
        // Handle various possibilities for the type

        // 
    endfunction
endclass

/**
 * Wrapper object for a particular analysis-port specialization.
 *
 * Note: this is a Python-side wrapper (a `pyhdl_uvm_object` subclass holding
 * `m_uvm_obj`), not an analysis port itself.  It extends
 * `pyhdl_uvm_analysis_port_proxy`, *not* the similarly-named
 * `pyhdl_uvm_analysis_port`, which is the UVM-side port.
 */
class pyhdl_uvm_analysis_port_ap #(type T) extends pyhdl_uvm_analysis_port_proxy;
    typedef pyhdl_uvm_analysis_port_ap #(T) this_t;

    function new(uvm_object obj);
        super.new(obj);
    endfunction

    /**
     * Register a Python listener against this port specialization.
     *
     * @param listener The Python callable to register.
     * @warning Unfinished -- the subscriber is constructed but never bound,
     *          so the listener is not called. @see pyhdl_uvm_subscriber
     */
    virtual function void connect(PyObject listener);
        uvm_component comp;
        pyhdl_uvm_subscriber #(T) subscriber;

        $cast(comp, m_uvm_obj);

        // Create a subscriber
        // TODO: the subscriber is constructed but not yet bound to `comp`'s
        // analysis port -- pyhdl_uvm_subscriber::write is still a stub.
        subscriber = new(listener);

    endfunction

endclass


