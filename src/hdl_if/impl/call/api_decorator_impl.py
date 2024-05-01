#****************************************************************************
#* api_decorator_impl.py
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
from typing import get_type_hints
from .ctor import Ctor
from .api_def import ApiDef
from .api_def_rgy import ApiDefRgy

class ApiDecoratorImpl(object):

    def __init__(self, args=None, kwargs=None):
        pass

    def __call__(self, T):
        ctor = Ctor.inst()
        rgy = ApiDefRgy.inst()

#        print(inspect.getargs(T.__init__))
        init_params = []
        init_m = getattr(T, "__init__")
        if hasattr(init_m, "__code__"):
            init_co = init_m.__code__

            type_hints = get_type_hints(init_m)
            for i in range(1,init_co.co_argcount):
                name = init_co.co_varnames[i]
                if name not in type_hints.keys():
                    raise Exception("parameter %s is missing a type specification" % name)
                init_params.append((name, type_hints[name]))

        fullname = T.__module__ + "." + T.__qualname__
        ad = ApiDef(
            fullname,
            init_params,
            ctor.getMethodDefs())
        rgy.addApiDef(ad)

        return T


