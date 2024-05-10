#****************************************************************************
#* backend_cocotb.py
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
from hdl_if.backend import Backend

class BackendCocotb(Backend):

    def __init__(self):
        super().__init__()
        pass

    def mkEvent(self):
        from cocotb.triggers import Event
        return Event()
    
    def mkLock(self):
        from cocotb.triggers import Lock
        return Lock()
    
    def mkSemaphore(self):
        raise NotImplementedError("mkSemaphore (class %s)" % str(type(self)))
    
    def mkTask(self, coro):
        import cocotb
        return cocotb.create_task(coro)

