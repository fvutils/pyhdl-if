#****************************************************************************
#* tlm_interface_decorator_impl.py
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
from hdl_if.tlm.tlm_ifc import TlmIfc
from hdl_if.tlm.tlm_ifc_rgy import TlmIfcRgy
from .type_info_tlm_if import TypeInfoTlmIF

class TlmInterfaceDecoratorImpl(typeworks.ClsDecoratorBase):

    def __init__(self, args, kwargs):
        super().__init__(args, kwargs)
        self.tlm_ifc = None
        pass

    def get_type_category(self):
        return TlmIfc
    
    def pre_decorate(self, T):
        from hdl_if.tlm.tlm_method import TlmMethod
        tlm_if_ti = TypeInfoTlmIF.get(self.get_typeinfo())
        self.tlm_ifc = TlmIfc(tlm_if_ti, T.__qualname__)

        # TODO: collect registered TLM methods from base classes
        if_methods = typeworks.DeclRgy.pop_decl(TlmMethod)

        print("if_methods: %d" % len(if_methods))

        tlm_if_ti._if_method_l.extend(if_methods)
        self.tlm_ifc._if_method_l.extend(if_methods)

        super().pre_decorate(T)
    
    def post_decorate(self, T, Tp):
        tlm_if_ti = TypeInfoTlmIF.get(self.get_typeinfo())
        super().post_decorate(T, Tp)

        tlm_if_ti._base_init = Tp.__init__

        TypeInfoTlmIF.addMethods(Tp)

        # TODO: Add Methods

    def pre_register(self):
        TlmIfcRgy.inst().addTlmIf(self.tlm_ifc)
        super().pre_register()




