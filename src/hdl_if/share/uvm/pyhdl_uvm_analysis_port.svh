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

class uvm_analysis_port_proxy extends uvm_component;
    `uvm_component_utils(uvm_analysis_port_proxy)
    PyObject            listeners[$];

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    function void connect_phase(uvm_phase phase);
    endfunction

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

    virtual function void add_listener(PyObject l);
        Py_IncRef(l);
        listeners.push_back(l);
    endfunction

endclass

class pyhdl_uvm_analysis_port_proxy extends pyhdl_uvm_component;
    function new(uvm_object obj);
        super.new(obj);
    endfunction

    virtual function void add_listener(PyObject l);
        uvm_analysis_port_proxy p;
        $cast(p, m_uvm_obj);
        p.add_listener(l);
    endfunction

endclass
`pyhdl_uvm_type_utils(uvm_analysis_port_proxy, pyhdl_uvm_analysis_port_proxy, uvm_component, pyhdl_uvm_component)

class pyhdl_uvm_analysis_imp #(type T=int) extends uvm_subscriber #(T);
    typedef pyhdl_uvm_analysis_imp #(T) this_t;
    `uvm_component_param_utils(this_t);

    uvm_analysis_port_proxy           proxy;
    function new(string name, uvm_component parent);
        super.new(name, parent);
        proxy = new("proxy", this);
    endfunction

    virtual function void write(T t);
        proxy.write(t);
    endfunction

endclass

class pyhdl_uvm_analysis_port #(type T=int) extends uvm_analysis_port #(T);
    uvm_analysis_port_proxy proxy;

    function new(string name, uvm_component parent);
        super.new(name, parent);
        proxy = new("proxy", m_comp);
    endfunction

    function void write(T t);
        super.write(t);
        proxy.write(t);
    endfunction

endclass

class pyhdl_uvm_subscriber #(type T=int) extends uvm_tlm_if_base #(T,T);
    typedef pyhdl_uvm_subscriber #(T) this_t;
    PyObject            m_listener;

    function new(PyObject listener);
        m_listener = listener;
    endfunction

    virtual function void write(input T t);
        // Handle various possibilities for the type

        // 
    endfunction
endclass

/**
 * Wrapper object for a particular analysis-port specialization
 */
class pyhdl_uvm_analysis_port_ap #(type T) extends pyhdl_uvm_analysis_port;
    typedef pyhdl_uvm_analysis_port_ap #(T) this_t;

    function new(uvm_object obj);
        super.new(obj);
    endfunction

    virtual function void connect(PyObject listener);
        uvm_component comp;
        pyhdl_uvm_subscriber #(T) subscriber;

        $cast(comp, m_uvm_obj);

        // Create a subscriber 
        subscriber = new("", comp, listener);

    endfunction

endclass


