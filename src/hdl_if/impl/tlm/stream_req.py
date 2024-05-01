#****************************************************************************
#* stream_req.py
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
from .stream import Stream, StreamKind

class StreamReq(Stream):

    def __init__(self, name):
        super().__init__(StreamKind.Req, name)

    async def put(self, obj):
        dat_arr = bytes(obj)
        data = 0
        for d in reversed(dat_arr):
            data <<= 8
            data |= d

        # TODO: Check if this is a valid object
        print("put::data 0x%08x" % data, flush=True)
        await self.proxy.invoke_hdl_t(
            "put",
            (data,)
        )

