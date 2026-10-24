#****************************************************************************
#* py.py
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
"""Python front end: builds a :class:`TypeUniverse` from Python declarations.

* A ``@dataclass`` becomes a record. Its fields come from
  ``dataclasses.fields()``; a dataclass base becomes the record's base.
* An ``enum.IntEnum`` becomes an enum. Its width is the smallest of 8, 16,
  32 or 64 bits that holds every value, unless the class sets
  ``__pyhdl_width__``.
* A ``typing.Protocol`` becomes an interface. Its public methods (those not
  starting with ``_``), including those of base protocols, are the
  interface's methods; ``async def`` declares a task.

Type hints map as follows: ``int`` is a signed 64-bit integer; the sized
hints from :mod:`hdl_if.rt` (``u8``, ``i32``, ``uint(N)``...) and the ctypes
integer types give a width; ``bool``, ``float``, ``str``, ``bytes``,
``List[T]``/``list[T]``, ``Optional[T]`` (as ``T``), a dataclass, an
``IntEnum``, a Protocol, and ``Ref[dataclass]`` (by reference) are
supported.

Every definition found this way already exists in Python, so it carries a
``py_ref`` and the Python back end imports it instead of generating it.
"""
import ctypes
import dataclasses as dc
import enum
import fnmatch
import importlib
import inspect
import typing
from typing import Dict, List, Optional

from ..ir import (
    ScalarT, BoolT, RealT, StrT, BytesT, EnumRef, RecordRef, ListT, IfRef,
    EnumDef, FieldDef, RecordDef, ParamDef, MethodDef, InterfaceDef,
    TypeUniverse, IrError,
)
from ...rt.conv import int_info, is_ref, strip_annotated

__all__ = ["PyFrontEnd", "universe_from_py"]

_CTYPES_OTHER = {
    ctypes.c_bool: BoolT(),
    ctypes.c_float: RealT(32),
    ctypes.c_double: RealT(64),
}


def _qualname(cls) -> str:
    return "%s.%s" % (cls.__module__, cls.__qualname__)


def _is_protocol(cls) -> bool:
    return isinstance(cls, type) and getattr(cls, "_is_protocol", False) \
        and cls is not typing.Protocol


def _is_record(cls) -> bool:
    return isinstance(cls, type) and dc.is_dataclass(cls)


def _is_enum(cls) -> bool:
    return isinstance(cls, type) and issubclass(cls, enum.IntEnum) \
        and cls is not enum.IntEnum


class PyFrontEnd(object):
    """Collects definitions from Python classes into a TypeUniverse."""

    def __init__(self):
        self.u = TypeUniverse()
        self._by_cls: Dict[type, str] = {}

    # -- entry points ------------------------------------------------------
    def add_module(self, mod, include=None, exclude=None):
        """Add the dataclasses, IntEnums and Protocols defined in ``mod``.

        Args:
            mod: A module, or its name.
            include: ``fnmatch`` patterns on ``module.Class``; when given,
                only matching classes are added (plus what they use).
            exclude: ``fnmatch`` patterns on ``module.Class`` to skip.
        """
        if isinstance(mod, str):
            try:
                mod = importlib.import_module(mod)
            except Exception as e:
                raise IrError("Failed to import module '%s': %s" % (mod, str(e)))
        for name, obj in sorted(vars(mod).items()):
            if not isinstance(obj, type) or obj.__module__ != mod.__name__:
                continue
            if not (_is_record(obj) or _is_enum(obj) or _is_protocol(obj)):
                continue
            qn = _qualname(obj)
            if include and not any(fnmatch.fnmatch(qn, p) for p in include):
                continue
            if exclude and any(fnmatch.fnmatch(qn, p) for p in exclude):
                continue
            self.add_class(obj)

    def add_class(self, cls) -> str:
        """Add one class (and the classes it refers to). Returns its name."""
        if cls in self._by_cls:
            return self._by_cls[cls]
        if _is_record(cls):
            return self._add_record(cls)
        if _is_enum(cls):
            return self._add_enum(cls)
        if _is_protocol(cls):
            return self._add_protocol(cls)
        raise IrError("%s is not a dataclass, IntEnum or Protocol" % _qualname(cls))

    def _claim(self, cls) -> str:
        name = cls.__name__
        other = self.u.get(name)
        if other is not None:
            raise IrError("Two definitions named '%s': %s and %s" % (
                name, other.py_ref, _qualname(cls)))
        self._by_cls[cls] = name
        return name

    # -- enums -------------------------------------------------------------
    def _add_enum(self, cls) -> str:
        name = self._claim(cls)
        values = [(m.name, int(m.value)) for m in cls]
        signed = any(v < 0 for _, v in values)
        width = getattr(cls, "__pyhdl_width__", None)
        if width is None:
            need = 1
            for _, v in values:
                need = max(need, (v.bit_length() + 1) if signed else max(1, v.bit_length()))
            width = next((w for w in (8, 16, 32, 64) if w >= need), need)
        self.u.add(EnumDef(name, int(width), values, signed=signed, py_ref=_qualname(cls)))
        return name

    # -- records -----------------------------------------------------------
    def _add_record(self, cls) -> str:
        name = self._claim(cls)
        rd = RecordDef(name, py_ref=_qualname(cls))
        self.u.add(rd)

        base_fields = set()
        for b in cls.__mro__[1:]:
            if _is_record(b):
                rd.base = self.add_class(b)
                base_fields = {f.name for f in dc.fields(b)}
                break

        try:
            hints = typing.get_type_hints(cls, include_extras=True)
        except Exception as e:
            raise IrError("%s: cannot resolve type hints: %s" % (_qualname(cls), str(e)))
        for f in dc.fields(cls):
            if f.name in base_fields:
                continue
            what = "%s.%s" % (_qualname(cls), f.name)
            t = self.map_hint(hints.get(f.name, None), what)
            if isinstance(t, RecordRef) and t.by_ref:
                raise IrError("%s: record fields cannot be references (Ref[...])" % what)
            if isinstance(t, IfRef):
                raise IrError("%s: record fields cannot be interfaces" % what)
            rd.fields.append(FieldDef(f.name, t))
        return name

    # -- protocols ---------------------------------------------------------
    def _add_protocol(self, cls) -> str:
        name = self._claim(cls)
        idef = InterfaceDef(name, py_ref=_qualname(cls))
        self.u.add(idef)
        seen = set()
        for c in cls.__mro__:
            if c in (object, typing.Protocol, typing.Generic) or not _is_protocol(c):
                continue
            for mname, m in c.__dict__.items():
                if mname.startswith("_") or mname in seen:
                    continue
                if not inspect.isfunction(m):
                    continue
                seen.add(mname)
                idef.methods.append(self._method(cls, mname, m))
        return name

    def _method(self, cls, mname, func) -> MethodDef:
        what = "%s.%s" % (_qualname(cls), mname)
        try:
            hints = typing.get_type_hints(func, include_extras=True)
        except Exception as e:
            raise IrError("%s: cannot resolve type hints: %s" % (what, str(e)))
        md = MethodDef(mname, is_task=inspect.iscoroutinefunction(func))
        sig = inspect.signature(func)
        for k, (pname, p) in enumerate(sig.parameters.items()):
            if k == 0:
                continue  # self
            if p.kind not in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD):
                raise IrError("%s: parameter %s: only plain positional parameters are supported" % (
                    what, pname))
            if pname not in hints:
                raise IrError("%s: parameter %s has no type annotation" % (what, pname))
            md.params.append(ParamDef(pname, self.map_hint(hints[pname], "%s parameter %s" % (what, pname))))
        rt = hints.get("return", None)
        if rt is not None and rt is not type(None):
            md.rtype = self.map_hint(rt, "%s return" % what)
        return md

    # -- hints -------------------------------------------------------------
    def map_hint(self, hint, what: str):
        """Return the IR type for a Python type hint.

        Raises:
            IrError: If the hint has no SV equivalent; the message names
                ``what``.
        """
        if hint is None:
            raise IrError("%s has no type annotation" % what)
        try:
            return self._map(hint)
        except IrError as e:
            raise IrError("%s: %s" % (what, str(e)))

    def _map(self, hint):
        if typing.get_origin(hint) is typing.Union:
            args = [a for a in typing.get_args(hint) if a is not type(None)]
            if len(args) != 1:
                raise IrError("unions other than Optional[T] are not supported (%s)" % str(hint))
            return self._map(args[0])

        if is_ref(hint):
            target = strip_annotated(hint)
            if not _is_record(target):
                raise IrError("Ref[...] must name a dataclass (got %s)" % str(target))
            return RecordRef(self.add_class(target), by_ref=True)

        ii = int_info(hint)
        if ii is not None:
            return ScalarT(ii.width, ii.signed)

        hint = strip_annotated(hint)
        if hint is bool:
            return BoolT()
        if hint is float:
            return RealT(64)
        if hint is str:
            return StrT()
        if hint is bytes:
            return BytesT()
        if hint in _CTYPES_OTHER:
            return _CTYPES_OTHER[hint]

        origin = typing.get_origin(hint)
        if origin in (list, typing.List):
            args = typing.get_args(hint)
            if len(args) != 1:
                raise IrError("list hint needs an element type (got %s)" % str(hint))
            elem = self._map(args[0])
            if isinstance(elem, IfRef) or (isinstance(elem, RecordRef) and elem.by_ref):
                raise IrError("list elements must be values (got %s)" % str(hint))
            return ListT(elem)

        if _is_enum(hint):
            return EnumRef(self.add_class(hint))
        if _is_record(hint):
            return RecordRef(self.add_class(hint))
        if _is_protocol(hint):
            return IfRef(self.add_class(hint))

        if isinstance(hint, type) and issubclass(hint, enum.Enum):
            raise IrError("enum %s must derive from enum.IntEnum" % hint.__name__)
        raise IrError("type %s has no SystemVerilog equivalent" % getattr(hint, "__name__", str(hint)))


def universe_from_py(modules: List[str],
                     include: Optional[List[str]] = None,
                     exclude: Optional[List[str]] = None) -> TypeUniverse:
    """Build a TypeUniverse from the classes in Python modules.

    Args:
        modules: Module names (or modules) to scan.
        include: Optional ``fnmatch`` patterns on ``module.Class``.
        exclude: Optional ``fnmatch`` patterns on ``module.Class``.
    """
    fe = PyFrontEnd()
    for m in modules:
        fe.add_module(m, include, exclude)
    fe.u.validate()
    return fe.u
