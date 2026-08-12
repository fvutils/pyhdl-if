/**
 * pyhdl_uvm_object.svh
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

typedef class pyhdl_uvm_object_rgy;

typedef interface class pyhdl_uvm_object_if;

/**
 * Exposes a `uvm_object` to Python.
 *
 * Wraps one `uvm_object` and forwards the parts of its API that Python needs.
 * Instances are created by the object registry as objects cross the boundary
 * -- a sequence item handed to a Python sequence body, for example -- rather
 * than constructed directly, and appear on the Python side as
 * `hdl_if.uvm.uvm_object`.
 *
 * Field access goes through #pack_ints and #unpack_ints. The `set_*_local`
 * methods are present but do nothing; see #set_int_local.
 *
 * @see pyhdl_uvm_component_proxy
 * @see pyhdl_uvm_sequence_proxy
 */
class pyhdl_uvm_object;
    /// The wrapped UVM object.
    uvm_object      m_uvm_obj;

    /**
     * Wrap a UVM object.
     *
     * @param obj The object to expose to Python.
     */
    function new(uvm_object obj);
        m_uvm_obj = obj;
    endfunction

    /// @return The wrapped object's registered type name.
    virtual function string get_type_name();
        return m_uvm_obj .get_type_name();
    endfunction

    /**
     * Randomize the wrapped object, honoring its SystemVerilog constraints.
     *
     * @return 1 if randomization succeeded.
     */
    virtual function bit _randomize();
        return m_uvm_obj .randomize();
    endfunction

    /// @return The wrapped object's leaf name.
    virtual function string get_name();
        return m_uvm_obj .get_name();
    endfunction

    /// @return The formatted field dump that #print would emit.
    virtual function string sprint();
        return m_uvm_obj .sprint();
    endfunction

    /// @return The wrapped object's full hierarchical name.
    virtual function string get_full_name();
        return m_uvm_obj .get_full_name();
    endfunction

    /**
     * Construct a new object of the wrapped object's type.
     *
     * @param name Leaf name for the new object.
     * @return The new object, wrapped for Python. Fields are at their
     *         defaults -- use #clone to copy them.
     */
    virtual function PyObject create(string name="");
        return pyhdl_uvm_object_rgy::inst().wrap(m_uvm_obj .create(name));
    endfunction

    /// Print the wrapped object's fields through the UVM printer.
    virtual function void print();
        m_uvm_obj .print();
    endfunction

    /// @return The wrapped object's single-line string form.
    virtual function string convert2string();
        return m_uvm_obj .convert2string();
    endfunction

    /// Record the wrapped object's fields to the transaction database.
    virtual function void record();
        m_uvm_obj .record();
    endfunction

    /**
     * Copy field values from another object into the wrapped one.
     *
     * @param rhs The Python-side object to copy from.
     */
    virtual function void copy(PyObject rhs);
        m_uvm_obj .copy(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction

    /**
     * Set an integral field by name.
     *
     * @param name The field name.
     * @param value The value to assign.
     *
     * @warning Not implemented -- the body is disabled and the call does
     *          nothing. `set_*_local` was generated on `uvm_object` by the
     *          UVM-1.1 `uvm_field_*` macros and is not a member under IEEE
     *          1800.2, which replaced it with `uvm_object::set_local`. Use
     *          #pack_ints and #unpack_ints instead.
     */
    virtual function void set_int_local(string name, longint unsigned value);
//        m_uvm_obj .set_int_local(name, value);
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
//        m_uvm_obj .set_string_local(name, value);
    endfunction

    /**
     * Set an object field by name.
     *
     * @param name The field name.
     * @param value The Python-side object to assign.
     *
     * @warning Not implemented. @see set_int_local
     */
    virtual function void set_object_local(string name, PyObject value);
//        m_uvm_obj .set_object_local(name, pyhdl_uvm_object_rgy::inst().get_object(value));
    endfunction

    /**
     * Compare the wrapped object's fields against another's.
     *
     * @param rhs The Python-side object to compare against.
     * @return 1 if the objects compare equal.
     */
    virtual function bit compare(PyObject rhs);
        return m_uvm_obj .compare(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction


    /// @return A copy of the wrapped object, fields included, wrapped for Python.
    virtual function PyObject clone();
        return pyhdl_uvm_object_rgy::inst().wrap(m_uvm_obj .clone());
    endfunction

    /// @return The wrapped `uvm_object` itself, for SystemVerilog-side use.
    virtual function uvm_object get_object();
        return m_uvm_obj;
    endfunction

    /**
     * Pack the wrapped object's fields into a Python list of integers.
     *
     * This and #unpack_ints are the supported route for reading and writing
     * fields from Python: pack, modify the list, unpack.
     *
     * @return A Python list of 32-bit words.
     */
    virtual function PyObject pack_ints();
        py_list ret = new();
        int unsigned data[];
        void'(m_uvm_obj .pack_ints(data));
        foreach (data[i]) begin
            ret.append(py_from_int(data[i]));
        end
        return ret.borrow();
    endfunction

    /**
     * Populate the wrapped object's fields from a Python list of integers.
     *
     * @param data A Python list of the shape #pack_ints returns.
     */
    virtual function void unpack_ints(PyObject data);
        py_list dl = new(data);
        int unsigned data_arr[] = new[dl.size()];
        foreach (data_arr[i]) begin
            data_arr[i] = dl.get_item(i).as_int();
        end
        void'(m_uvm_obj .unpack_ints(data_arr));
    endfunction

    /// Reseed the wrapped object's random number generator.
    virtual function void reseed();
        m_uvm_obj .reseed();
    endfunction

    /**
     * Set the wrapped object's leaf name.
     *
     * @param name The new leaf name.
     */
    virtual function void set_name(string name);
        m_uvm_obj .set_name(name);
    endfunction

    /// @return The wrapped object's unique instance id.
    virtual function longint unsigned get_inst_id();
        return m_uvm_obj .get_inst_id();
    endfunction

    /// @return The number of `uvm_object` instances created so far.
    virtual function longint unsigned get_inst_count();
        return m_uvm_obj .get_inst_count();
    endfunction

endclass

`pyhdl_uvm_type_utils(uvm_object, pyhdl_uvm_object, uvm_object, pyhdl_uvm_object)

