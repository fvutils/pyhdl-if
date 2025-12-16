/**
 * pyhdl_uvm_object_type.svh
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

class pyhdl_uvm_object_type;
    pyhdl_uvm_object_type       subtypes[$];
    string                      name;

    function new(string name);
        this.name = name;
    endfunction

    virtual function bit issubclass(uvm_object obj);
        return 0;
    endfunction

    virtual function pyhdl_uvm_object_if create(uvm_object obj);
        `PYHDL_IF_FATAL(("pyhdl_uvm_object_type base::create called", name))
        return null;
    endfunction

    virtual function int subtype_subclasses(ref pyhdl_uvm_object_type types[$], uvm_object obj);
        types = {};
        foreach (subtypes[i]) begin
            `PYHDL_IF_DEBUG(("%0s: issubclass(%0s)",
                subtypes[i].name,
                obj.get_type_name()))
            if (subtypes[i].issubclass(obj)) begin
                `PYHDL_IF_DEBUG(("issubtype"))
                types.push_back(subtypes[i]);
            end
        end
        return types.size();
    endfunction

endclass

class pyhdl_uvm_object_type_p #(type T=uvm_object, type Tw=pyhdl_uvm_object_w) extends pyhdl_uvm_object_type;
    typedef pyhdl_uvm_object_type_p #(T,Tw) this_t;
    static this_t   prv_inst;

    function new(string name);
        super.new(name);
    endfunction

    virtual function bit issubclass(uvm_object obj);
        T test_t;
        return $cast(test_t, obj);
    endfunction

    virtual function pyhdl_uvm_object_if create(uvm_object obj);
        Tw w = new(obj);

        // Create type on first object creation (?)
        return w;
    endfunction

    static function pyhdl_uvm_object_type inst(string name);
        if (prv_inst == null) begin
            prv_inst = new(name);
        end
        return prv_inst;
    endfunction
endclass

