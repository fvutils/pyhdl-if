#****************************************************************************
#* req_fifo_decorator_impl.py
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
from .interface_decorator_impl_base import InterfaceDecoratorImplBase

class ReqFifoDecoratorImpl(InterfaceDecoratorImplBase):

    def __init__(self, args, kwargs):
        super().__init__(args, kwargs)
        self.proxy = None

    def decorate(self, T):
        from hdl_tlm_if.tlm_method import TlmMethod, TlmMethodKind
        from typeworks.impl.typeinfo import TypeInfo
        from vsc_dataclasses.impl.typeinfo_randclass import TypeInfoRandClass

        is_method, rtype, params = self.get_signature()

        if rtype is not None:
            raise Exception("Request-FIFO method may not have a return type")
        if len(params) != 1:
            raise Exception("Request-FIFO method must have exactly one data parameter (%d)" % len(params))

        ptype = params[0][1]
        ptype_info = TypeInfo.get(ptype, False)

        if ptype_info is None:
            raise Exception("FIFO data-parameter types must be registered as randclass")
        
        ptype_ti = TypeInfoRandClass.get(ptype_info)

        self.proxy = TlmMethod(T.__name__, TlmMethodKind.Req, ptype_ti, None)

        async def closure(self, obj):
            model = self._model
            if T.__name__ not in model._if_m.keys():
                raise Exception("Method %s is unbound" % T.__name__)
            ifc = model._if_m[T.__name__]
            await ifc.put(obj)
        return closure
    
    def register(self, T, Tp):
        super().register(T, self.proxy)

