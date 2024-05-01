#****************************************************************************
#* api_def.py
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

class ApiDef(object):

    def __init__(self, fullname, init_params, methods):
        self._fullname = fullname
        self._init_params = init_params
        self._methods = methods

    @property
    def fullname(self):
        return self._fullname

    @property
    def name(self):
        last_dot = self._fullname.rfind('.')
        if last_dot != -1:
            return self._fullname[last_dot+1:]
        else:
            return self._fullname
        
    @property
    def init_params(self):
        return self._init_params

    @property
    def methods(self):
        return self._methods

