#****************************************************************************
#* hdl_services.py
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
from typing import Dict, List

class HdlServices(object):

    _impl : List['HdlServices'] = []
    _impl_m : Dict[str, 'HdlServices'] = {}

    def __init__(self, name):
        self.name = name

    def registerTimeCB(self, cb : callable, time_ps : int) -> object:
        raise NotImplementedError("registerTimeCB for %s" % str(type(self)))

    @classmethod
    def registerServices(cls, services):
        cls._impl.append(services)
        cls._impl_m[services.name] = services

    @classmethod
    def inst(cls, name=None):
        if len(cls._impl) == 0:
            raise Exception("No services registered yet")
        if name is None:
            return cls._impl[0]
        else:
            return cls._impl_m[name]

