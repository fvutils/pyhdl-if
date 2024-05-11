#****************************************************************************
#* hdl_services_dpi.py
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
from hdl_if.hdl_services import HdlServices

class HdlServicesDpi(HdlServices):

    def __init__(self, scope=None):
        super().__init__("dpi")
        self._scope = scope

        try:
            lib = ctypes.cdll.LoadLibrary(None)
            self._svGetScope = getattr(lib, "svGetScope")
            self._svGetScope.restype = ctypes.c_void_p

            self._svSetScope = getattr(lib, "svSetScope")
            self._svSetScope.argtypes = [ctypes.c_void_p]

            self._svGetNameFromScope = getattr(lib, "svGetNameFromScope")
            self._svGetNameFromScope.restype = ctypes.c_char_p
            self._svGetNameFromScope.argtypes = [ctypes.c_void_p]

            self._RegisterTimeCB = getattr(lib, "pyhdl_pi_if_RegisterTimeCB");
            self._RegisterTimeCB.restype = ctypes.c_int
            self._RegisterTimeCB.argtypes = [ctypes.py_object, ctypes.c_uint64]
        except Exception as e:
            print("DPI Exception: %s" % str(e), flush=True)

        if self._scope == None:
            self._scope = self.svGetScope()

    def getPkgScope(self):
        return self._scope

    def svGetScope(self):
        return self._svGetScope()

    def svSetScope(self, scope):
        self._svSetScope(scope)

    def registerTimeCB(self, cb : callable, time_ps : int) -> object:
        self._svSetScope(self._scope)
        cb_id = self._RegisterTimeCB(cb, time_ps)
        return cb_id
