#****************************************************************************
#* tlm_method.py
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
"""Declaration of a single FIFO-backed TLM method."""

from enum import Enum, auto

class TlmMethodKind(Enum):
    """The direction of data flow through a TLM method.

    Attributes:
        Req: Outbound only -- see :func:`~hdl_if.decorators.req_fifo`.
        Rsp: Inbound only -- see :func:`~hdl_if.decorators.rsp_fifo`.
        ReqRsp: Paired request and response -- see
            :func:`~hdl_if.decorators.reqrsp_fifo`.
    """
    Req = auto()
    Rsp = auto()
    ReqRsp = auto()


class TlmMethod(object):
    """One FIFO-backed method of a TLM interface.

    Created when a method is decorated, and collected by
    :func:`~hdl_if.decorators.tlm_if` into the interface's type info. The
    payload types are what the generated SystemVerilog FIFO widths are derived
    from.

    Args:
        name: The method name.
        kind: The method's :class:`TlmMethodKind`.
        t1: The request payload type, or None for a response-only method.
        t2: The response payload type, or None for a request-only method.
    """

    def __init__(self, name, kind, t1, t2):
        self.name = name
        self.kind = kind
        self.t1 = t1
        self.t2 = t2

