#****************************************************************************
#* tlm_ifc.py
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
"""Type information for a declared TLM interface."""

from hdl_if.impl.tlm.type_info_tlm_if import TypeInfoTlmIF

class TlmIfc(TypeInfoTlmIF):
    """Describes a class decorated with :func:`~hdl_if.decorators.tlm_if`.

    Carries the interface's name and the FIFO methods declared inside it,
    which is what the SystemVerilog interface package is generated from.

    Args:
        ti: Type info for the decorated class.
        qname: The class's fully-qualified name. The leaf name becomes
            :attr:`name`.
    """

    def __init__(self, ti, qname):
        super().__init__(ti)
        self.ti = ti
        self.qname = qname
        self.name = qname
        ld = self.name.rfind('.')
        if ld != -1:
            self.name = self.name[ld+1:]

    def getMethods(self):
        """Return the interface's :class:`~hdl_if.tlm.tlm_method.TlmMethod` list."""
        return self._if_method_l

    @staticmethod
    def get(T) -> 'TlmIfc':
        """Return the TLM type info for a decorated class.

        Args:
            T: A class decorated with :func:`~hdl_if.decorators.tlm_if`.

        Returns:
            The interface's type info.
        """
        from hdl_if.impl.typeinfo import TypeInfo
        return TypeInfoTlmIF.get(TypeInfo.get(T))

