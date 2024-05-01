#****************************************************************************
#* decorators.py
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
from .impl.call.api_decorator_impl import ApiDecoratorImpl
from .impl.call.method_decorator_impl import MethodDecoratorImpl
from .impl.call.method_def import MethodKind

#********************************************************************
#* Decorators for API interfaces
#********************************************************************

def api(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # Called with no arguments
        return ApiDecoratorImpl()(args[0])
    else:
        return ApiDecoratorImpl(args, kwargs)
        
def impfunc(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return MethodDecoratorImpl(MethodKind.ImpFunc)(args[0])
    else:
        return MethodDecoratorImpl(MethodKind.ImpFunc, args, kwargs)

def imptask(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return MethodDecoratorImpl(MethodKind.ImpTask)(args[0])
    else:
        return MethodDecoratorImpl(MethodKind.ImpTask, args, kwargs)

def expfunc(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return MethodDecoratorImpl(MethodKind.ExpFunc)(args[0])
    else:
        return MethodDecoratorImpl(MethodKind.ExpFunc, args, kwargs)

def exptask(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return MethodDecoratorImpl(MethodKind.ExpTask)(args[0])
    else:
        return MethodDecoratorImpl(MethodKind.ExpTask, args, kwargs)

#********************************************************************
#* Decorators for TLM interfaces
#********************************************************************

def tlm_if(*args, **kwargs):
    from .impl.tlm.tlm_interface_decorator_impl import TlmInterfaceDecoratorImpl
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return TlmInterfaceDecoratorImpl([], {})(args[0])
    else:
        return TlmInterfaceDecoratorImpl(args, kwargs)

def req_fifo(*args, **kwargs):
    from .impl.tlm.req_fifo_decorator_impl import ReqFifoDecoratorImpl
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return ReqFifoDecoratorImpl([], {})(args[0])
    else:
        return ReqFifoDecoratorImpl(args, kwargs)

def rsp_fifo(*args, **kwargs):
    from .impl.tlm.rsp_fifo_decorator_impl import RspFifoDecoratorImpl
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return RspFifoDecoratorImpl([], {})(args[0])
    else:
        return RspFifoDecoratorImpl(args, kwargs)

def reqrsp_fifo(*args, **kwargs):
    from .impl.tlm.req_rsp_fifo_decorator_impl import ReqRspFifoDecoratorImpl
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return ReqRspFifoDecoratorImpl([], {})(args[0])
    else:
        return ReqRspFifoDecoratorImpl(args, kwargs)
    pass

def req_mbox(*args, **kwargs):
    pass

def rsp_mbox(*args, **kwargs):
    pass
