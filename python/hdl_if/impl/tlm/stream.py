#****************************************************************************
#* stream.py
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
from enum import Enum, auto

class StreamKind(Enum):
    Req = auto()
    Rsp = auto()
    ReqRsp = auto()

class Stream(object):

    def __init__(self, kind, name):
        self.kind = kind
        if name.endswith(".fifo_reg"):
            name = name[:name.rfind(".")]
        self.fullname = name
        self.name = name[name.rfind('.')+1:]

    @property
    def proxy(self) -> CallProxy:
        return getattr(self, "_proxy")

