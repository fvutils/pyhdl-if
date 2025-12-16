#****************************************************************************
#* method_def.py
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
from typing import List, Tuple, Any
from enum import Enum, auto
import inspect

class MethodKind(Enum):
    ImpTask = auto()
    ExpTask = auto()
    ImpFunc = auto()
    ExpFunc = auto()
    Imp = auto()
    Exp = auto()

# Sentinel value to indicate no default
_NO_DEFAULT = inspect.Parameter.empty

class MethodDef(object):

    def __init__(self, 
                 kind : MethodKind,
                 T,
                 name : str,
                 rtype,
                 params : List[Tuple[str, object]],
                 defaults : List[Any] = None):
        self._kind = kind
        self._name = name
        self._rtype = rtype
        self._params = params
        # defaults is a list parallel to params; each element is either a value or _NO_DEFAULT
        self._defaults = defaults if defaults is not None else [_NO_DEFAULT] * len(params)
        pass

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return self._kind 
    
    @property
    def rtype(self):
        return self._rtype
    
    @property
    def params(self):
        return self._params

    @property
    def defaults(self):
        return self._defaults
    


