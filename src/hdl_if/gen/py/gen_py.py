#****************************************************************************
#* gen_py.py
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
"""Generates the Python half of a type universe.

The module contains, in order: an ``IntEnum`` per enum, a dataclass per
record, a reference class per record (``<rec>_sv_ref``), a ``Protocol`` per
interface, and the proxy (``<i>_sv_proxy``) and adapter (``<i>_py_adapter``)
for each interface. Definitions that already exist in Python (``py_ref``)
are imported instead of generated.

The output is valid on Python 3.9 and is deterministic.
"""
from typing import Dict, List

from ..ir import (
    ScalarT, BoolT, RealT, StrT, BytesT, EnumRef, RecordRef, ListT, IfRef,
    EnumDef, RecordDef, InterfaceDef, MethodDef, TypeUniverse, IrError,
)
from ..naming import GEN_VERSION, mangle, check_names
from ...rt_api import PYHDL_IF_RT_API_VERSION

_STD_INTS = {8, 16, 32, 64}


class _Out(object):
    def __init__(self):
        self.lines = []

    def __call__(self, line=""):
        self.lines.append(line)

    def text(self):
        return "\n".join(self.lines).rstrip() + "\n"


class PyGen(object):

    def __init__(self, u: TypeUniverse, source: str):
        self.u = u
        self.source = source
        self.convs: Dict[str, str] = {}      # var name -> hint expression
        self.conv_keys: Dict[str, str] = {}  # var name -> type spelling
        self.rt_names = set()                # names imported from hdl_if.rt
        self.wide_aliases: Dict[str, str] = {}

    # -- types -------------------------------------------------------------
    def hint(self, t) -> str:
        """Python type hint for an IR type."""
        if isinstance(t, ScalarT):
            name = "%s%d" % ("i" if t.signed else "u", t.width)
            if t.width in _STD_INTS:
                self.rt_names.add(name)
            else:
                self.wide_aliases[name] = "_typing.Annotated[int, _rt.IntT(%d, %s)]" % (
                    t.width, t.signed)
            return name
        if isinstance(t, BoolT):
            return "bool"
        if isinstance(t, RealT):
            return "float"
        if isinstance(t, StrT):
            return "str"
        if isinstance(t, BytesT):
            return "bytes"
        if isinstance(t, ListT):
            return "list[%s]" % self.hint(t.elem)
        if isinstance(t, RecordRef):
            if t.by_ref:
                self.rt_names.add("Ref")
                return "Ref[%s]" % t.name
            return t.name
        if isinstance(t, (EnumRef, IfRef)):
            return t.name
        raise IrError("Unknown type %s" % str(t))

    def conv(self, t) -> str:
        """Name of the module-level converter for an IR type."""
        name = "_c_" + mangle(t)
        from ..ir import type_str
        key = type_str(t)
        if name in self.conv_keys and self.conv_keys[name] != key:
            raise IrError("Types '%s' and '%s' have the same generated name %s" % (
                key, self.conv_keys[name], name))
        self.conv_keys[name] = key
        self.convs[name] = self.hint(t)
        return name

    def default(self, t) -> str:
        if isinstance(t, ScalarT):
            return "0"
        if isinstance(t, BoolT):
            return "False"
        if isinstance(t, RealT):
            return "0.0"
        if isinstance(t, StrT):
            return '""'
        if isinstance(t, BytesT):
            return 'b""'
        if isinstance(t, EnumRef):
            e = self.u.enum(t.name)
            return "%s.%s" % (t.name, e.values[0][0])
        if isinstance(t, RecordRef):
            return "_dc.field(default_factory=%s)" % t.name
        if isinstance(t, ListT):
            return "_dc.field(default_factory=list)"
        raise IrError("No default for %s" % str(t))

    # -- module ------------------------------------------------------------
    def generate(self) -> str:
        self.u.validate()
        check_names(self.u)
        order = self.u.dep_order()
        enums = [d for d in order if isinstance(d, EnumDef)]
        records = [d for d in order if isinstance(d, RecordDef)]
        ifaces = [d for d in order if isinstance(d, InterfaceDef)]

        body = _Out()
        for e in enums:
            self.gen_enum(body, e)
        for r in records:
            self.gen_record(body, r)
        for r in records:
            self.gen_sv_ref(body, r)
        for i in ifaces:
            self.gen_protocol(body, i)
        for i in ifaces:
            self.gen_sv_proxy(body, i)
            self.gen_py_adapter(body, i)

        if ifaces:
            body()
            for i in ifaces:
                body("_rt.register_interface(%s, %s_sv_proxy, %s_py_adapter)" % (
                    i.name, i.name, i.name))
        if self.convs:
            body()
            for name in sorted(self.convs.keys()):
                body("%s = _rt.conv_for(%s)" % (name, self.convs[name]))

        out = _Out()
        out("# Generated by pyhdl-if (generator version %d). Do not edit." % GEN_VERSION)
        out("# Source: %s" % self.source)
        out("# pyhdl-if runtime API version: %d" % PYHDL_IF_RT_API_VERSION)
        out('"""Records and interfaces generated from %s."""' % self.source)
        out("from __future__ import annotations")
        out()
        out("import dataclasses as _dc")
        out("import enum as _enum")
        out("import typing as _typing")
        out()
        out("from hdl_if import rt as _rt")
        if self.rt_names:
            out("from hdl_if.rt import %s" % ", ".join(sorted(self.rt_names)))
        imports = self.py_ref_imports()
        for line in imports:
            out(line)
        out()
        out("_rt.check_rt_api_version(%d, __name__)" % PYHDL_IF_RT_API_VERSION)
        if self.wide_aliases:
            out()
            for name in sorted(self.wide_aliases.keys()):
                out("%s = %s" % (name, self.wide_aliases[name]))
        out.lines.extend(body.lines)
        return out.text()

    def py_ref_imports(self) -> List[str]:
        ret = []
        for d in self.u.enums + self.u.records + self.u.interfaces:
            if d.py_ref is None:
                continue
            mod, _, cls = d.py_ref.rpartition(".")
            if mod == "":
                raise IrError("%s: py_ref '%s' must be module.Class" % (d.name, d.py_ref))
            if cls == d.name:
                ret.append("from %s import %s" % (mod, cls))
            else:
                ret.append("from %s import %s as %s" % (mod, cls, d.name))
        return sorted(ret)

    # -- enums -------------------------------------------------------------
    def gen_enum(self, out, e: EnumDef):
        if e.py_ref is not None:
            return
        out()
        out()
        out("class %s(_enum.IntEnum):" % e.name)
        out('    """Enum ``%s``."""' % e.name)
        for n, v in e.values:
            out("    %s = %d" % (n, v))

    # -- records -----------------------------------------------------------
    def gen_record(self, out, r: RecordDef):
        if r.py_ref is not None:
            # Still record the converters the reference class needs
            for f in self.u.all_fields(r):
                self.hint(f.type)
            return
        out()
        out()
        out("@_dc.dataclass")
        out("class %s(%s):" % (r.name, r.base if r.base is not None else "object"))
        out('    """Record ``%s``."""' % r.name)
        for f in r.fields:
            out("    %s: %s = %s" % (f.name, self.hint(f.type), self.default(f.type)))
        if r.base is None:
            out()
            out("    def copy(self) -> %s:" % r.name)
            out('        """Return a deep copy."""')
            out("        return _rt.copy(self)")

    def gen_sv_ref(self, out, r: RecordDef):
        out()
        out()
        base = ("%s_sv_ref" % r.base) if r.base is not None else "_rt.SvRef"
        out("class %s_sv_ref(%s):" % (r.name, base))
        out('    """Reference to an SV ``%s``. Each field access calls SV."""' % r.name)
        out("    __slots__ = ()")
        out("    _rec_type = %s" % r.name)
        for f in r.fields:
            t = f.type
            c = self.conv(t)
            out()
            out("    @property")
            if isinstance(t, RecordRef):
                out("    def %s(self) -> %s_sv_ref:" % (f.name, t.name))
                out('        return self._call_f("get_%s", ())' % f.name)
            else:
                out("    def %s(self) -> %s:" % (f.name, self.hint(t)))
                out('        return %s.from_sv(self._call_f("get_%s", ()))' % (c, f.name))
            out()
            out("    @%s.setter" % f.name)
            out("    def %s(self, v: %s):" % (f.name, self.hint(t)))
            out('        self._call_f("set_%s", (%s.to_sv(v),))' % (f.name, c))

    # -- interfaces --------------------------------------------------------
    def sig(self, m: MethodDef, typed: bool) -> str:
        params = ["self"]
        for p in m.params:
            if typed:
                params.append("%s: %s" % (p.name, self.hint(p.type)))
            else:
                params.append(p.name)
        ret = ""
        if typed:
            ret = " -> %s" % (self.hint(m.rtype) if m.rtype is not None else "None")
        return "%sdef %s(%s)%s:" % (
            "async " if m.is_task else "", m.name, ", ".join(params), ret)

    @staticmethod
    def _tuple(items: List[str]) -> str:
        if len(items) == 1:
            return "(%s,)" % items[0]
        return "(%s)" % ", ".join(items)

    def gen_protocol(self, out, i: InterfaceDef):
        if i.py_ref is not None:
            for m in i.methods:
                self.sig(m, True)
            return
        out()
        out()
        out("class %s(_typing.Protocol):" % i.name)
        out('    """Interface ``%s``."""' % i.name)
        if len(i.methods) == 0:
            out("    pass")
        for m in i.methods:
            out()
            out("    %s ..." % self.sig(m, True))

    def gen_sv_proxy(self, out, i: InterfaceDef):
        out()
        out()
        out("class %s_sv_proxy(_rt.SvProxy):" % i.name)
        out('    """Calls an SV implementation of ``%s``."""' % i.name)
        out("    __slots__ = ()")
        for m in i.methods:
            args = self._tuple(["%s.to_sv(%s)" % (self.conv(p.type), p.name) for p in m.params]) \
                if m.params else "()"
            if m.is_task:
                call = 'await self._call_t("%s", %s)' % (m.name, args)
            else:
                call = 'self._call_f("%s", %s)' % (m.name, args)
            out()
            out("    %s" % self.sig(m, True))
            if m.rtype is not None:
                out("        return %s.from_sv(%s)" % (self.conv(m.rtype), call))
            else:
                out("        %s" % call)

    def gen_py_adapter(self, out, i: InterfaceDef):
        out()
        out()
        out("class %s_py_adapter(_rt.PyAdapter):" % i.name)
        out('    """Lets SV call a Python implementation of ``%s``."""' % i.name)
        out("    __slots__ = ()")
        for m in i.methods:
            args = ", ".join("%s.from_sv(%s)" % (self.conv(p.type), p.name) for p in m.params)
            call = "self._impl.%s(%s)" % (m.name, args)
            if m.is_task:
                call = "await " + call
            out()
            out("    %s" % self.sig(m, False))
            if m.rtype is not None:
                out("        return %s.to_sv(%s)" % (self.conv(m.rtype), call))
            else:
                out("        %s" % call)


def gen_py(u: TypeUniverse, source: str) -> str:
    """Return the Python module for ``u``.

    Args:
        u: The definitions.
        source: Names the input, for the file header.
    """
    return PyGen(u, source).generate()
