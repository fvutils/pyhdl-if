#****************************************************************************
#* api_def_rgy.py
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
from typing import List, Dict
from .api_def import ApiDef

class ApiDefRgy(object):

    _inst = None

    def __init__(self):
        self.api_m : Dict[str, ApiDef] = {}
        self.api_l : List[ApiDef] = []
        pass

    def addApiDef(self, ad):
        self.api_m[ad.name] = ad
        self.api_l.append(ad)

    def getApis(self):
        return self.api_l

    @classmethod
    def init(cls):
        cls._inst = None

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = ApiDefRgy()
        return cls._inst


