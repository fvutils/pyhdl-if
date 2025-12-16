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
import inspect
from hdl_if.call.call_proxy import CallProxy
from .method_def import MethodDef

class ImpFuncImpl(object):

    def __init__(self, md : MethodDef):
        self._md = md
        pass

    def __call__(self, api_self, *args, **kwargs):
        if not hasattr(api_self, "_proxy") or getattr(api_self, "_proxy") is None:
            raise Exception("Class is not bound to an HDL object")

        # Build full argument list by combining provided args/kwargs with defaults
        full_args = self._build_args(args, kwargs)

        proxy : CallProxy = getattr(api_self, "_proxy") 

        return proxy.invoke_hdl_f(
            self._md.name,
            full_args
        )

    def _build_args(self, args, kwargs):
        """Build full argument tuple by combining provided args/kwargs with defaults."""
        params = self._md.params
        defaults = self._md.defaults
        n_params = len(params)
        
        # Start with provided positional args
        result = list(args)
        
        # Fill in the remaining parameters
        for i in range(len(result), n_params):
            pname = params[i][0]
            if pname in kwargs:
                # Use the provided keyword argument
                result.append(kwargs[pname])
            elif defaults[i] is not inspect.Parameter.empty:
                # Use the default value
                result.append(defaults[i])
            else:
                raise TypeError(f"{self._md.name}() missing required argument: '{pname}'")
        
        # Check for unexpected keyword arguments
        param_names = {p[0] for p in params}
        for key in kwargs:
            if key not in param_names:
                raise TypeError(f"{self._md.name}() got an unexpected keyword argument '{key}'")
        
        return tuple(result)
