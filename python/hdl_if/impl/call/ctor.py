#****************************************************************************
#* ctor.py
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
from typing import List
from .api_def import ApiDef
from .method_def import MethodDef

class Ctor(object):

    _inst = None

    def __init__(self):
        self.method_l : List[MethodDef] = []

    def addMethodDef(self, md):
        self.method_l.append(md)

    def getMethodDefs(self) -> List[MethodDef]:
        ret = self.method_l.copy()
        self.method_l.clear()
        return ret

    @classmethod
    def init(cls):
        cls._inst = None

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = Ctor()
        return cls._inst

