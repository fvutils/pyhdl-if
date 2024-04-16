#****************************************************************************
#* rsp_fifo_decorator_impl.py
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

class RspFifoDecoratorImpl(InterfaceDecoratorImplBase):

    def __init__(self, args, kwargs):
        super().__init__(args, kwargs)
        self.proxy = None

    def decorate(self, T):
        from hdl_tlm_if.tlm_method import TlmMethod, TlmMethodKind
        self.proxy = TlmMethod(T.__name__, TlmMethodKind.Rsp, None, None)

        async def closure(self, obj):
            model = self._model
            if T.__name__ not in model._if_m.keys():
                raise Exception("Method %s is unbound" % T.__name__)
            ifc = model._if_m[T.__name__]
            await ifc.get(obj)
        return closure

    def register(self, T, Tp):
        super().register(T, self.proxy)

