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
import ctypes
from .interface_decorator_impl_base import InterfaceDecoratorImplBase

class RspFifoDecoratorImpl(InterfaceDecoratorImplBase):

    def __init__(self, args, kwargs):
        super().__init__(args, kwargs)
        self.proxy = None

    def decorate(self, T):
        from hdl_if.tlm.tlm_method import TlmMethod, TlmMethodKind

        is_method, rtype, params = self.get_signature()

        if rtype is None:
            raise Exception("Response FIFO must specify a return type")
        if len(params) > 0:
            raise Exception("Respoonse FIFO must not have parameters")

        if not hasattr(rtype, "_fields_"):
            raise Exception("FIFO response type must derive from ctypes.Structure")

        self.proxy = TlmMethod(T.__name__, TlmMethodKind.Rsp, None, rtype)

        async def closure(self):
            model = self._model
            if T.__name__ not in model._if_m.keys():
                raise Exception("Method %s is unbound" % T.__name__)
            ifc = model._if_m[T.__name__]
            ival = await ifc.get()
            sz = ctypes.sizeof(rtype)
            bval = bytearray(sz)

            for i in range(sz):
                bval[i] = (ival & 0xFF)
                ival >>= 8

            obj = rtype.from_buffer_copy(bval)

            return obj
        return closure

    def register(self, T, Tp):
        super().register(T, self.proxy)

