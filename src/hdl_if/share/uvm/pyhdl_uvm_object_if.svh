/**
 * pyhdl_uvm_object_if.svh
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

/**
 * Both sides of an object that has crossed the language boundary.
 *
 * Every wrapper implements this, so the registry can recover either half from a
 * handle to the other without knowing the concrete wrapper type.
 *
 * @see pyhdl_uvm_object_rgy
 */
interface class pyhdl_uvm_object_if;
    pure virtual function uvm_object get_object();
    pure virtual function PyObject get_pyobject();
endclass

