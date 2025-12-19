/**
 * pyhdl_uvm.sv
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

`include "uvm_macros.svh"
`include "pyhdl_if_macros.svh"
`include "pyhdl_uvm_macros.svh"

package pyhdl_uvm;
    import uvm_pkg::*;
    import pyhdl_if::*;

    typedef class pyhdl_uvm_object_type_rgy;
    typedef class pyhdl_uvm_object_type_rgy_p;

    `include "pyhdl_uvm_apis.svh"
    `include "pyhdl_uvm_object_if.svh"

    `include "pyhdl_uvm_analysis_port.svh"
    `include "pyhdl_uvm_enum_rgy.svh"
    `include "pyhdl_uvm_object.svh"
    `include "pyhdl_uvm_object_type.svh"
    `include "pyhdl_uvm_cmdline_processor.svh"
    `include "pyhdl_uvm_component.svh"
    `include "pyhdl_uvm_component_proxy.svh"
    `include "pyhdl_uvm_object_list.svh"
    `include "pyhdl_uvm_object_map.svh"
    `include "pyhdl_uvm_object_string.svh"
    `include "pyhdl_uvm_object_rgy.svh"
    `include "pyhdl_uvm_sequence_proxy.svh"
    `include "pyhdl_uvm_phase.svh"
    `include "pyhdl_uvm_reg.svh"
    `include "pyhdl_uvm_reg_block.svh"
    `include "pyhdl_uvm_reg_field.svh"
    `include "pyhdl_uvm_wrapper_factory.svh"
    `include "pyhdl_uvm_pygen.svh"

endpackage
