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
 * Accessor class for UVM objects. Exposes key UVM features to Python
 */
class pyhdl_uvm_object;
    uvm_object      m_uvm_obj;

    function new(uvm_object obj);
        m_uvm_obj = obj;
    endfunction

    virtual function string get_type_name();
        return m_uvm_obj .get_type_name();
    endfunction

    virtual function bit _randomize();
        return m_uvm_obj .randomize();
    endfunction

    virtual function string get_name();
        return m_uvm_obj .get_name();
    endfunction

    virtual function string sprint();
        return m_uvm_obj .sprint();
    endfunction

    virtual function string get_full_name();
        return m_uvm_obj .get_full_name();
    endfunction

    virtual function PyObject create(string name="");
        return pyhdl_uvm_object_rgy::inst().wrap(m_uvm_obj .create(name));
    endfunction

    virtual function void print();
        m_uvm_obj .print();
    endfunction

    virtual function string convert2string();
        return m_uvm_obj .convert2string();
    endfunction

    virtual function void record();
        m_uvm_obj .record();
    endfunction

    virtual function void copy(PyObject rhs);
        m_uvm_obj .copy(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction

    virtual function void set_int_local(string name, longint unsigned value);
//        m_uvm_obj .set_int_local(name, value);
    endfunction

    virtual function void set_string_local(string name, string value);
//        m_uvm_obj .set_string_local(name, value);
    endfunction

    virtual function void set_object_local(string name, PyObject value);
//        m_uvm_obj .set_object_local(name, pyhdl_uvm_object_rgy::inst().get_object(value));
    endfunction

    virtual function bit compare(PyObject rhs);
        return m_uvm_obj .compare(pyhdl_uvm_object_rgy::inst().get_object(rhs));
    endfunction


    virtual function PyObject clone();
        return pyhdl_uvm_object_rgy::inst().wrap(m_uvm_obj .clone());
    endfunction

    virtual function uvm_object get_object();
        return m_uvm_obj;
    endfunction

    virtual function PyObject pack_ints();
        py_list ret = new();
        int unsigned data[];
        void'(m_uvm_obj .pack_ints(data));
        foreach (data[i]) begin
            ret.append(py_from_int(data[i]));
        end
        return ret.borrow();
    endfunction

    virtual function void unpack_ints(PyObject data);
        py_list dl = new(data);
        int unsigned data_arr[] = new[dl.size()];
        foreach (data_arr[i]) begin
            data_arr[i] = dl.get_item(i).as_int();
        end
        void'(m_uvm_obj .unpack_ints(data_arr));
    endfunction

    virtual function void reseed();
        m_uvm_obj .reseed();
    endfunction

    virtual function void set_name(string name);
        m_uvm_obj .set_name(name);
    endfunction

    virtual function longint unsigned get_inst_id();
        return m_uvm_obj .get_inst_id();
    endfunction

    virtual function longint unsigned get_inst_count();
        return m_uvm_obj .get_inst_count();
    endfunction

endclass

`pyhdl_uvm_type_utils(uvm_object, pyhdl_uvm_object, uvm_object, pyhdl_uvm_object)

