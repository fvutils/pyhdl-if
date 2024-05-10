#****************************************************************************
#* hdl_call_endpoint.py
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

class HdlCallEndpoint(object):

    def __init__(self, name):
        from hdl_if.hdl_obj_rgy import HdlObjRgy
        self._name = name
        self._backend = None
        self._obj_rgy = HdlObjRgy.inst()

    @property
    def name(self):
        return self._name
    
    @property
    def backend(self):
        from hdl_if.backend import Backend
        if self._backend is None:
            self._backend = Backend.inst()
        return self._backend
    
    def idle(self):
        be = self.backend

    def invoke_hdl_f(self, obj_id : int, method_name : str, args : tuple):
        raise NotImplementedError("Class %s doesn't implement invoke_hdl_f" % str(type(self)))

    def invoke_hdl_t(self, 
                     obj_id, 
                     evt_obj,
                     method_name, 
                     args):
        raise NotImplementedError("Class %s doesn't implement invoke_hdl_t" % str(type(self)))

    def response_py_t(self, sem_id, res):
        raise NotImplementedError("Class %s doesn't implement response_py_t" % str(type(self)))

    def newObj(self, cls_t, obj_id, args):
        raise NotImplementedError("Class %s doesn't implement newObj" % str(type(self)))

    def registerObj(self, obj, inst_path, trim_elems=0):
        if trim_elems:
            path_s = inst_path.split(".")
            path_s = path_s[:-trim_elems]
            inst_path = ".".join(path_s)
        self._obj_rgy.registerObj(obj, inst_path)
    
    



