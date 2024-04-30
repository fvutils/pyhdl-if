#****************************************************************************
#* call_proxy_vpi.py
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
import hdl_if.impl.vpi.api as api
from typing import Dict, List, Tuple
from hdl_if.call.call_proxy import CallProxy

class CallProxyVPI(CallProxy):

    class Req(object):
        def __init__(self, id, args, ev):
            self.id = id
            self.args = args
            self.ev = ev
            print("Req.__init__: id=%d" % self.id, flush=True)

    def __init__(self, target, ev_h):
        self.target = target
        self.ev_h = ev_h
        self.ev_v = 1
        self.ev_h_armed = False
        self.req_q : List[Tuple[str,Tuple,object]] = []
        self.method_name_id_m : Dict[str, int] = {}
        pass

    def invoke_hdl_f(
            self,
            method_name : str,
            args : tuple):
        raise Exception("VPI only supports task calls")

    async def invoke_hdl_t(
            self,
            method_name,
            args):
        from hdl_if.backend import Backend
        be = Backend.inst();
        evt = be.mkEvent()

        req = CallProxyVPI.Req(
            self.method_name_id_m[method_name],
            args, 
            evt)
        print("req: %s ; id=%d" % (str(req), req.id))
        self.req_q.append(req)

        # Decide if we need to toggle the VPI event handle
        if not self.ev_h_armed:
            val_s = api.t_vpi_value()
            val_s.format = api.vpiIntVal
            val_s.value.integer = self.ev_v
            self.ev_v = 0 if self.ev_v else 1
            api.vpi_put_value(self.ev_h, ctypes.byref(val_s), None, api.vpiNoDelay)
            self.ev_h_armed = True

        # Wait for ack
        ret = await evt.wait()

        self.ev_h_armed = False

        return ret
    
    def nextReq(self) -> Tuple[str,Tuple,object]:
        print("nextReq: len=%d" % len(self.req_q))
        if len(self.req_q) > 0:
            req = self.req_q.pop(0)
            print("req.id: %s" % str(req.id))
            print("return %s" % str(req))
            return req
        else:
            return None
    
    def getReqId(self, req : Tuple[str,Tuple,object]) -> int:
        if req[0] in self.method_name_id_m.keys():
            return self.method_name_id_m[req[0]]
        else:
            return -1
        
    def setMethodId(self, name, id):
        print("setMethodId: %s=%d" % (name, id))
        self.method_name_id_m[name] = id

    async def invoke_py_t_wrap(
            self,
            sem_id,
            m,
            args):
        res = await m(*args)
        self.ep.response_py_t(sem_id, res)

    def invoke_py_t(
            self,
            sem_id,
            method_name,
            args):
        from hdl_if.backend import Backend
        be = Backend.inst()

        m = getattr(self.target, method_name, None)

        if m is None:
            print("Error: failed to find method %s" % method_name, flush=True)
        
        be.mkTask(self.invoke_py_t_wrap(sem_id, m, args))
        be.idle()
        

        

