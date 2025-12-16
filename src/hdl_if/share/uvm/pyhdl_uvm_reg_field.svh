/**
 * pyhdl_uvm_reg_field.svh
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

class pyhdl_uvm_reg_field extends pyhdl_uvm_object;

    function new(uvm_object obj);
        super.new(obj);
    endfunction

    function void set(longint unsigned value);
        uvm_reg_field field;
        $cast(field, m_uvm_obj);

        field.set(value);
    endfunction

    function longint unsigned get();
        uvm_reg_field field;
        $cast(field, m_uvm_obj);

        return field.get();
    endfunction

    task write(
        output bit      retval,
        input longint   value);
        retval = 0;
    endtask

    task read(
        output PyObject retval);
    endtask

endclass

`pyhdl_uvm_type_utils(uvm_reg_field, pyhdl_uvm_reg_field, uvm_object, pyhdl_uvm_object)