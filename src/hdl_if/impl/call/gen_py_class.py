#****************************************************************************
#* gen_py_class.py
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
from typing import TextIO
from .api_def import ApiDef
from .method_def import MethodDef, MethodKind

class GenPyClass:
    """Generates Python class definitions from ApiDef instances"""
    
    TYPE_MAP = {
        ctypes.c_bool: 'ct.c_bool',
        bool: 'ct.c_bool',
        ctypes.c_byte: 'ct.c_byte',
        ctypes.c_char: 'ct.c_char',
        ctypes.c_int8: 'ct.c_int8',
        ctypes.c_int16: 'ct.c_int16',
        ctypes.c_int32: 'ct.c_int32',
        ctypes.c_int64: 'ct.c_int64',
        int: 'ct.c_int64',
        ctypes.c_uint8: 'ct.c_uint8',
        ctypes.c_uint16: 'ct.c_uint16',
        ctypes.c_uint32: 'ct.c_uint32',
        ctypes.c_uint64: 'ct.c_uint64',
        float: 'float',
        ctypes.c_double: 'ct.c_double',
        str: 'str',
        ctypes.py_object: 'ct.py_object',
    }
    
    def __init__(self, out: TextIO, ind: str = ""):
        self._out = out
        self._ind = ind
    
    def gen_module(self, apis: list):
        """Generate complete Python module with API classes"""
        self.println("import ctypes as ct")
        self.println("import hdl_if as hif")
        self.println()
        
        for api in apis:
            self.gen_class(api)
            self.println()
    
    def gen_class(self, api: ApiDef):
        """Generate a single Python class"""
        self.println("@hif.api")
        self.println(f"class {api.name}(object):")
        self.inc_ind()
        
        if api.init_params:
            self.gen_init(api)
            self.println()
        
        has_methods = False
        for method in api.methods:
            self.gen_method(method)
            self.println()
            has_methods = True
        
        if not has_methods and not api.init_params:
            self.println("pass")
        
        self.dec_ind()
    
    def gen_init(self, api: ApiDef):
        """Generate __init__ method"""
        params_str = ", ".join([f"{name}: {self._type_str(ptype)}" 
                                for name, ptype in api.init_params])
        self.println(f"def __init__(self, {params_str}):")
        self.inc_ind()
        for name, _ in api.init_params:
            self.println(f"self.{name} = {name}")
        self.dec_ind()
    
    def gen_method(self, method: MethodDef):
        """Generate a single method"""
        decorator = "@hif.imp" if method.kind in [MethodKind.ImpFunc, MethodKind.ImpTask] else "@hif.exp"
        self.println(decorator)
        
        is_async = method.kind in [MethodKind.ImpTask, MethodKind.ExpTask]
        async_prefix = "async " if is_async else ""
        
        params_str = ""
        if method.params:
            params_str = ", " + ", ".join([f"{name}: {self._type_str(ptype)}" 
                                           for name, ptype in method.params])
        
        return_annotation = ""
        if method.rtype is not None:
            return_annotation = f" -> {self._type_str(method.rtype)}"
        
        self.println(f"{async_prefix}def {method.name}(self{params_str}){return_annotation}:")
        self.inc_ind()
        self.println("pass")
        self.dec_ind()
    
    def _type_str(self, ptype) -> str:
        """Convert Python type to string representation"""
        if ptype in self.TYPE_MAP:
            return self.TYPE_MAP[ptype]
        return str(ptype)
    
    def println(self, text: str = ""):
        """Write a line with current indentation"""
        if text:
            self._out.write(f"{self._ind}{text}\n")
        else:
            self._out.write("\n")
    
    def inc_ind(self):
        """Increase indentation"""
        self._ind += "    "
    
    def dec_ind(self):
        """Decrease indentation"""
        if len(self._ind) >= 4:
            self._ind = self._ind[:-4]
        else:
            self._ind = ""
