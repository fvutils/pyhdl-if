/**
 * pyhdl_uvm_object_type_ap.svh
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

class pyhdl_uvm_object_type_ap #(type T) extends pyhdl_uvm_object_type;
    typedef pyhdl_uvm_type_info_ap #(T) this_t;
    static this_t prv_inst;

    function new(string name);
        super.new(name);
    endfunction

    virtual function bit issubclass(uvm_object obj);
        uvm_analysis_port #(T) test_t;
        return $cast(test_t, obj);
    endfunction

    static function pyhdl_uvm_object_type inst(string name);
        if (prv_inst == null) begin
            prv_inst = new(name);
        end
    endfunction


endclass
