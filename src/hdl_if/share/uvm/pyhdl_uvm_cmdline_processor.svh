/**
 * pyhdl_uvm_cmdline_processor.svh
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

class pyhdl_uvm_cmdline_processor extends pyhdl_uvm_object;
    uvm_cmdline_processor           m_clp;

    function new(uvm_object clp);
        super.new(clp);
    endfunction

    virtual function pyhdl_if::PyObject get_plusargs();
        uvm_cmdline_processor clp;
        string plusargs[$];
        py_list ret = new();

        $cast(clp, m_uvm_obj);

        clp.get_plusargs(plusargs);

        foreach (plusargs[i]) begin
            ret.append(py_from_str(plusargs[i]));
        end

        return ret.borrow();
    endfunction

endclass

`pyhdl_uvm_type_utils(uvm_cmdline_processor, pyhdl_uvm_cmdline_processor, uvm_object, pyhdl_uvm_object)

