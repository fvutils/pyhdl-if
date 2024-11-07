#****************************************************************************
#* method_decorator_impl.py
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
import inspect
from .ctor import Ctor
from .imp_func_impl import ImpFuncImpl
from .imp_task_impl import ImpTaskImpl
from .method_def import MethodDef, MethodKind
from typing import get_type_hints

class MethodDecoratorImpl(object):

    def __init__(self, kind : MethodKind, args=None, kwargs=None):
        self._kind = kind
        self._args = args
        self._kwargs = kwargs

    def __call__(self, T):

        code = T.__code__
        hints = get_type_hints(T)

        if "return" in hints.keys():
            rtype = hints["return"]
        else:
            rtype = None

        params = []
        for i in range(1,code.co_argcount):
            pname = code.co_varnames[i]
            if pname not in hints.keys():
                raise Exception("Method parameter %s.%s is untyped" % (
                    T.__name__,
                    pname))
            params.append((pname, hints[pname]))

        if self._kind in [MethodKind.Imp,MethodKind.Exp]:
            # Need to probe type
            if inspect.iscoroutinefunction(T):
                if self._kind == MethodKind.Imp:
                    self._kind = MethodKind.ImpTask
                else:
                    self._kind = MethodKind.ExpTask
            else:
                if self._kind == MethodKind.Imp:
                    self._kind = MethodKind.ImpFunc
                else:
                    self._kind = MethodKind.ExpFunc

        md = MethodDef(self._kind, T, T.__name__, rtype, params)
        Ctor.inst().addMethodDef(md)

        if self._kind == MethodKind.ImpFunc:
            closure = ImpFuncImpl(md)
            return lambda self, *args, **kwargs: closure(self, *args, **kwargs)
        elif self._kind == MethodKind.ImpTask:
            closure = ImpTaskImpl(md)
            return lambda self, *args, **kwargs: closure(self, *args, **kwargs)
        else:
            return T
