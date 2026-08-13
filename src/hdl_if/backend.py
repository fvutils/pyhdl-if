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

"""Abstraction over the event loop PyHDL-IF runs on."""


class Backend(object):
    """Supplies the concurrency primitives PyHDL-IF builds on.

    PyHDL-IF runs either on its own asyncio loop or inside cocotb's scheduler,
    and the two provide different event, lock and task primitives. Code that
    needs one asks the backend rather than importing ``asyncio`` directly, so
    it works under both.

    You rarely construct a backend. Use :meth:`inst` -- or
    :func:`hdl_if.get_backend` -- to reach the active one. Subclasses
    implement the factory methods; the base class raises
    :class:`NotImplementedError` for each.
    """

    _inst = None

    def __init__(self):
        pass

    def mkEvent(self):
        """Create a backend-appropriate event object.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("mkEvent (class %s)" % str(type(self)))

    def mkLock(self):
        """Create a backend-appropriate lock.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("mkLock (class %s)" % str(type(self)))

    def mkSemaphore(self):
        """Create a backend-appropriate semaphore.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("mkSemaphore (class %s)" % str(type(self)))

    def mkTask(self, coro):
        """Schedule a coroutine as a task on the backend's loop.

        Args:
            coro: The coroutine to schedule.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("mkTask (class %s)" % str(type(self)))

    def idle(self):
        """Yield control to the backend's scheduler."""
        #raise NotImplementedError("idle (class %s)" % str(type(self)))
        print("idle", flush=True)

    def callCallback(self, cb):
        """Invoke a callback in the backend's execution context.

        Args:
            cb: The callback to invoke.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("callCallback (class %s)" % str(type(self)))

    @classmethod
    def inst(cls, inst=None):
        """Return the active backend, or install a specific one.

        With no argument, returns the current backend, selecting one on first
        use: cocotb's if ``cocotb`` is already imported, otherwise the asyncio
        backend.

        Args:
            inst: A backend to install as the singleton. Pass this to override
                automatic selection, before anything else touches the backend.

        Returns:
            The active :class:`Backend`.

        Note:
            When no backend has been installed, each call constructs a *new*
            auto-selected backend rather than caching one. Install an instance
            explicitly if you need a stable identity.
        """
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

