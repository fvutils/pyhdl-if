#****************************************************************************
#* type_info_tlm_if.py
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
import typeworks
from typing import List
from hdl_if.tlm.tlm_method import TlmMethod
from .model_info_tlm_if import ModelInfoTlmIF

class TypeInfoTlmIF(object):
    ATTR_NAME = "_tlm_if_typeinfo"

    def __init__(self, info : typeworks.TypeInfo):
        self._base_init = None
        self._if_method_l : List[TlmMethod] = []
        pass

    @staticmethod
    def init(self, *args, **kwargs):
        print("init %s" % str(self))
        tlm_if_ti = TypeInfoTlmIF.get(typeworks.TypeInfo.get(type(self)))
        self._model = ModelInfoTlmIF()
        tlm_if_ti._base_init(self, *args, **kwargs)
        
    @classmethod
    def addMethods(cls, T):
        T.__init__ = cls.init

    @staticmethod
    def get(info) -> 'TypeInfoTlmIF':
        if not hasattr(info, TypeInfoTlmIF.ATTR_NAME):
            from hdl_if.tlm.tlm_ifc import TlmIfc
            setattr(info, TypeInfoTlmIF.ATTR_NAME, TlmIfc(info, info.T.__qualname__))
        return getattr(info, TypeInfoTlmIF.ATTR_NAME)

