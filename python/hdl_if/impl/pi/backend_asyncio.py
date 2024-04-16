#****************************************************************************
#* backend_asyncio.py
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
import asyncio
from hdl_if.backend import Backend

class Event(asyncio.Event):
    def __init__(self):
        super().__init__()
        self.val = None

    def set(self, val) -> None:
        be = Backend.inst();
        self.val = val
        super().set()
        be.idle()

    async def wait(self):
        await super().wait()
        return self.val

class BackendAsyncio(Backend):

    def __init__(self):
        super().__init__()
        self._loop = asyncio.get_event_loop()
        pass

    def mkTask(self, coro):
        print("mkTask", flush=True)
        return asyncio.ensure_future(coro)

    def mkEvent(self):
        return Event()
    
    def mkLock(self):
        return asyncio.Lock()
    
    def mkSemaphore(self):
        return asyncio.Semaphore()
    
    def __soon_cb(self):
        self._loop.stop()

    def idle(self):
        self._loop.call_soon(self.__soon_cb)
        self._loop.run_forever()

    def callCallback(self, cb):
        cb()
        self.idle()

