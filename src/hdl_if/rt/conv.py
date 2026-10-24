#****************************************************************************
#* conv.py
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
"""Conversion between Python values and the payloads SystemVerilog exchanges.

Generated SystemVerilog never builds or reads a Python dataclass directly. It
builds a *payload* out of plain Python values, and this module converts the
payload to and from the typed Python value, driven by the type hint:

=====================  ==========================================
Hint                   Payload
=====================  ==========================================
int, sized int <= 64   ``int``
sized int > 64         hex ``str`` (two's complement, no prefix)
bool                   ``bool``
float                  ``float``
str                    ``str``
bytes                  ``list`` of ``int`` (0-255)
``IntEnum`` subclass   ``int``
dataclass (copy)       ``tuple`` of field payloads, or ``None``
``Ref[dataclass]``     the object itself
``List[T]``            ``list`` of ``T`` payloads
interface              the object (see :func:`register_interface`)
=====================  ==========================================

Keeping the payload format behind :func:`rec_from_sv` / :func:`rec_to_sv`
means it can change without regenerating code.
"""
import ctypes
import dataclasses as dc
import enum
import typing
from typing import Any, Callable, Dict, Tuple

from .types import IntT, RefMarker

__all__ = [
    "Conv", "conv_for", "rec_from_sv", "rec_to_sv", "copy",
    "register_interface", "interface_info", "get_field", "set_field",
    "py_adapt",
]


class Conv(object):
    """Converts one type between its Python value and its payload.

    Attributes:
        to_sv: Python value -> payload.
        from_sv: payload -> Python value.
    """
    __slots__ = ("to_sv", "from_sv", "hint")

    def __init__(self, hint, to_sv: Callable, from_sv: Callable):
        self.hint = hint
        self.to_sv = to_sv
        self.from_sv = from_sv


def _ident(v):
    return v


_CTYPES_INT = {
    ctypes.c_int8: IntT(8, True),
    ctypes.c_uint8: IntT(8, False),
    ctypes.c_int16: IntT(16, True),
    ctypes.c_uint16: IntT(16, False),
    ctypes.c_int32: IntT(32, True),
    ctypes.c_uint32: IntT(32, False),
    ctypes.c_int64: IntT(64, True),
    ctypes.c_uint64: IntT(64, False),
}

# Protocol class -> (sv_proxy class, py_adapter class)
_interfaces: Dict[type, Tuple[type, type]] = {}

_conv_cache: Dict[Any, Conv] = {}


def register_interface(iface: type, sv_proxy: type, py_adapter: type):
    """Register the generated classes for an interface.

    Generated modules call this at import time, so a value whose hint is
    ``iface`` can be passed across: a Python implementation is wrapped in
    ``py_adapter``, and an SV implementation arrives as an ``sv_proxy``.

    Args:
        iface: The interface (a ``typing.Protocol``).
        sv_proxy: Generated class that forwards calls to an SV implementation.
        py_adapter: Generated class that receives calls from SV and forwards
            them to a Python implementation.
    """
    _interfaces[iface] = (sv_proxy, py_adapter)
    _conv_cache.pop(iface, None)


def interface_info(iface: type):
    """Return ``(sv_proxy, py_adapter)`` for a registered interface, or None."""
    return _interfaces.get(iface, None)


def int_info(hint):
    """Return the :class:`IntT` for an integer hint, or None if not one."""
    if typing.get_origin(hint) is typing.Annotated:
        base = hint.__origin__
        for m in hint.__metadata__:
            if isinstance(m, IntT) and base is int:
                return m
        return None
    if hint is int:
        return IntT(64, True)
    if hint in _CTYPES_INT:
        return _CTYPES_INT[hint]
    return None


def is_ref(hint) -> bool:
    """True if ``hint`` is ``Ref[...]``."""
    if typing.get_origin(hint) is typing.Annotated:
        return any(isinstance(m, RefMarker) for m in hint.__metadata__)
    return False


def strip_annotated(hint):
    """Return the hint inside ``Annotated[...]``, or ``hint`` itself."""
    if typing.get_origin(hint) is typing.Annotated:
        return hint.__origin__
    return hint


def strip_optional(hint):
    """Return ``X`` for ``Optional[X]``, or ``hint`` itself."""
    if typing.get_origin(hint) is typing.Union:
        args = [a for a in typing.get_args(hint) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return hint


def conv_for(hint) -> Conv:
    """Return the converter for a type hint.

    Converters are cached, and a dataclass's field converters are built on
    first use, so recursive and forward-referenced records work.

    Raises:
        TypeError: If the hint has no SystemVerilog equivalent.
    """
    try:
        return _conv_cache[hint]
    except KeyError:
        pass
    except TypeError:
        # Unhashable hint; build without caching
        return _mk_conv(hint)
    c = _mk_conv(hint)
    _conv_cache[hint] = c
    return c


def _mk_conv(hint) -> Conv:
    hint = strip_optional(hint)

    if hint is None or hint is type(None):
        return Conv(hint, _ident, _ident)

    if is_ref(hint):
        # The object itself crosses; None stays None
        return Conv(hint, _ident, _ident)

    ii = int_info(hint)
    if ii is not None:
        if ii.width <= 64:
            return Conv(hint, int, int)
        return _mk_wide_int_conv(hint, ii)

    hint = strip_annotated(hint)

    if hint is bool:
        return Conv(hint, bool, bool)
    if hint is float:
        return Conv(hint, float, float)
    if hint is str:
        return Conv(hint, str, str)
    if hint is bytes:
        return Conv(hint, list, bytes)

    origin = typing.get_origin(hint)
    if origin in (list, typing.List):
        args = typing.get_args(hint)
        if len(args) != 1:
            raise TypeError("List hint %s must have one element type" % str(hint))
        return _mk_list_conv(hint, args[0])

    if isinstance(hint, type):
        if issubclass(hint, enum.IntEnum):
            def enum_from_sv(v, _cls=hint):
                return _cls(v)
            return Conv(hint, int, enum_from_sv)
        if dc.is_dataclass(hint):
            return _mk_record_conv(hint)
        if hint in _interfaces:
            return _mk_interface_conv(hint)

    raise TypeError("Type %s has no SystemVerilog equivalent" % str(hint))


def _mk_wide_int_conv(hint, ii: IntT) -> Conv:
    mask = (1 << ii.width) - 1
    sign = 1 << (ii.width - 1)

    def to_sv(v):
        return format(int(v) & mask, "x")

    if ii.signed:
        def from_sv(s):
            v = int(s, 16)
            return v - (1 << ii.width) if (v & sign) else v
    else:
        def from_sv(s):
            return int(s, 16)
    return Conv(hint, to_sv, from_sv)


def _mk_list_conv(hint, elem_hint) -> Conv:
    ec = conv_for(elem_hint)

    def to_sv(v):
        f = ec.to_sv
        return [f(e) for e in v]

    def from_sv(v):
        f = ec.from_sv
        return [f(e) for e in v]
    return Conv(hint, to_sv, from_sv)


def _record_fields(cls):
    """Return ``[(name, Conv), ...]`` for a dataclass, in field order."""
    hints = typing.get_type_hints(cls, include_extras=True)
    ret = []
    for f in dc.fields(cls):
        try:
            ret.append((f.name, conv_for(hints[f.name])))
        except TypeError as e:
            raise TypeError("%s.%s: %s" % (cls.__name__, f.name, str(e)))
    return ret


def _mk_record_conv(cls) -> Conv:
    state = {}

    def fields():
        flds = state.get("f", None)
        if flds is None:
            flds = _record_fields(cls)
            state["f"] = flds
        return flds

    def to_sv(v):
        if v is None:
            return None
        if not isinstance(v, cls):
            # A reference to an SV object: take a snapshot first
            copy_m = getattr(v, "copy", None)
            if copy_m is None:
                raise TypeError("Expected %s, got %s" % (
                    cls.__name__, type(v).__name__))
            v = copy_m()
        return tuple(c.to_sv(getattr(v, n)) for n, c in fields())

    def from_sv(p):
        if p is None:
            return None
        return cls(*(c.from_sv(e) for (n, c), e in zip(fields(), p)))
    return Conv(cls, to_sv, from_sv)


def _mk_interface_conv(iface) -> Conv:
    from .obj import SvObj, PyAdapter
    sv_proxy, py_adapter = _interfaces[iface]

    def to_sv(v):
        if v is None or isinstance(v, (SvObj, PyAdapter)):
            return v
        return py_adapter(v)

    def from_sv(v):
        if isinstance(v, PyAdapter):
            return v._impl
        return v
    return Conv(iface, to_sv, from_sv)


_field_cache: Dict[Tuple[type, str], Conv] = {}


def _field_conv(cls, name) -> Conv:
    key = (cls, name)
    c = _field_cache.get(key, None)
    if c is None:
        hints = typing.get_type_hints(cls, include_extras=True)
        if name not in hints:
            raise AttributeError("%s has no field %s" % (cls.__name__, name))
        c = conv_for(hints[name])
        _field_cache[key] = c
    return c


def get_field(obj, name: str):
    """Return the payload of field ``name`` of record ``obj``.

    Used by SV references to Python records, for fields whose payload is not
    the field's value itself.
    """
    return _field_conv(type(obj), name).to_sv(getattr(obj, name))


def set_field(obj, name: str, payload):
    """Set field ``name`` of record ``obj`` from its payload."""
    setattr(obj, name, _field_conv(type(obj), name).from_sv(payload))


def py_adapt(adapter_cls, impl):
    """Return ``impl`` wrapped in ``adapter_cls``, unless it is an adapter.

    Called by the SV runtime when it is handed a Python implementation of an
    interface.
    """
    from .obj import PyAdapter
    if isinstance(impl, PyAdapter):
        return impl
    return adapter_cls(impl)


def rec_from_sv(cls, payload):
    """Build a record of type ``cls`` from an SV payload.

    This is the single entry point SystemVerilog uses to copy a record into
    Python.
    """
    return conv_for(cls).from_sv(payload)


def rec_to_sv(obj):
    """Return the SV payload for a record.

    This is the single entry point SystemVerilog uses to copy a record out of
    Python. ``obj`` may also be a reference to an SV record, in which case
    its current value is copied.
    """
    cls = getattr(type(obj), "_rec_type", None) or type(obj)
    return conv_for(cls).to_sv(obj)


def copy(obj):
    """Return an independent copy of a record or a record reference.

    For a dataclass this is a deep copy. For a reference to an SV record it
    is a snapshot of the SV object's current value.
    """
    copy_m = getattr(obj, "copy", None)
    if copy_m is not None and not dc.is_dataclass(obj):
        return copy_m()
    cls = type(obj)
    c = conv_for(cls)
    return c.from_sv(c.to_sv(obj))
