#****************************************************************************
#* naming.py
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
"""Names of generated classes and functions, shared by both back ends.

For record ``r``:

* ``r`` -- the value type (SV class, Python dataclass)
* ``r_if`` -- SV accessor interface class
* ``r_py_ref`` -- SV reference to a Python ``r``
* ``r_sv_ref`` -- Python reference to an SV ``r``
* ``r_sv_adapter`` -- SV receiver of calls on an ``r_sv_ref``
* ``r_sv_wrap`` -- SV accessor wrapper, for an existing SV class
* ``r_to_py``, ``r_from_py``, ``r_ref_to_py``, ``r_ref_from_py``,
  ``r_copy``, ``r_from_if``, ``r_wrap`` -- SV package functions

For interface ``i``:

* ``i`` -- SV interface class, Python Protocol
* ``i_sv_proxy`` -- Python caller of an SV implementation
* ``i_py_adapter`` -- Python receiver of calls on a Python implementation
* ``i_sv_adapter`` -- SV receiver of calls on an SV implementation
* ``i_py_proxy`` -- SV caller of a Python implementation
* ``i_to_py``, ``i_from_py`` -- SV package functions
"""
import re

from .ir import ScalarT, BoolT, RealT, StrT, TypeUniverse, IrError, type_str

#: Version of the generated code's shape. Bumped when generated output
#: changes for the same input, independent of the pyhdl-if version, so that
#: upgrading pyhdl-if alone does not make checked-in code look stale.
GEN_VERSION = 1

RECORD_SUFFIXES = (
    "_if", "_py_ref", "_sv_ref", "_sv_adapter", "_sv_wrap",
    "_to_py", "_from_py", "_ref_to_py", "_ref_from_py", "_copy", "_from_if",
    "_wrap",
)
INTERFACE_SUFFIXES = (
    "_sv_proxy", "_py_adapter", "_sv_adapter", "_py_proxy", "_to_py", "_from_py",
)

_BUILTIN_TYPE_RE = re.compile(r"^([ui]\d+|bool|f32|f64|str|bytes|list|ref)$")


def mangle(t) -> str:
    """Return an identifier-safe spelling of a type, for generated names."""
    return re.sub(r"[^A-Za-z0-9]+", "_", type_str(t)).strip("_")


def generated_names(u: TypeUniverse):
    """Return ``{generated name: definition name}`` for every definition."""
    ret = {}
    for r in u.records:
        for s in RECORD_SUFFIXES:
            ret[r.name + s] = r.name
    for i in u.interfaces:
        for s in INTERFACE_SUFFIXES:
            ret[i.name + s] = i.name
    return ret


def check_names(u: TypeUniverse):
    """Raise :class:`IrError` if a definition's name clashes with a
    generated name or a type spelling."""
    gen = generated_names(u)
    for d in u.enums + u.records + u.interfaces:
        if _BUILTIN_TYPE_RE.match(d.name):
            raise IrError("'%s' cannot be used as a name: it is a type spelling" % d.name)
        if d.name in gen and gen[d.name] != d.name:
            raise IrError("'%s' clashes with a name generated for '%s'" % (
                d.name, gen[d.name]))
    # SV enum value names share the package namespace
    seen = {}
    for e in u.enums:
        for n, _ in e.values:
            if n in gen or u.get(n) is not None:
                raise IrError("enum %s value %s clashes with another name" % (e.name, n))
            if n in seen:
                raise IrError("enum %s value %s clashes with a value of enum %s" % (
                    e.name, n, seen[n]))
            seen[n] = e.name


def is_direct(t) -> bool:
    """True if a field of this type is read and written on a Python object
    as its plain value (no payload conversion needed)."""
    if isinstance(t, ScalarT):
        return t.width <= 64
    return isinstance(t, (BoolT, RealT, StrT))
