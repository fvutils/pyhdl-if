#****************************************************************************
#* call_proxy.py
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

class CallProxy(object):

    def __init__(self, obj):
        self.target = obj
        pass

    async def invoke_hdl_t(
            self,
            method_name : str,
            args : tuple):
        raise NotImplementedError("CallProxy.invoke_hdl_t: %s" % str(type(self)))
    
    def invoke_hdl_f(
            self,
            method_name : str,
            args : tuple):
        raise NotImplementedError("CallProxy.invoke_hdl_f: %s" % str(type(self)))
    
    def response_hdl_t(
            self,
            call_id : int,
            result : object):
        """Called by the HDL environment to respond to a task call"""
        raise NotImplementedError("CallProxy.response_hdl_t: %s" % str(type(self)))
    
    def invoke_py_f(
            self,
            method_name : str,
            args : tuple) -> object:
        """Called by the HDL environment to invoke a Python function"""
        m = getattr(self.target, method_name, None)

        if m is None:
            raise Exception("Failed to find method %s" % method_name)

        return m(*args)

    def invoke_py_t(
            self,
            method_name : str,
            args : tuple) -> int:
        pass

    def response_py_t(
            self,
            call_id : int,
            result : object):
        raise NotImplementedError("CallProxy.response_py_t: %s" % str(type(self)))

