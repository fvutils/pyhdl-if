#****************************************************************************
#* call_proxy_dpi.py
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
from hdl_if.call.call_proxy import CallProxy

class CallProxyDPI(CallProxy):

    def __init__(self, target, obj_id, ep):
        self.target = target
        self.obj_id = obj_id
        self.ep = ep
        pass

    def invoke_hdl_f(
            self,
            method_name : str,
            args : tuple):
        return self.ep.invoke_hdl_f(
            self.obj_id,
            method_name,
            args)
        pass

    async def invoke_hdl_t(
            self,
            method_name,
            args):
        from hdl_if.backend import Backend
        be = Backend.inst();
        evt = be.mkEvent()

        self.ep.invoke_hdl_t(self.obj_id, evt, method_name, args)
        res = await evt.wait()

        return res

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
