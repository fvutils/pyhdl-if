/**
 * pyhdl_uvm_phase.svh
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

class pyhdl_uvm_phase extends pyhdl_uvm_object;

    function new(uvm_object obj);
        super.new(obj);
    endfunction

    virtual function void raise_objection(input PyObject obj, input int count);
        uvm_phase phase;
        uvm_object o;

        o = pyhdl_uvm_object_rgy::inst().get_object(obj);
        $cast(phase, m_uvm_obj);
        phase.raise_objection(o, "", count);
    endfunction

    virtual function void drop_objection(input PyObject obj, input int count);
        uvm_phase phase;
        uvm_object o;
        o = pyhdl_uvm_object_rgy::inst().get_object(obj);
        $cast(phase, m_uvm_obj);
        phase.drop_objection(o, "", count);

    endfunction
endclass

`pyhdl_uvm_type_utils(uvm_phase, pyhdl_uvm_phase, uvm_object, pyhdl_uvm_object)
