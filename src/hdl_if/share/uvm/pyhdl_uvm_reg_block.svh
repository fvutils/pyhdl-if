/**
 * pyhdl_uvm_reg_block.svh
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

class pyhdl_uvm_reg_block extends pyhdl_uvm_object;

    function new(uvm_object obj);
        super.new(obj);
    endfunction

    virtual function PyObject get_parent();
        uvm_reg_block block;
        $cast(block, m_uvm_obj);
        return pyhdl_uvm_object_rgy::inst().wrap(block.get_parent());
    endfunction

    virtual function PyObject get_root_blocks();
        uvm_reg_block blocks[$];
        py_list ret = new();
        uvm_reg_block block;

        $cast(block, m_uvm_obj);
        block.get_root_blocks(blocks);

        foreach (blocks[i]) begin
            ret.append_obj(pyhdl_uvm_object_rgy::inst().wrap(blocks[i]));
        end

        return ret.borrow();
    endfunction

    virtual function PyObject get_registers();
        uvm_reg regs[$];
        py_list ret = new();
        uvm_reg_block block;

        $cast(block, m_uvm_obj);
        block.get_registers(regs);

        foreach (regs[i]) begin
            ret.append_obj(pyhdl_uvm_object_rgy::inst().wrap(regs[i]));
        end

        return ret.borrow();
    endfunction

endclass

`pyhdl_uvm_type_utils(uvm_reg_block, pyhdl_uvm_reg_block, uvm_object, pyhdl_uvm_object)