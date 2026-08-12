#****************************************************************************
#* hdl_services.py
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
"""Simulator services available to Python."""

from typing import Dict, List

class HdlServices(object):
    """Services the running simulator provides to Python.

    Each foreign interface -- DPI, VPI -- registers an implementation at
    startup, so this is the seam between Python and simulator-specific
    facilities such as time callbacks. Reach the active one with :meth:`inst`.

    Args:
        name: The name this implementation registers under, e.g. ``"dpi"``.
    """

    _impl : List['HdlServices'] = []
    _impl_m : Dict[str, 'HdlServices'] = {}

    def __init__(self, name):
        self.name = name

    def registerTimeCB(self, cb : callable, time_ps : int) -> object:
        """Schedule a callback at a simulation time.

        Args:
            cb: The callback to invoke.
            time_ps: Delay from now, in picoseconds.

        Returns:
            A handle identifying the scheduled callback.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("registerTimeCB for %s" % str(type(self)))

    @classmethod
    def registerServices(cls, services):
        """Register a services implementation.

        Called by a foreign-interface backend during startup.

        Args:
            services: The implementation to register.
        """
        cls._impl.append(services)
        cls._impl_m[services.name] = services

    @classmethod
    def inst(cls, name=None):
        """Return a registered services implementation.

        Args:
            name: The implementation to return. Defaults to the first
                registered, which is the right one in a single-simulator run.

        Returns:
            The requested :class:`HdlServices`.

        Raises:
            Exception: If nothing has registered yet, which means the
                simulator-side startup has not run.
            KeyError: If ``name`` names no registered implementation.
        """
        if len(cls._impl) == 0:
            raise Exception("No services registered yet")
        if name is None:
            return cls._impl[0]
        else:
            return cls._impl_m[name]

