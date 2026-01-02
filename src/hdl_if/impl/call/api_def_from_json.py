#****************************************************************************
#* api_def_from_json.py
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
import json
import ctypes
from typing import Dict, List, Any
from .api_def import ApiDef
from .method_def import MethodDef, MethodKind

class ApiDefFromJson:
    """Parses JSON API definitions and creates ApiDef instances"""
    
    TYPE_MAP = {
        'bool': ctypes.c_bool,
        'byte': ctypes.c_byte,
        'char': ctypes.c_char,
        'int8': ctypes.c_int8,
        'int16': ctypes.c_int16,
        'int32': ctypes.c_int32,
        'int64': ctypes.c_int64,
        'int': int,
        'uint8': ctypes.c_uint8,
        'uint16': ctypes.c_uint16,
        'uint32': ctypes.c_uint32,
        'uint64': ctypes.c_uint64,
        'float': float,
        'double': ctypes.c_double,
        'str': str,
        'string': str,
        'pyobject': ctypes.py_object,
        'object': ctypes.py_object,
    }
    
    @classmethod
    def parse(cls, json_str: str) -> List[ApiDef]:
        """Parse JSON string and return list of ApiDef instances"""
        data = json.loads(json_str)
        
        if isinstance(data, dict):
            if "apis" in data:
                apis_data = data["apis"]
            else:
                apis_data = [data]
        elif isinstance(data, list):
            apis_data = data
        else:
            raise ValueError("JSON must be an object or array")
        
        return [cls._parse_api(api_data) for api_data in apis_data]
    
    @classmethod
    def _parse_api(cls, api_data: Dict[str, Any]) -> ApiDef:
        """Parse a single API definition"""
        fullname = api_data.get("fullname")
        if not fullname:
            raise ValueError("API definition must have 'fullname' field")
        
        init_params = []
        if "init_params" in api_data:
            for param in api_data["init_params"]:
                pname = param["name"]
                ptype_str = param["type"]
                ptype = cls._parse_type(ptype_str)
                init_params.append((pname, ptype))
        
        methods = []
        if "methods" in api_data:
            for method_data in api_data["methods"]:
                method = cls._parse_method(method_data)
                methods.append(method)
        
        return ApiDef(fullname, init_params, methods, pycls=None)
    
    @classmethod
    def _parse_method(cls, method_data: Dict[str, Any]) -> MethodDef:
        """Parse a single method definition"""
        name = method_data.get("name")
        if not name:
            raise ValueError("Method definition must have 'name' field")
        
        kind_str = method_data.get("kind", "exp_func")
        kind = cls._parse_kind(kind_str)
        
        rtype = None
        if "return_type" in method_data:
            rtype_str = method_data["return_type"]
            if rtype_str and rtype_str != "void" and rtype_str != "None":
                rtype = cls._parse_type(rtype_str)
        
        params = []
        if "params" in method_data:
            for param in method_data["params"]:
                pname = param["name"]
                ptype_str = param["type"]
                ptype = cls._parse_type(ptype_str)
                params.append((pname, ptype))
        
        return MethodDef(kind, None, name, rtype, params)
    
    @classmethod
    def _parse_kind(cls, kind_str: str) -> MethodKind:
        """Parse method kind string"""
        kind_map = {
            'imp_task': MethodKind.ImpTask,
            'exp_task': MethodKind.ExpTask,
            'imp_func': MethodKind.ImpFunc,
            'exp_func': MethodKind.ExpFunc,
            'imp': MethodKind.ImpTask,
            'exp': MethodKind.ExpFunc,
        }
        kind_str = kind_str.lower()
        if kind_str not in kind_map:
            raise ValueError(f"Unknown method kind: {kind_str}")
        return kind_map[kind_str]
    
    @classmethod
    def _parse_type(cls, type_str: str):
        """Parse type string to Python type"""
        type_str_lower = type_str.lower()
        if type_str_lower in cls.TYPE_MAP:
            return cls.TYPE_MAP[type_str_lower]
        raise ValueError(f"Unknown type: {type_str}")
