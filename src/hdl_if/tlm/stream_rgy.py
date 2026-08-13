#****************************************************************************
#* stream_rgy.py
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
"""Registry of TLM streams discovered in the HDL hierarchy."""

from hdl_if.impl.typeinfo import TypeInfo
from typing import List
from hdl_if.impl.tlm.type_info_tlm_if import TypeInfoTlmIF
from hdl_if.impl.tlm.stream import Stream

"""Registry of TLM streams discovered in the HDL hierarchy."""


class StreamRgy(object):
    """Maps HDL instance paths to the TLM streams found beneath them.

    The SystemVerilog TLM FIFOs register themselves here as they elaborate.
    :meth:`connect_if` then binds a Python
    :func:`~hdl_if.decorators.tlm_if` object to the streams at a given path,
    matching them up by method name.

    Reach the singleton with :meth:`inst`.
    """

    _inst = None

    def __init__(self):
        self._stream_m = {}
        self._stream_l : List[str] = []
        self._is_init = False
        pass

    async def initialize(self):
        """Wait until stream registration has settled.

        Streams register during elaboration, so this yields until the
        registered count stops growing before any binding is attempted. Safe
        to call more than once -- subsequent calls return immediately.
        """
        if not self._is_init:
            from hdl_if.backend import Backend
            be = Backend.inst()

            stream_c = len(self._stream_m)
            for _ in range(16):
                ev = be.mkEvent()

                if stream_c == len(self._stream_m):
                    break

            # TODO: Run a few delta cycles ...
            self._is_init = True

    def get_interfaces(self) -> List[str]:
        """Return the HDL paths that have registered streams."""
        return self._stream_l


    def register_stream(self, s : Stream):
        """Register a stream under its enclosing scope.

        The stream's own name is trimmed from its full path, so every stream
        of one interface groups under the same path.

        Args:
            s: The stream to register.
        """
        path = s.fullname
        last_dot = path.rfind('.')
        if last_dot != -1:
            path = path[:last_dot]

        if path in self._stream_m.keys():
            self._stream_m[path].append(s)
        else:
            self._stream_m[path] = [s]
            self._stream_l.append(path)

    async def connect_if(self, ifc, path, match):
        """Bind a Python TLM interface object to the streams at an HDL path.

        Each method declared on the interface is matched by name to a
        registered stream, and the binding recorded on the object's model.

        Args:
            ifc: The :func:`~hdl_if.decorators.tlm_if` object to bind.
            path: The HDL instance path holding the streams.
            match: Reserved for pattern-based matching. Currently a True value
                makes this a no-op.

        Raises:
            Exception: If the path has no registered streams, or a declared
                method has no stream of the same name.
        """
        ifcs = None
        if not match:
            if path not in self._stream_m.keys():
                raise Exception("Path %s isn't a known TLM interface" % path)
            ifcs = self._stream_m[path]

            if_type_info = TypeInfoTlmIF.get(TypeInfo.get(type(ifc)))
            print("ifcs: %s" % str(ifcs), flush=True)
            for m in if_type_info._if_method_l:
                if_t = None
                for i in ifcs:
                    if m.name == i.name:
                        if_t = i
                        break
                if if_t is None:
                    avail = "["
                    for ii,i in enumerate(ifcs):
                        if ii:
                            avail += ", "
                        avail += i.name
                    avail += "]"
                    raise Exception("Failed to find method %s (avail: %s)" % (
                        m.name,
                        avail))

                ifc._model._if_m[m.name] = if_t
            
        else:
            pass

    @classmethod
    def inst(cls):
        """Return the registry singleton, creating it on first use."""
        if cls._inst is None:
            cls._inst = StreamRgy()
        return cls._inst

