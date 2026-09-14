/**
 * pyhdl_uvm_wrapper_factory.svh
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

/**
 * The pair a wrapper factory returns: the SystemVerilog wrapper and its Python peer.
 *
 * SystemVerilog has no tuple, and both halves are needed at once -- the wrapper
 * to keep alive, the Python object to hand back across the boundary.
 */
class create_t;
    CallEmptyBase   first;
    PyObject        second;

    function new(CallEmptyBase first, PyObject second);
        this.first = first;
        this.second = second;
    endfunction
endclass


/**
 * Creates the wrapper that presents a UVM object to Python.
 *
 * One implementation exists per registered type, produced by the
 * `pyhdl_uvm_type_utils` macro. The registry looks the right one up by type
 * rather than switching on a name.
 *
 * @see pyhdl_uvm_wrapper_factory_t
 */
interface class pyhdl_uvm_wrapper_factory;

    pure virtual function create_t create(
        uvm_object      obj,
        PyObject        obj_t);
endclass

/**
 * The wrapper factory for one registered type pair.
 *
 * A singleton per parameterisation -- there is nothing per-instance to hold, and
 * the registry needs a stable handle to store.
 *
 * @param WrapperT The wrapper class to construct.
 * @param UvmObjT The UVM type it wraps. #create casts to this, so registering a
 *        mismatched pair fails at the cast rather than silently.
 */
class pyhdl_uvm_wrapper_factory_t #(type WrapperT, type UvmObjT=uvm_object) implements pyhdl_uvm_wrapper_factory;
    static pyhdl_uvm_wrapper_factory_t #(WrapperT, UvmObjT) m_inst;

    virtual function create_t create(uvm_object obj, PyObject obj_t);
        UvmObjT o;
        create_t ret;
        WrapperT wrapper;

        $cast(o, obj);
        wrapper = new(o);

        ret = new(wrapper, wrapper.m_obj);

        if (obj_t != null) begin
            void'(PyObject_SetAttrString(ret.second, "obj_t", obj_t));
        end

        return ret;
    endfunction

    static function pyhdl_uvm_wrapper_factory inst();
        if (m_inst == null) begin
            m_inst = new();
        end
        return m_inst;
    endfunction

endclass


