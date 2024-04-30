#****************************************************************************
#* imp_func_impl.py
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
from hdl_if.call.call_proxy import CallProxy

class ImpFuncImpl(object):

    def __init__(self, md):
        self._md = md
        pass

    def __call__(self, api_self, *args, **kwargs):
        if not hasattr(api_self, "_proxy") or getattr(api_self, "_proxy") is None:
            raise Exception("Class is not bound to an HDL object")

        if len(kwargs) != 0:
            raise Exception("Only positional arguments are supported")

        proxy : CallProxy = getattr(api_self, "_proxy") 

        print("args: %s" % str(args), flush=True)
        return proxy.invoke_hdl_f(
            self._md.name,
            args
        )
