#****************************************************************************
#* hdl_call_endpoint_dpi.py
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
from hdl_if.call.hdl_call_endpoint import HdlCallEndpoint
from hdl_if import HdlServices

class HdlCallEndpointDPI(HdlCallEndpoint):

    def __init__(self, scope):
        super().__init__("dpi")
        self.scope = scope

        exe_l = ctypes.cdll.LoadLibrary(None)
        if not hasattr(exe_l, "pyhdl_call_if_invoke_hdl_f"):
            print("TODO: Try DPIExportLib")
            exe_l = self._findDPIExportLib()
        try:
            # self.svSetScope = exe_l.svSetScope
            # self.svSetScope.restype = None
            # self.svSetScope.argtypes = (
            #     ctypes.c_void_p,
            # )
            self.pyhdl_call_if_invoke_hdl_f = exe_l.pyhdl_call_if_invoke_hdl_f
            self.pyhdl_call_if_invoke_hdl_f.restype = ctypes.py_object
            self.pyhdl_call_if_invoke_hdl_f.argtypes = (
                ctypes.c_int,
                ctypes.c_char_p,
                ctypes.py_object)
            self.pyhdl_call_if_invoke_hdl_t = exe_l.pyhdl_call_if_invoke_hdl_t
            self.pyhdl_call_if_invoke_hdl_t.restype = ctypes.c_int
            self.pyhdl_call_if_invoke_hdl_t.argtypes = (
                ctypes.c_int,
                ctypes.py_object,
                ctypes.c_char_p,
                ctypes.py_object)
            self.pyhdl_call_if_response_py_t = exe_l.pyhdl_call_if_response_py_t
            self.pyhdl_call_if_response_py_t.restype = None
            self.pyhdl_call_if_response_py_t.argtypes = (
                ctypes.c_int,
                ctypes.py_object)
        except Exception as e:
            print("Exception(__init__): %s" % str(e), flush=True)
        
    def invoke_hdl_f(self, obj_id : int, method_name : str, args : tuple):
        dpi = HdlServices.inst("dpi")
        ret = None
        try:
            dpi.svSetScope(self.scope)
            ret = self.pyhdl_call_if_invoke_hdl_f(obj_id, method_name.encode(), args)
        except Exception as e:
            print("Exception(invoke_hdl_f): %s" % str(e), flush=True)
        return ret
    
    def invoke_hdl_t(self, 
                     obj_id, 
                     evt_obj,
                     method_name, 
                     args):
        dpi = HdlServices.inst("dpi")
        dpi.svSetScope(self.scope)
        self.pyhdl_call_if_invoke_hdl_t(
            obj_id,
            evt_obj,
            method_name.encode(),
            args)
    
    def response_py_t(self, sem_id, res):
        dpi = HdlServices.inst("dpi")
        try:
            dpi.svSetScope(self.scope)
            self.pyhdl_call_if_response_py_t(sem_id, res)
        except Exception as e:
            print("Exception(response_py): %s" % str(e), flush=True)

    # Note: implementation of object creation is
    # a bit different between environments
    def newObj(self, cls_t, obj_id, args):
        from .call_proxy_dpi import CallProxyDPI
        ret = cls_t(*args)
        setattr(ret, "_proxy", CallProxyDPI(ret, obj_id, self))
        return ret
    
    def connectObj(self, obj, obj_id):
        from .call_proxy_dpi import CallProxyDPI
        setattr(obj, "_proxy", CallProxyDPI(obj, obj_id, self))

    def _findDPIExportLib(self):
        pass

