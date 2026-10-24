#****************************************************************************
#* obj.py
#*
#* Copyright 2026 Matthew Ballance and Contributors
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
#****************************************************************************
"""Python objects that stand for SystemVerilog objects, and the reverse.

* :class:`SvRef` -- a reference to an SV record. Generated subclasses expose
  one property per field.
* :class:`SvProxy` -- an SV implementation of an interface. Generated
  subclasses expose one method per interface method.
* :class:`PyAdapter` -- wraps a Python implementation of an interface so SV
  can call it. Generated subclasses convert arguments and results.

An SV object reachable from Python is held in the SV runtime's object table
under an integer id. When the Python object is collected, its id is queued
(:func:`take_released`) and the SV side frees the slot the next time it needs
one. Nothing calls into SV from a finalizer.
"""
import traceback
from typing import ClassVar, Optional

__all__ = [
    "SvObj", "SvRef", "SvProxy", "PyAdapter",
    "set_endpoint", "endpoint", "sv_obj_new", "sv_obj_id",
    "take_released", "invoke_py_t", "ERROR",
]

_endpoint = None
_released = []


class _Error(object):
    """Type of :data:`ERROR`."""
    def __repr__(self):
        return "hdl_if.rt.ERROR"


#: Returned to SV in place of a result when a Python task raised. The
#: traceback has already been printed.
ERROR = _Error()


def set_endpoint(ep):
    """Use ``ep`` for calls into SV. For tests; normally found automatically."""
    global _endpoint
    _endpoint = ep


def endpoint():
    """Return the call endpoint for the running simulator."""
    global _endpoint
    if _endpoint is None:
        from hdl_if.impl.call.context import Context
        eps = Context.inst()._endpoints
        if len(eps) == 0:
            raise RuntimeError("No simulator endpoint: is the simulation running?")
        _endpoint = eps[0]
    return _endpoint


def take_released():
    """Return, and forget, the ids of SV objects Python no longer references.

    Called by the SV runtime before it reuses or grows its object table.
    """
    global _released
    ret = _released
    _released = []
    return ret


class SvObj(object):
    """Base for Python objects that stand for an SV object.

    Instances are created by the SV runtime through :func:`sv_obj_new`, never
    by user code.
    """
    __slots__ = ("_obj_id", "__weakref__")

    @classmethod
    def _from_id(cls, obj_id: int):
        ret = cls.__new__(cls)
        ret._obj_id = obj_id
        return ret

    def _call_f(self, method: str, args: tuple):
        """Call an SV function on the target and return its payload."""
        return endpoint().invoke_hdl_f(self._obj_id, method, args)

    async def _call_t(self, method: str, args: tuple):
        """Call an SV task on the target and return its payload."""
        from hdl_if.backend import Backend
        evt = Backend.inst().mkEvent()
        endpoint().invoke_hdl_t(self._obj_id, evt, method, args)
        return await evt.wait()

    def __del__(self):
        # Must be safe at any time, including after the simulation ended and
        # during interpreter shutdown: only queue the id, never raise.
        try:
            oid = self._obj_id
            if oid >= 0:
                self._obj_id = -1
                _released.append(oid)
        except Exception:
            pass

    def __repr__(self):
        try:
            return "<%s sv-id=%d>" % (type(self).__name__, self._obj_id)
        except Exception:
            return "<%s>" % type(self).__name__


class SvRef(SvObj):
    """A reference to an SV record.

    Reading or writing a field crosses to SV on every access. Use
    :meth:`copy` to take a snapshot as a plain dataclass.
    """
    __slots__ = ()

    #: The record's dataclass. Set by the generated subclass.
    _rec_type: ClassVar[Optional[type]] = None

    def copy(self):
        """Return the record's current value as a new dataclass."""
        from .conv import conv_for
        return conv_for(self._rec_type).from_sv(self._call_f("__copy", ()))


class SvProxy(SvObj):
    """An SV implementation of an interface, callable from Python."""
    __slots__ = ()


class PyAdapter(object):
    """Lets SV call a Python implementation of an interface.

    Args:
        impl: The object that implements the interface's methods.
    """
    __slots__ = ("_impl",)

    def __init__(self, impl):
        self._impl = impl


def sv_obj_new(cls, obj_id: int):
    """Create the Python stand-in of class ``cls`` for SV object ``obj_id``.

    Called by the SV runtime.
    """
    return cls._from_id(obj_id)


def sv_obj_id(obj) -> int:
    """Return the SV object id of ``obj``, or -1 if it is not an SV object.

    Called by the SV runtime to recognize one of its own objects coming back.
    """
    if isinstance(obj, SvObj):
        return obj._obj_id
    return -1


def invoke_py_t(sem_id: int, obj, method: str, args: tuple):
    """Start a Python coroutine method on behalf of an SV task.

    The result is delivered to SV through the call endpoint when the
    coroutine completes. If it raises, the traceback is printed and
    :data:`ERROR` is delivered instead. Called by the SV runtime.
    """
    from hdl_if.backend import Backend
    be = Backend.inst()

    async def run():
        try:
            res = await getattr(obj, method)(*args)
        except BaseException:
            traceback.print_exc()
            res = ERROR
        endpoint().response_py_t(sem_id, res)

    be.mkTask(run())
    be.idle()
