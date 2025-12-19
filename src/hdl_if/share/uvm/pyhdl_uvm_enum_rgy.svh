/**
 * pyhdl_uvm_enum_rgy.svh
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

/**
 * Class to store information about an enum type
 */
class pyhdl_uvm_enum_info;
    string          type_name;
    string          names[$];
    int             values[$];
    
    function new(string type_name);
        this.type_name = type_name;
    endfunction
    
    function void add_enumerator(string name, int value);
        names.push_back(name);
        values.push_back(value);
    endfunction
    
    function int get_size();
        return names.size();
    endfunction
    
    function string get_name(int index);
        if (index >= 0 && index < names.size()) begin
            return names[index];
        end
        return "";
    endfunction
    
    function int get_value(int index);
        if (index >= 0 && index < values.size()) begin
            return values[index];
        end
        return 0;
    endfunction
    
    function int find_value(string name);
        foreach (names[i]) begin
            if (names[i] == name) begin
                return values[i];
            end
        end
        `PYHDL_IF_FATAL(("Enumerator '%s' not found in enum type '%s'", name, type_name))
        return 0;
    endfunction
    
    function string find_name(int value);
        foreach (values[i]) begin
            if (values[i] == value) begin
                return names[i];
            end
        end
        return $sformatf("UNKNOWN(%0d)", value);
    endfunction
endclass

/**
 * Registry for enum types
 */
class pyhdl_uvm_enum_rgy extends uvm_enum_rgy_imp_impl #(pyhdl_uvm_enum_rgy);
    static pyhdl_uvm_enum_rgy   m_inst;
    pyhdl_uvm_enum_info         m_enum_m[string];
    uvm_enum_rgy_exp_impl       m_exp;
    
    function new();
        super.new(this);
        m_exp = new(m_obj);
    endfunction
    
    function void register_enum(string type_name, pyhdl_uvm_enum_info info);
        if (m_enum_m.exists(type_name)) begin
            `PYHDL_IF_FATAL(("Enum type '%s' is already registered", type_name))
        end
        m_enum_m[type_name] = info;
        `PYHDL_IF_DEBUG(("Registered enum type '%s' with %0d enumerators", type_name, info.get_size()))
    endfunction
    
    function pyhdl_uvm_enum_info get_enum_info(string type_name);
        if (!m_enum_m.exists(type_name)) begin
            return null;
        end
        return m_enum_m[type_name];
    endfunction
    
    virtual function PyObject get_enum_names(string type_name);
        pyhdl_uvm_enum_info info;
        PyObject names_list;
        
        if (!m_enum_m.exists(type_name)) begin
            `PYHDL_IF_FATAL(("Enum type '%s' is not registered", type_name))
            return None;
        end
        
        info = m_enum_m[type_name];
        names_list = PyList_New(longint'(info.get_size()));
        
        foreach (info.names[i]) begin
            PyObject name_obj = PyUnicode_FromString(info.names[i]);
            void'(PyList_SetItem(names_list, longint'(i), name_obj));
        end
        
        return names_list;
    endfunction
    
    virtual function PyObject get_enum_values(string type_name);
        pyhdl_uvm_enum_info info;
        PyObject values_list;
        
        if (!m_enum_m.exists(type_name)) begin
            `PYHDL_IF_FATAL(("Enum type '%s' is not registered", type_name))
            return None;
        end
        
        info = m_enum_m[type_name];
        values_list = PyList_New(longint'(info.get_size()));
        
        foreach (info.values[i]) begin
            PyObject value_obj = PyLong_FromLong(longint'(info.values[i]));
            void'(PyList_SetItem(values_list, longint'(i), value_obj));
        end
        
        return values_list;
    endfunction
    
    virtual function PyObject get_enum_types();
        PyObject types_list;
        string type_names[$];
        int idx = 0;
        
        // Collect all registered type names
        foreach (m_enum_m[tn]) begin
            type_names.push_back(tn);
        end
        
        types_list = PyList_New(longint'(type_names.size()));
        
        foreach (type_names[i]) begin
            PyObject name_obj = PyUnicode_FromString(type_names[i]);
            void'(PyList_SetItem(types_list, longint'(i), name_obj));
        end
        
        return types_list;
    endfunction
    
    static function pyhdl_uvm_enum_rgy inst();
        if (m_inst == null) begin
            m_inst = new();
        end
        return m_inst;
    endfunction
endclass

