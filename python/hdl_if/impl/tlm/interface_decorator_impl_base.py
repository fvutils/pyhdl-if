#****************************************************************************
#* interface_decorator_impl_base.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
import typeworks

class InterfaceDecoratorImplBase(typeworks.MethodDecoratorBase):

    def __init__(self, args, kwargs):
        super().__init__(args, kwargs)

    def get_category(self):
        from hdl_if.tlm.tlm_method import TlmMethod
        return TlmMethod

