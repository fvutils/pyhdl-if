#****************************************************************************
#* tlm_ifc_rgy.py
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

"""Registry of declared TLM interfaces."""


class TlmIfcRgy(object):
    """Collects every class decorated with :func:`~hdl_if.decorators.tlm_if`.

    ``hdl_if ifc-gen-sv`` reads this registry to emit the matching
    SystemVerilog, so an interface must have been imported before generation
    runs. Reach the singleton with :meth:`inst`.
    """

    _inst = None

    def __init__(self):
        self.tlm_ifcs = []

    def addTlmIf(self, tlm_ifc):
        """Register a TLM interface.

        Args:
            tlm_ifc: The interface type info to register.
        """
        self.tlm_ifcs.append(tlm_ifc)

    def getTlmIfcs(self):
        """Return every registered interface, in declaration order."""
        return self.tlm_ifcs

    @classmethod
    def inst(cls):
        """Return the registry singleton, creating it on first use."""
        if cls._inst is None:
            cls._inst = TlmIfcRgy()
        return cls._inst

    @classmethod
    def reset(cls):
        """Discard the singleton and its registrations.

        Intended for tests, which need a clean registry per case.
        """
        cls._inst = None
