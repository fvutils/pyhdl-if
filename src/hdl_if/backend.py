#****************************************************************************
#* backend.py
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

class Backend(object):

    _inst = None

    def __init__(self):
        pass

    def mkEvent(self):
        raise NotImplementedError("mkEvent (class %s)" % str(type(self)))
    
    def mkLock(self):
        raise NotImplementedError("mkLock (class %s)" % str(type(self)))
    
    def mkSemaphore(self):
        raise NotImplementedError("mkSemaphore (class %s)" % str(type(self)))
    
    def mkTask(self, coro):
        raise NotImplementedError("mkTask (class %s)" % str(type(self)))
    
    def idle(self):
        #raise NotImplementedError("idle (class %s)" % str(type(self)))
        print("idle", flush=True)

    def callCallback(self, cb):
        raise NotImplementedError("callCallback (class %s)" % str(type(self)))
    
    @classmethod
    def inst(cls, inst=None):
        if inst is not None:
            cls._inst = inst
        elif cls._inst is None:
            import sys
            if "cocotb" in sys.modules.keys():
                from .impl.pi.backend_cocotb import BackendCocotb
                return BackendCocotb()
            else:
                from .impl.pi.backend_asyncio import BackendAsyncio
                return BackendAsyncio()

        return cls._inst

