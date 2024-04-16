#****************************************************************************
#* context.py
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
from hdl_call_if.hdl_call_endpoint import HdlCallEndpoint

class Context(object):
    _inst = None

    def __init__(self):
        self._endpoints = []
        self._object_rgy_type_m = {}
        self._object_rgy_name_m = {}
        pass

    def addEndpoint(self, ep : HdlCallEndpoint):
        self._endpoints.append(ep)

    def getObjectsByType(self, typename):
        pass
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = Context()
        return cls._inst


