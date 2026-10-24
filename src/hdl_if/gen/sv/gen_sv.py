#****************************************************************************
#* gen_sv.py
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
"""Generates the SystemVerilog half of a type universe: one package.

Per enum: a ``typedef enum``. Per record ``r``: the accessor interface
``r_if``, the value class ``r`` (or, for an existing SV class, the wrapper
``r_sv_wrap``), ``r_py_ref``, ``r_sv_adapter`` and the conversion functions.
Per interface ``i``: the interface class ``i``, ``i_sv_adapter``,
``i_py_proxy`` and ``i_to_py``/``i_from_py``.

Generated code calls only the ``pyhdl_if`` package. Internal helpers are
named with a leading ``__``; those marked "GIL held" expect the caller to
hold the GIL, the public ones take it themselves.
"""
from typing import Dict, List

from ..ir import (
    ScalarT, BoolT, RealT, StrT, BytesT, EnumRef, RecordRef, ListT, IfRef,
    EnumDef, RecordDef, InterfaceDef, MethodDef, TypeUniverse, IrError,
)
from ..naming import GEN_VERSION, mangle, check_names
from ...rt_api import PYHDL_IF_RT_API_VERSION

P = "pyhdl_if::"


class _Out(object):
    def __init__(self):
        self.lines = []
        self.ind = 0

    def __call__(self, line=""):
        if line == "":
            self.lines.append("")
        else:
            self.lines.append("    " * self.ind + line)

    def inc(self):
        self.ind += 1

    def dec(self):
        self.ind -= 1

    def text(self):
        return "\n".join(self.lines).rstrip() + "\n"


class SvGen(object):

    def __init__(self, u: TypeUniverse, pkg: str, py_module: str, source: str):
        self.u = u
        self.pkg = pkg
        self.py_module = py_module
        self.source = source
        self.lists: Dict[str, ListT] = {}    # helper base name -> list type
        self.wides: Dict[str, ScalarT] = {}  # helper name -> wide int type
        # SV container types spelled by the user (sv_type): pattern -> name
        self.svts: Dict[str, str] = {}
        self.svt_types: Dict[str, object] = {}  # name -> IR type

    # -- names -------------------------------------------------------------
    def rec_cls(self, name) -> str:
        """SV name of a record's value class."""
        r = self.u.record(name)
        return r.sv_ref if r.sv_ref is not None else name

    def enum_name(self, name) -> str:
        e = self.u.enum(name)
        return e.sv_ref if e.sv_ref is not None else name

    def if_name(self, name) -> str:
        i = self.u.interface(name)
        return i.sv_ref if i.sv_ref is not None else name

    def list_name(self, t: ListT) -> str:
        """Public typedef name of a list type (e.g. ``list_u8_t``)."""
        name = "list_%s_t" % mangle(t.elem)
        if self.u.get(name) is not None:
            raise IrError("'%s' clashes with the typedef generated for %s" % (
                name, "list<...>"))
        if isinstance(t.elem, ListT):
            self.list_name(t.elem)
        self.lists[name] = t
        return name

    def wide_name(self, t: ScalarT) -> str:
        name = "__hex_" + mangle(t)
        self.wides[name] = t
        return name

    # -- types -------------------------------------------------------------
    def sv_type(self, t) -> str:
        if isinstance(t, ScalarT):
            if t.signed and t.width in (8, 16, 32, 64):
                return {8: "byte", 16: "shortint", 32: "int", 64: "longint"}[t.width]
            if t.width == 1:
                return "bit signed" if t.signed else "bit"
            return "bit %s[%d:0]" % ("signed " if t.signed else "", t.width - 1)
        if isinstance(t, BoolT):
            return "bit"
        if isinstance(t, RealT):
            return "real" if t.width == 64 else "shortreal"
        if isinstance(t, StrT):
            return "string"
        if isinstance(t, BytesT):
            return P + "pyhdl_if_bytes_t"
        if isinstance(t, EnumRef):
            return self.enum_name(t.name)
        if isinstance(t, RecordRef):
            return ("%s_if" % t.name) if t.by_ref else self.rec_cls(t.name)
        if isinstance(t, ListT):
            return self.list_name(t)
        if isinstance(t, IfRef):
            return self.if_name(t.name)
        raise IrError("Unknown type %s" % str(t))

    def acc_type(self, t) -> str:
        """Type a getter returns: records are returned by reference."""
        if isinstance(t, RecordRef):
            return "%s_if" % t.name
        return self.sv_type(t)

    def _int_signed(self, t) -> bool:
        if isinstance(t, ScalarT):
            return t.signed
        if isinstance(t, EnumRef):
            return self.u.enum(t.name).signed
        return False

    def to_py(self, e: str, t) -> str:
        """Expression converting SV value ``e`` to a payload (new ref)."""
        if isinstance(t, (ScalarT, EnumRef)):
            if isinstance(t, ScalarT) and t.width > 64:
                return '%sPyUnicode_FromString($sformatf("%%0h", %s))' % (P, e)
            if self._int_signed(t):
                return "%sPyLong_FromLongLong(64'(%s))" % (P, e)
            return "%sPyLong_FromUnsignedLongLong(64'(%s))" % (P, e)
        if isinstance(t, BoolT):
            return "%sPyBool_FromLong(64'(%s))" % (P, e)
        if isinstance(t, RealT):
            return "%sPyFloat_FromDouble(%s)" % (P, e)
        if isinstance(t, StrT):
            return "%sPyUnicode_FromString(%s)" % (P, e)
        if isinstance(t, BytesT):
            return "%spyhdl_if_rt_bytesToPy(%s)" % (P, e)
        if isinstance(t, RecordRef):
            if t.by_ref:
                return "__%s_ref_to_py(%s)" % (t.name, e)
            return "__%s_to_payload(%s)" % (t.name, e)
        if isinstance(t, ListT):
            return "__%s_to_py(%s)" % (self.list_name(t), e)
        if isinstance(t, IfRef):
            return "__%s_to_py(%s)" % (t.name, e)
        raise IrError("Unknown type %s" % str(t))

    def from_py(self, o: str, t) -> str:
        """Expression converting payload ``o`` (borrowed) to an SV value."""
        if isinstance(t, ScalarT):
            if t.width > 64:
                return "%s(%s)" % (self.wide_name(t), o)
            return "%d'(%sPyLong_AsUnsignedLongLongMask(%s))" % (t.width, P, o)
        if isinstance(t, EnumRef):
            return "%s'(%sPyLong_AsUnsignedLongLongMask(%s))" % (
                self.enum_name(t.name), P, o)
        if isinstance(t, BoolT):
            return "(%sPyObject_IsTrue(%s) == 1)" % (P, o)
        if isinstance(t, RealT):
            return "%sPyFloat_AsDouble(%s)" % (P, o)
        if isinstance(t, StrT):
            return "%sPyUnicode_AsUTF8(%s)" % (P, o)
        if isinstance(t, BytesT):
            return "%spyhdl_if_rt_bytesFromPy(%s)" % (P, o)
        if isinstance(t, RecordRef):
            if t.by_ref:
                return "__%s_ref_from_py(%s)" % (t.name, o)
            return "__%s_from_payload(%s)" % (t.name, o)
        if isinstance(t, ListT):
            return "__%s_from_py(%s)" % (self.list_name(t), o)
        if isinstance(t, IfRef):
            return "__%s_from_py(%s)" % (t.name, o)
        raise IrError("Unknown type %s" % str(t))

    def copy_expr(self, e: str, t) -> str:
        """Expression for an independent copy of ``e``."""
        if isinstance(t, RecordRef):
            return "%s_copy(%s)" % (t.name, e)
        if isinstance(t, ListT) and self._has_record(t):
            return "__%s_copy(%s)" % (self.list_name(t), e)
        return e

    def _has_record(self, t) -> bool:
        if isinstance(t, RecordRef):
            return True
        if isinstance(t, ListT):
            return self._has_record(t.elem)
        return False

    # -- types as the user spelled them (sv_type) -------------------------
    @staticmethod
    def _is_container(t) -> bool:
        return isinstance(t, (ListT, BytesT))

    def svt(self, t, pattern):
        """Typedef name for a user-spelled container type, or None.

        A field or parameter of an existing SV definition that holds a queue
        or array is converted element by element through helpers for its
        exact type, since unpacked arrays of different element types do not
        assign to each other.
        """
        if pattern is None or not self._is_container(t):
            return None
        name = self.svts.get(pattern, None)
        if name is None:
            name = "__svt%d" % len(self.svts)
            self.svts[pattern] = name
            self.svt_types[name] = t
        return name

    def to_py_x(self, e: str, t, pattern=None) -> str:
        n = self.svt(t, pattern)
        if n is not None:
            return "%s_to_py(%s)" % (n, e)
        return self.to_py(e, t)

    def from_py_x(self, o: str, t, pattern=None) -> str:
        n = self.svt(t, pattern)
        if n is not None:
            return "%s_from_py(%s)" % (n, o)
        return self.from_py(o, t)

    def copy_x(self, e: str, t, pattern=None) -> str:
        n = self.svt(t, pattern)
        if n is not None:
            return ("%s_copy(%s)" % (n, e)) if self._has_record(t) else e
        return self.copy_expr(e, t)

    def type_x(self, t, pattern=None) -> str:
        """Type name for a value of ``t`` (accessor/setter argument)."""
        n = self.svt(t, pattern)
        if n is not None:
            return n
        return self.sv_type(t)

    def acc_x(self, t, pattern=None) -> str:
        """Type a getter returns."""
        if isinstance(t, RecordRef):
            return "%s_if" % t.name
        return self.type_x(t, pattern)

    def decl(self, name: str, t, pattern=None) -> str:
        """Declaration of ``name`` with the user's spelling if there is one."""
        if pattern is not None:
            return pattern % name
        return "%s %s" % (self.sv_type(t), name)

    @staticmethod
    def _getter_kind(t) -> str:
        if isinstance(t, RecordRef):
            return "record"
        if isinstance(t, ScalarT) and t.width <= 64:
            return "attr"
        if isinstance(t, (BoolT, RealT, StrT, EnumRef)):
            return "attr"
        return "field"

    @staticmethod
    def _setter_kind(t) -> str:
        if isinstance(t, ScalarT) and t.width <= 64:
            return "attr"
        if isinstance(t, (BoolT, RealT, StrT)):
            return "attr"
        return "field"

    # -- package -----------------------------------------------------------
    def generate(self) -> str:
        self.u.validate()
        check_names(self.u)
        order = self.u.dep_order()
        enums = [d for d in order if isinstance(d, EnumDef)]
        records = [d for d in order if isinstance(d, RecordDef)]
        ifaces = [d for d in order if isinstance(d, InterfaceDef)]

        # Generate the body first: it discovers the list and wide-int helpers
        body = _Out()
        body.inc()
        for r in records:
            self.gen_record(body, r)
        for i in ifaces:
            self.gen_interface(body, i)

        out = _Out()
        out("// Generated by pyhdl-if (generator version %d). Do not edit." % GEN_VERSION)
        out("// Source: %s" % self.source)
        out("// Python module: %s" % self.py_module)
        out("// pyhdl-if runtime API version: %d" % PYHDL_IF_RT_API_VERSION)
        out()
        out("/**")
        out(" * Records and interfaces generated from %s." % self.source)
        out(" *")
        out(" * The Python half is module %s." % self.py_module)
        out(" */")
        out("package %s;" % self.pkg)
        out.inc()
        out()
        out('localparam string __PY_MODULE = "%s";' % self.py_module)
        out()
        out('bit __rt_ok = %spyhdl_if_check_rt_api_version(%d, "%s");' % (
            P, PYHDL_IF_RT_API_VERSION, self.pkg))
        out()
        out("%sPyObject __py_cls_m[string];" % P)
        out()
        out("// Returns a class from the Python module. GIL held. Borrowed.")
        out("function automatic %sPyObject __py_cls(string name);" % P)
        out.inc()
        out("if (!__py_cls_m.exists(name)) begin")
        out("    __py_cls_m[name] = %spyhdl_if_rt_import(__PY_MODULE, name);" % P)
        out("end")
        out("return __py_cls_m[name];")
        out.dec()
        out("endfunction")

        for e in enums:
            self.gen_enum(out, e)

        fwd = []
        for r in records:
            if r.sv_ref is None:
                fwd.append("typedef class %s;" % r.name)
            else:
                fwd.append("typedef class %s_sv_wrap;" % r.name)
            fwd.append("typedef class %s_py_ref;" % r.name)
            fwd.append("typedef class %s_sv_adapter;" % r.name)
        for i in ifaces:
            if i.sv_ref is None:
                fwd.append("typedef interface class %s;" % i.name)
            fwd.append("typedef class %s_sv_adapter;" % i.name)
            fwd.append("typedef class %s_py_proxy;" % i.name)
        if fwd:
            out()
            for line in fwd:
                out(line)

        self.gen_helpers(out)

        out.lines.extend(body.lines)
        out.dec()
        out()
        out("endpackage")
        return out.text()

    # -- enums -------------------------------------------------------------
    def gen_enum(self, out, e: EnumDef):
        if e.sv_ref is not None:
            return
        base = "bit %s[%d:0]" % ("signed " if e.signed else "", e.width - 1)
        out()
        out("/** Enum %s. */" % e.name)
        out("typedef enum %s {" % base)
        for k, (n, v) in enumerate(e.values):
            sep = "," if k + 1 < len(e.values) else ""
            if v < 0:
                lit = "-%d'sd%d" % (e.width, -v)
            else:
                lit = "%d'%sd%d" % (e.width, "s" if e.signed else "", v)
            out("    %s = %s%s" % (n, lit, sep))
        out("} %s;" % e.name)

    # -- helpers -----------------------------------------------------------
    def gen_helpers(self, out):
        # Lists, innermost first so typedefs precede their use
        def depth(t):
            return 1 + depth(t.elem) if isinstance(t, ListT) else 0
        done = set()
        for name in sorted(self.lists.keys(), key=lambda n: (depth(self.lists[n]), n)):
            t = self.lists[name]
            if name in done:
                continue
            done.add(name)
            et = self.sv_type(t.elem)
            out()
            out("typedef %s %s[$];" % (et, name))
            out()
            out("// GIL held. New ref.")
            out("function automatic %sPyObject __%s_to_py(%s v);" % (P, name, name))
            out.inc()
            out("%sPyObject ret = %sPyList_New(64'(v.size()));" % (P, P))
            out("foreach (v[i]) begin")
            out("    void'(%sPyList_SetItem(ret, 64'(i), %s));" % (P, self.to_py("v[i]", t.elem)))
            out("end")
            out("return ret;")
            out.dec()
            out("endfunction")
            out()
            out("// GIL held. o is borrowed.")
            out("function automatic %s __%s_from_py(%sPyObject o);" % (name, name, P))
            out.inc()
            out("%s ret;" % name)
            out("if (o == null || o == %sNone) return ret;" % P)
            out("for (int i=0; i<int'(%sPyList_Size(o)); i++) begin" % P)
            out("    ret.push_back(%s);" % self.from_py("%sPyList_GetItem(o, 64'(i))" % P, t.elem))
            out("end")
            out("return ret;")
            out.dec()
            out("endfunction")
            if self._has_record(t):
                out()
                out("// Deep copy.")
                out("function automatic %s __%s_copy(%s v);" % (name, name, name))
                out.inc()
                out("%s ret;" % name)
                out("foreach (v[i]) begin")
                out("    ret.push_back(%s);" % self.copy_expr("v[i]", t.elem))
                out("end")
                out("return ret;")
                out.dec()
                out("endfunction")
        for pattern, name in self.svts.items():
            self.gen_svt(out, name, pattern, self.svt_types[name])
        for name in sorted(self.wides.keys()):
            t = self.wides[name]
            out()
            out("// GIL held. o is borrowed.")
            out("function automatic %s %s(%sPyObject o);" % (self.sv_type(t), name, P))
            out.inc()
            out("%s ret;" % self.sv_type(t))
            out('void\'($sscanf(%sPyUnicode_AsUTF8(o), "%%h", ret));' % P)
            out("return ret;")
            out.dec()
            out("endfunction")

    def gen_svt(self, out, name, pattern, t):
        elem = ScalarT(8, False) if isinstance(t, BytesT) else t.elem
        dims = pattern.split("%s", 1)[1].strip()
        kind = "queue" if dims == "[$]" else ("dyn" if dims == "[]" else "fixed")

        def elem_to_py(e):
            if isinstance(t, BytesT):
                # The user's element may be a signed byte
                return "%sPyLong_FromLong(64'(%s) & 64'hFF)" % (P, e)
            return self.to_py(e, elem)

        out()
        out("typedef %s;" % (pattern % name))
        out()
        out("// GIL held. New ref.")
        out("function automatic %sPyObject %s_to_py(%s v);" % (P, name, name))
        out.inc()
        # $size() of a queue is not its length in every simulator
        size = "$size(v)" if kind == "fixed" else "v.size()"
        out("%sPyObject ret = %sPyList_New(64'(%s));" % (P, P, size))
        out("int k = 0;")
        out("foreach (v[i]) begin")
        out("    void'(%sPyList_SetItem(ret, 64'(k), %s));" % (P, elem_to_py("v[i]")))
        out("    k++;")
        out("end")
        out("return ret;")
        out.dec()
        out("endfunction")
        out()
        out("// GIL held. o is borrowed.")
        out("function automatic %s %s_from_py(%sPyObject o);" % (name, name, P))
        out.inc()
        out("%s ret;" % name)
        out("int n;")
        out("if (o == null || o == %sNone) return ret;" % P)
        out("n = int'(%sPyList_Size(o));" % P)
        item = self.from_py("%sPyList_GetItem(o, 64'(i))" % P, elem)
        if kind == "queue":
            out("for (int i=0; i<n; i++) begin")
            out("    ret.push_back(%s);" % item)
            out("end")
        elif kind == "dyn":
            out("ret = new[n];")
            out("foreach (ret[i]) begin")
            out("    ret[i] = %s;" % item)
            out("end")
        else:
            out("begin")
            out("    int k = 0;")
            out("    foreach (ret[j]) begin")
            out("        if (k < n) ret[j] = %s;" % self.from_py("%sPyList_GetItem(o, 64'(k))" % P, elem))
            out("        k++;")
            out("    end")
            out("end")
        out("return ret;")
        out.dec()
        out("endfunction")
        if self._has_record(t):
            out()
            out("// Deep copy.")
            out("function automatic %s %s_copy(%s v);" % (name, name, name))
            out.inc()
            out("%s ret;" % name)
            if kind == "queue":
                out("foreach (v[i]) ret.push_back(%s);" % self.copy_expr("v[i]", elem))
            else:
                if kind == "dyn":
                    out("ret = new[v.size()];")
                out("foreach (v[i]) ret[i] = %s;" % self.copy_expr("v[i]", elem))
            out("return ret;")
            out.dec()
            out("endfunction")

    # -- records -----------------------------------------------------------
    def gen_record(self, out, r: RecordDef):
        n = r.name
        V = self.rec_cls(n)
        fields = self.u.all_fields(r)
        out()
        out("//****************************************************************")
        out("//* Record %s" % n)
        out("//****************************************************************")

        # Accessor interface
        out()
        out("/**")
        out(" * Accessors for a %s: a local object, or a reference to one in" % n)
        out(" * Python. Code written against %s_if works on either." % n)
        out(" */")
        if r.base is not None:
            out("interface class %s_if extends %s_if;" % (n, r.base))
        else:
            out("interface class %s_if;" % n)
        out.inc()
        for f in r.fields:
            out("pure virtual function %s get_%s();" % (self.acc_x(f.type, f.sv_type), f.name))
            out("pure virtual function void set_%s(%s v);" % (f.name, self.type_x(f.type, f.sv_type)))
        if r.base is None:
            out("// Releases a reference; does nothing on a local object.")
            out("pure virtual function void dispose();")
        out.dec()
        out("endclass")

        if r.sv_ref is None:
            self.gen_value_class(out, r)
        else:
            self.gen_sv_wrap(out, r, fields)
        self.gen_py_ref(out, r, fields)
        self.gen_rec_adapter(out, r, fields)
        self.gen_rec_funcs(out, r, fields, V)

    def gen_value_class(self, out, r: RecordDef):
        n = r.name
        out()
        out("/** Record %s, as a value. */" % n)
        if r.base is not None:
            out("class %s extends %s implements %s_if;" % (n, self.rec_cls(r.base), n))
        else:
            out("class %s implements %s_if;" % (n, n))
        out.inc()
        for f in r.fields:
            t = f.type
            init = ""
            if isinstance(t, EnumRef):
                init = " = %s" % self.u.enum(t.name).values[0][0]
            elif isinstance(t, RecordRef):
                init = " = new()"
            out("%s%s;" % (self.decl(f.name, t, f.sv_type), init))
        # Every accessor, the base's too: Verilator does not accept inherited
        # methods as implementations of the interface class
        for f in self.u.all_fields(r):
            t = f.type
            out()
            out("virtual function %s get_%s();" % (self.acc_x(t, f.sv_type), f.name))
            if isinstance(t, RecordRef):
                out("    return %s_wrap(%s);" % (t.name, f.name))
            else:
                out("    return %s;" % f.name)
            out("endfunction")
            out()
            out("virtual function void set_%s(%s v);" % (f.name, self.type_x(t, f.sv_type)))
            out("    %s = %s;" % (f.name, self.copy_x("v", t, f.sv_type)))
            out("endfunction")
        out()
        out("virtual function void dispose();")
        out("endfunction")
        out.dec()
        out("endclass")

    def gen_sv_wrap(self, out, r: RecordDef, fields):
        n = r.name
        V = self.rec_cls(n)
        out()
        out("/** Accessors for an existing %s object. */" % V)
        out("class %s_sv_wrap implements %s_if;" % (n, n))
        out.inc()
        out("%s m_obj;" % V)
        out()
        out("function new(%s obj);" % V)
        out("    m_obj = obj;")
        out("endfunction")
        for f in fields:
            t = f.type
            out()
            out("virtual function %s get_%s();" % (self.acc_x(t, f.sv_type), f.name))
            if isinstance(t, RecordRef):
                out("    return %s_wrap(m_obj.%s);" % (t.name, f.name))
            else:
                out("    return m_obj.%s;" % f.name)
            out("endfunction")
            out()
            out("virtual function void set_%s(%s v);" % (f.name, self.type_x(t, f.sv_type)))
            out("    m_obj.%s = %s;" % (f.name, self.copy_x("v", t, f.sv_type)))
            out("endfunction")
        out()
        out("virtual function void dispose();")
        out("endfunction")
        out.dec()
        out("endclass")

    def gen_py_ref(self, out, r: RecordDef, fields):
        n = r.name
        out()
        out("/** Reference to a %s in Python. Call dispose() when done. */" % n)
        out("class %s_py_ref extends %sPyRef implements %s_if;" % (n, P, n))
        out.inc()
        out()
        out("// obj: a new reference, owned until dispose()")
        out("function new(%sPyObject obj);" % P)
        out('    super.new(obj, "%s_py_ref");' % n)
        out("endfunction")
        for f in fields:
            t = f.type
            at = self.acc_x(t, f.sv_type)
            gk = self._getter_kind(t)
            out()
            out("virtual function %s get_%s();" % (at, f.name))
            out.inc()
            out("%s ret;" % at)
            out("%sPyObject o;" % P)
            out("%sPyGILState_STATE state;" % P)
            out('if (!this.live("get_%s")) return ret;' % f.name)
            out("state = %sPyGILState_Ensure();" % P)
            if gk == "field":
                out('o = %spyhdl_if_rt_getField(m_obj, "%s");' % (P, f.name))
            else:
                out('o = %spyhdl_if_rt_getAttr(m_obj, "%s");' % (P, f.name))
            out("if (o != null) begin")
            if gk == "record":
                out("    ret = __%s_ref_from_py(o);" % t.name)
            else:
                out("    ret = %s;" % self.from_py_x("o", t, f.sv_type))
            out("    %sPy_DecRef(o);" % P)
            out("end")
            out("%sPyGILState_Release(state);" % P)
            out("return ret;")
            out.dec()
            out("endfunction")
            out()
            out("virtual function void set_%s(%s v);" % (f.name, self.type_x(t, f.sv_type)))
            out.inc()
            out("%sPyGILState_STATE state;" % P)
            out('if (!this.live("set_%s")) return;' % f.name)
            out("state = %sPyGILState_Ensure();" % P)
            fn = "pyhdl_if_rt_setAttr" if self._setter_kind(t) == "attr" else "pyhdl_if_rt_setField"
            out('%s%s(m_obj, "%s", %s);' % (P, fn, f.name, self.to_py_x("v", t, f.sv_type)))
            out("%sPyGILState_Release(state);" % P)
            out.dec()
            out("endfunction")
        self._dispose(out)
        out.dec()
        out("endclass")

    def gen_rec_adapter(self, out, r: RecordDef, fields):
        n = r.name
        out()
        out("// Receives calls from Python on a reference to an SV %s." % n)
        out("class %s_sv_adapter implements %sICallApiOwnedRes;" % (n, P))
        out.inc()
        out("%s_if m_target;" % n)
        out()
        out("function new(%s_if target);" % n)
        out("    m_target = target;")
        out("endfunction")
        out()
        out("virtual function %sPyObject invokeFunc(" % P)
        out("    string              method,")
        out("    %sPyObject  args);" % P)
        out.inc()
        out("%sPyObject ret;" % P)
        out("%sPyGILState_STATE state = %sPyGILState_Ensure();" % (P, P))
        out("case (method)")
        out.inc()
        for f in fields:
            t = f.type
            get = "m_target.get_%s()" % f.name
            if isinstance(t, RecordRef):
                out('"get_%s": ret = __%s_ref_to_py(%s);' % (f.name, t.name, get))
            else:
                out('"get_%s": ret = %s;' % (f.name, self.to_py_x(get, t, f.sv_type)))
            out('"set_%s": begin' % f.name)
            out("    m_target.set_%s(%s);" % (
                f.name, self.from_py_x("%sPyTuple_GetItem(args, 0)" % P, t, f.sv_type)))
            out("    ret = %spyhdl_if_rt_none();" % P)
            out("end")
        out('"__copy": ret = __%s_to_payload(%s_from_if(m_target));' % (n, n))
        out("default: begin")
        out('    %spyhdl_if_rt_error({"%s reference: no method ", method});' % (P, n))
        out("    ret = %spyhdl_if_rt_none();" % P)
        out("end")
        out.dec()
        out("endcase")
        out("%sPyGILState_Release(state);" % P)
        out("return ret;")
        out.dec()
        out("endfunction")
        self._no_tasks(out, "%s reference" % n)
        out.dec()
        out("endclass")

    def _dispose(self, out):
        # Verilator does not accept the inherited PyRef::dispose() as the
        # implementation of the interface's dispose()
        out()
        out("virtual function void dispose();")
        out("    super.dispose();")
        out("endfunction")

    def _no_tasks(self, out, what):
        out()
        out("virtual task invokeTask(")
        out("    output %sPyObject       retval," % P)
        out("    inout %sPyGILState_STATE state," % P)
        out("    input string                    method,")
        out("    input %sPyObject        args);" % P)
        out('    %spyhdl_if_rt_error({"%s: no task ", method});' % (P, what))
        out("    retval = %spyhdl_if_rt_none();" % P)
        out("endtask")

    def gen_rec_funcs(self, out, r: RecordDef, fields, V):
        n = r.name
        sv_owned = r.sv_ref is not None

        out()
        out("/** Returns accessors for v (v itself for a generated record). */")
        out("function automatic %s_if %s_wrap(%s v);" % (n, n, V))
        if sv_owned:
            out("    %s_sv_wrap w;" % n)
            out("    if (v == null) return null;")
            out("    w = new(v);")
            out("    return w;")
        else:
            out("    return v;")
        out("endfunction")

        out()
        out("// GIL held. New ref.")
        out("function automatic %sPyObject __%s_to_payload(%s v);" % (P, n, V))
        out.inc()
        out("%sPyObject t;" % P)
        out("if (v == null) return %spyhdl_if_rt_none();" % P)
        out("t = %sPyTuple_New(%d);" % (P, len(fields)))
        for k, f in enumerate(fields):
            out("void'(%sPyTuple_SetItem(t, %d, %s));" % (P, k, self.to_py_x("v.%s" % f.name, f.type, f.sv_type)))
        out("return t;")
        out.dec()
        out("endfunction")

        out()
        out("// GIL held. t is borrowed.")
        out("function automatic %s __%s_from_payload(%sPyObject t);" % (V, n, P))
        out.inc()
        out("%s v;" % V)
        out("if (t == null || t == %sNone) return null;" % P)
        out("v = new();")
        for k, f in enumerate(fields):
            out("v.%s = %s;" % (f.name, self.from_py_x("%sPyTuple_GetItem(t, %d)" % (P, k), f.type, f.sv_type)))
        out("return v;")
        out.dec()
        out("endfunction")

        out()
        out("// GIL held. New ref.")
        out("function automatic %sPyObject __%s_ref_to_py(%s_if r);" % (P, n, n))
        out.inc()
        out("%s_py_ref pr;" % n)
        out("if (r == null) return %spyhdl_if_rt_none();" % P)
        out("if ($cast(pr, r)) return %spyhdl_if_rt_pyRefObj(pr);" % P)
        out("begin")
        out("    %s_sv_adapter a = new(r);" % n)
        out('    return %spyhdl_if_rt_svObjNew(__py_cls("%s_sv_ref"), a);' % (P, n))
        out("end")
        out.dec()
        out("endfunction")

        out()
        out("// GIL held. o is borrowed.")
        out("function automatic %s_if __%s_ref_from_py(%sPyObject o);" % (n, n, P))
        out.inc()
        out("%sICallApi a;" % P)
        out("if (o == null || o == %sNone) return null;" % P)
        out("a = %spyhdl_if_rt_svObjGet(o);" % P)
        out("if (a != null) begin")
        out("    %s_sv_adapter sa;" % n)
        out("    if ($cast(sa, a)) return sa.m_target;")
        out('    %spyhdl_if_rt_error("expected a reference to %s");' % (P, n))
        out("    return null;")
        out("end else begin")
        out("    %s_py_ref pr;" % n)
        out("    %sPy_IncRef(o);" % P)
        out("    pr = new(o);")
        out("    return pr;")
        out("end")
        out.dec()
        out("endfunction")

        out()
        out("/** Returns a deep copy of v. */")
        out("function automatic %s %s_copy(%s v);" % (V, n, V))
        out.inc()
        out("%s ret;" % V)
        out("if (v == null) return null;")
        out("ret = new();")
        for f in fields:
            out("ret.%s = %s;" % (f.name, self.copy_x("v.%s" % f.name, f.type, f.sv_type)))
        out("return ret;")
        out.dec()
        out("endfunction")

        out()
        out("/** Returns a copy of the current value behind r. */")
        out("function automatic %s %s_from_if(%s_if r);" % (V, n, n))
        out.inc()
        out("%s ret;" % V)
        out("if (r == null) return null;")
        out("ret = new();")
        for f in fields:
            t = f.type
            if isinstance(t, RecordRef):
                out("begin")
                out("    %s_if h = r.get_%s();" % (t.name, f.name))
                out("    ret.%s = %s_from_if(h);" % (f.name, t.name))
                out("    if (h != null) h.dispose();")
                out("end")
            else:
                out("ret.%s = r.get_%s();" % (f.name, f.name))
        out("return ret;")
        out.dec()
        out("endfunction")

        self._public(out, "/** Copies v into a new Python %s. */" % n,
                     "%sPyObject" % P, "%s_to_py(%s v)" % (n, V),
                     '%spyhdl_if_rt_recFromSv(__py_cls("%s"), __%s_to_payload(v))' % (P, n, n))

        out()
        out("/** Copies a Python %s (or a reference to one) into a new SV %s. */" % (n, n))
        out("function automatic %s %s_from_py(%sPyObject o);" % (V, n, P))
        out.inc()
        out("%s ret;" % V)
        out("%sPyObject p;" % P)
        out("%sPyGILState_STATE state = %sPyGILState_Ensure();" % (P, P))
        out("p = %spyhdl_if_rt_recToSv(o);" % P)
        out("if (p != null) begin")
        out("    ret = __%s_from_payload(p);" % n)
        out("    %sPy_DecRef(p);" % P)
        out("end")
        out("%sPyGILState_Release(state);" % P)
        out("return ret;")
        out.dec()
        out("endfunction")

        self._public(out, "/** Returns a Python reference to r. */",
                     "%sPyObject" % P, "%s_ref_to_py(%s_if r)" % (n, n),
                     "__%s_ref_to_py(r)" % n)
        self._public(out, "/** Returns an SV reference to a Python %s. Call dispose() when done. */" % n,
                     "%s_if" % n, "%s_ref_from_py(%sPyObject o)" % (n, P),
                     "__%s_ref_from_py(o)" % n)

    def _public(self, out, doc, rtype, sig, expr):
        out()
        out(doc)
        out("function automatic %s %s;" % (rtype, sig))
        out.inc()
        out("%s ret;" % rtype)
        out("%sPyGILState_STATE state = %sPyGILState_Ensure();" % (P, P))
        out("ret = %s;" % expr)
        out("%sPyGILState_Release(state);" % P)
        out("return ret;")
        out.dec()
        out("endfunction")

    # -- interfaces --------------------------------------------------------
    def proto(self, m: MethodDef) -> str:
        """SV prototype of a method, without 'virtual'/'pure'."""
        params = []
        if m.is_task:
            if m.rtype is not None:
                params.append("output %s" % self.decl(m.sv_ret_name or "retval", m.rtype,
                    (m.sv_rtype + " %s") if m.sv_rtype else None))
            for p in m.params:
                params.append("input %s" % self.decl(p.name, p.type, p.sv_type))
            return "task %s(%s)" % (m.name, ", ".join(params))
        for p in m.params:
            params.append(self.decl(p.name, p.type, p.sv_type))
        if m.rtype is None:
            rt = "void"
        else:
            rt = m.sv_rtype if m.sv_rtype else self.sv_type(m.rtype)
        return "function %s %s(%s)" % (rt, m.name, ", ".join(params))

    @staticmethod
    def _rpat(m: MethodDef):
        return (m.sv_rtype + " %s") if m.sv_rtype else None

    def gen_interface(self, out, i: InterfaceDef):
        n = i.name
        I = self.if_name(n)
        funcs = [m for m in i.methods if not m.is_task]
        tasks = [m for m in i.methods if m.is_task]
        out()
        out("//****************************************************************")
        out("//* Interface %s" % n)
        out("//****************************************************************")

        if i.sv_ref is None:
            out()
            out("/** Interface %s. Implement it in SV, or call a Python implementation. */" % n)
            out("interface class %s;" % n)
            out.inc()
            for m in i.methods:
                out("pure virtual %s;" % self.proto(m))
            out("// Releases a proxy; does nothing on a local implementation.")
            out("pure virtual function void dispose();")
            out.dec()
            out("endclass")

        # SV adapter
        out()
        out("// Receives calls from Python on an SV implementation of %s." % n)
        out("class %s_sv_adapter implements %sICallApiOwnedRes;" % (n, P))
        out.inc()
        out("%s m_impl;" % I)
        out()
        out("function new(%s impl);" % I)
        out("    m_impl = impl;")
        out("endfunction")
        out()
        out("virtual function %sPyObject invokeFunc(" % P)
        out("    string              method,")
        out("    %sPyObject  args);" % P)
        out.inc()
        out("%sPyObject ret;" % P)
        out("%sPyGILState_STATE state = %sPyGILState_Ensure();" % (P, P))
        out("case (method)")
        out.inc()
        for m in funcs:
            args = [self.from_py_x("%sPyTuple_GetItem(args, %d)" % (P, k), p.type, p.sv_type)
                    for k, p in enumerate(m.params)]
            out('"%s": begin' % m.name)
            out.inc()
            if m.rtype is not None:
                out("%s;" % self.decl("__r", m.rtype, self._rpat(m)))
                self._call(out, "__r = m_impl.%s" % m.name, args)
                out("ret = %s;" % self.to_py_x("__r", m.rtype, self._rpat(m)))
            else:
                self._call(out, "m_impl.%s" % m.name, args)
                out("ret = %spyhdl_if_rt_none();" % P)
            out.dec()
            out("end")
        out("default: begin")
        out('    %spyhdl_if_rt_error({"%s: no function ", method});' % (P, n))
        out("    ret = %spyhdl_if_rt_none();" % P)
        out("end")
        out.dec()
        out("endcase")
        out("%sPyGILState_Release(state);" % P)
        out("return ret;")
        out.dec()
        out("endfunction")
        out()
        out("virtual task invokeTask(")
        out("    output %sPyObject       retval," % P)
        out("    inout %sPyGILState_STATE state," % P)
        out("    input string                    method,")
        out("    input %sPyObject        args);" % P)
        out.inc()
        out("case (method)")
        out.inc()
        for m in tasks:
            out('"%s": begin' % m.name)
            out.inc()
            if m.rtype is not None:
                out("%s;" % self.decl("__r", m.rtype, self._rpat(m)))
            for k, p in enumerate(m.params):
                out("%s = %s;" % (self.decl("__p_%s" % p.name, p.type, p.sv_type),
                    self.from_py_x("%sPyTuple_GetItem(args, %d)" % (P, k), p.type, p.sv_type)))
            out("%sPyGILState_Release(state);" % P)
            args = (["__r"] if m.rtype is not None else []) + ["__p_%s" % p.name for p in m.params]
            out("m_impl.%s(%s);" % (m.name, ", ".join(args)))
            out("state = %sPyGILState_Ensure();" % P)
            if m.rtype is not None:
                out("retval = %s;" % self.to_py_x("__r", m.rtype, self._rpat(m)))
            else:
                out("retval = %spyhdl_if_rt_none();" % P)
            out.dec()
            out("end")
        out("default: begin")
        out('    %spyhdl_if_rt_error({"%s: no task ", method});' % (P, n))
        out("    retval = %spyhdl_if_rt_none();" % P)
        out("end")
        out.dec()
        out("endcase")
        out.dec()
        out("endtask")
        out.dec()
        out("endclass")

        # Python proxy
        out()
        out("/** Calls a Python implementation of %s. Call dispose() when done. */" % n)
        out("class %s_py_proxy extends %sPyRef implements %s;" % (n, P, I))
        out.inc()
        out()
        out("// obj: a new reference to the Python adapter, owned until dispose()")
        out("function new(%sPyObject obj);" % P)
        out('    super.new(obj, "%s_py_proxy");' % n)
        out("endfunction")
        for m in i.methods:
            out()
            out("virtual %s;" % self.proto(m))
            out.inc()
            if not m.is_task and m.rtype is not None:
                out("%s;" % self.decl("__ret", m.rtype, self._rpat(m)))
            out("%sPyObject __args, __res;" % P)
            out("%sPyGILState_STATE __state;" % P)
            if not m.is_task and m.rtype is not None:
                out('if (!this.live("%s")) return __ret;' % m.name)
            else:
                out('if (!this.live("%s")) return;' % m.name)
            out("__state = %sPyGILState_Ensure();" % P)
            out("__args = %sPyTuple_New(%d);" % (P, len(m.params)))
            for k, p in enumerate(m.params):
                out("void'(%sPyTuple_SetItem(__args, %d, %s));" % (P, k, self.to_py_x(p.name, p.type, p.sv_type)))
            if m.is_task:
                out("%sPyGILState_Release(__state);" % P)
                out('%spyhdl_if_rt_callPyTask(__res, this.m_obj, "%s", __args);' % (P, m.name))
                out("if (__res != null) begin")
                out("    __state = %sPyGILState_Ensure();" % P)
                if m.rtype is not None:
                    out("    %s = %s;" % (m.sv_ret_name or "retval", self.from_py_x("__res", m.rtype, self._rpat(m))))
                out("    %sPy_DecRef(__res);" % P)
                out("    %sPyGILState_Release(__state);" % P)
                out("end")
            else:
                out('__res = %spyhdl_if_rt_callPyFunc(this.m_obj, "%s", __args);' % (P, m.name))
                out("if (__res != null) begin")
                if m.rtype is not None:
                    out("    __ret = %s;" % self.from_py_x("__res", m.rtype, self._rpat(m)))
                out("    %sPy_DecRef(__res);" % P)
                out("end")
                out("%sPyGILState_Release(__state);" % P)
                if m.rtype is not None:
                    out("return __ret;")
            out.dec()
            out("endtask" if m.is_task else "endfunction")
        self._dispose(out)
        out.dec()
        out("endclass")

        # Conversions
        out()
        out("// GIL held. New ref.")
        out("function automatic %sPyObject __%s_to_py(%s h);" % (P, n, I))
        out.inc()
        out("%s_py_proxy pp;" % n)
        out("if (h == null) return %spyhdl_if_rt_none();" % P)
        out("if ($cast(pp, h)) return %spyhdl_if_rt_pyRefObj(pp);" % P)
        out("begin")
        out("    %s_sv_adapter a = new(h);" % n)
        out('    return %spyhdl_if_rt_svObjNew(__py_cls("%s_sv_proxy"), a);' % (P, n))
        out("end")
        out.dec()
        out("endfunction")
        out()
        out("// GIL held. o is borrowed.")
        out("function automatic %s __%s_from_py(%sPyObject o);" % (I, n, P))
        out.inc()
        out("%sICallApi a;" % P)
        out("if (o == null || o == %sNone) return null;" % P)
        out("a = %spyhdl_if_rt_svObjGet(o);" % P)
        out("if (a != null) begin")
        out("    %s_sv_adapter sa;" % n)
        out("    if ($cast(sa, a)) return sa.m_impl;")
        out('    %spyhdl_if_rt_error("expected an implementation of %s");' % (P, n))
        out("    return null;")
        out("end else begin")
        out('    %s_py_proxy pp = new(%spyhdl_if_rt_pyAdapt(__py_cls("%s_py_adapter"), o));' % (n, P, n))
        out("    return pp;")
        out("end")
        out.dec()
        out("endfunction")

        self._public(out, "/** Returns a Python object that calls h. */",
                     "%sPyObject" % P, "%s_to_py(%s h)" % (n, I), "__%s_to_py(h)" % n)
        self._public(out, "/** Returns an SV handle that calls a Python implementation. Call dispose() when done. */",
                     I, "%s_from_py(%sPyObject o)" % (n, P), "__%s_from_py(o)" % n)

    def _call(self, out, head, args):
        if len(args) == 0:
            out("%s();" % head)
        elif len(args) == 1:
            out("%s(%s);" % (head, args[0]))
        else:
            out("%s(" % head)
            for k, a in enumerate(args):
                out("    %s%s" % (a, "," if k + 1 < len(args) else ");"))


def gen_sv(u: TypeUniverse, pkg: str, py_module: str, source: str) -> str:
    """Return the SV package for ``u``.

    Args:
        u: The definitions.
        pkg: Name of the SV package.
        py_module: Name of the generated Python module (imported at run time).
        source: Names the input, for the file header.
    """
    return SvGen(u, pkg, py_module, source).generate()
