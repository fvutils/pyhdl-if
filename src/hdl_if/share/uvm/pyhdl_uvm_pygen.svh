/**
 * pyhdl_uvm_pygen.svh
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

class pyhdl_uvm_pygen extends uvm_test;
    `uvm_component_utils(pyhdl_uvm_pygen)

    pyhdl_uvm_component_proxy  m_proxy;

    function new(string name, uvm_component parent=null);
        super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "hdl_if.uvm.pygen::PyGen";
        m_proxy.build_phase(phase);
        $finish;
    endfunction

    function void connect_phase(uvm_phase phase);
        m_proxy.connect_phase(phase);
    endfunction

    task run_phase(uvm_phase phase);
        m_proxy.run_phase(phase);
    endtask

endclass

