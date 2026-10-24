#****************************************************************************
#* sv.py
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
"""SystemVerilog front end: builds a :class:`TypeUniverse` with pyslang.

* A class becomes a record. Its fields are its public, non-static,
  non-const data members (``--sv-fields=rand``: only ``rand``/``randc``
  ones). ``local`` and ``protected`` members are never mirrored: generated
  code outside the class cannot reach them.
* An ``interface class`` becomes an interface. Its pure virtual methods,
  including those of interface classes it extends, are the methods; a task's
  leading ``output`` argument carries its result.
* A ``typedef enum`` becomes an enum.

Base classes: the walk up ``extends`` stops at a class matching a *stop*
pattern (by default every class in ``uvm_pkg``) and passes over a class
matching a *skip* pattern (dropping its fields). Other base classes become
records too.

Every definition found already exists in SV, so it carries an ``sv_ref``
(``pkg::name``) and the SV back end generates companions for it instead of
regenerating it. Parameter and container types keep their SV spelling
(``sv_type``), since generated code must match them exactly.

Requires pyslang (``pip install pyhdl-if[sv]``).
"""
import dataclasses as dc
import fnmatch
import shlex
from typing import Dict, List, Optional

from ..ir import (
    ScalarT, BoolT, RealT, StrT, BytesT, EnumRef, RecordRef, ListT, IfRef,
    EnumDef, FieldDef, RecordDef, ParamDef, MethodDef, InterfaceDef,
    TypeUniverse, IrError,
)

__all__ = ["SvOptions", "SvFrontEnd", "universe_from_sv", "DEFAULT_STOP_AT"]

#: Base classes the inheritance walk stops at unless told otherwise.
DEFAULT_STOP_AT = ["uvm_pkg::*"]

#: Packages whose definitions are never roots.
_SKIP_PACKAGES = {"std", "uvm_pkg", "pyhdl_if", "$unit"}


@dc.dataclass
class SvOptions(object):
    """Selection and filtering for the SV front end.

    Patterns are ``fnmatch`` patterns. Definitions are named ``pkg::name``,
    fields ``pkg::Class.field`` and methods ``pkg::Iface.method``.
    """
    #: Definitions to use as roots (default: all). What they use comes too.
    include: List[str] = dc.field(default_factory=list)
    #: Definitions never to use as roots.
    exclude: List[str] = dc.field(default_factory=list)
    #: "public" (all public data members) or "rand" (only rand/randc).
    fields: str = "public"
    field_include: List[str] = dc.field(default_factory=list)
    field_exclude: List[str] = dc.field(default_factory=list)
    method_include: List[str] = dc.field(default_factory=list)
    method_exclude: List[str] = dc.field(default_factory=list)
    #: Base classes where the inheritance walk stops.
    stop_at: List[str] = dc.field(default_factory=lambda: list(DEFAULT_STOP_AT))
    #: Base classes the walk passes over, dropping their fields.
    skip_base: List[str] = dc.field(default_factory=list)
    #: Skip fields of unsupported types (with a warning) instead of failing.
    skip_unsupported: bool = False


def _match(name: str, patterns: List[str]) -> bool:
    return any(fnmatch.fnmatchcase(name, p) for p in patterns)


class SvFrontEnd(object):
    """Collects definitions from a pyslang compilation."""

    def __init__(self, opts: Optional[SvOptions] = None):
        self.opts = opts if opts is not None else SvOptions()
        self.u = TypeUniverse()
        self.warnings: List[str] = []
        self._sm = None
        self._by_path: Dict[str, str] = {}   # pkg::name -> definition name

    # -- compilation -------------------------------------------------------
    def compile(self, args: List[str]):
        """Compile SV sources with slang's command-line syntax.

        Args:
            args: Source files and slang options (``-f``, ``-I``/``+incdir+``,
                ``-D``/``+define+`` ...).

        Raises:
            IrError: If pyslang is missing or the sources have errors.
        """
        try:
            from pyslang.driver import Driver, CommandLineOptions
        except ImportError:
            raise IrError("gen-from-sv needs pyslang: pip install pyhdl-if[sv]")
        d = Driver()
        d.addStandardArgs()
        cmdline = "slang " + " ".join(shlex.quote(a) for a in args)
        if not d.parseCommandLine(cmdline, CommandLineOptions()):
            raise IrError("Bad SV arguments: %s" % " ".join(args))
        if not d.processOptions():
            raise IrError("Bad SV arguments: %s" % " ".join(args))
        if not d.parseAllSources():
            raise IrError("Failed to parse SV sources")
        comp = d.createCompilation()
        self._sm = d.sourceManager
        errors = [diag for diag in comp.getAllDiagnostics() if diag.isError()]
        if errors:
            import pyslang
            text = pyslang.DiagnosticEngine.reportAll(self._sm, errors)
            raise IrError("SV sources have errors:\n%s" % text)
        return comp

    def _where(self, sym) -> str:
        try:
            loc = sym.location
            return "%s:%d" % (self._sm.getFileName(loc), self._sm.getLineNumber(loc))
        except Exception:
            return "?"

    def _err(self, sym, msg):
        return IrError("%s: %s" % (self._where(sym), msg))

    # -- roots -------------------------------------------------------------
    def add_compilation(self, comp):
        """Add the roots selected by the options from every package."""
        from pyslang.ast import SymbolKind
        for pkg in comp.getPackages():
            if pkg.name in _SKIP_PACKAGES:
                continue
            for m in pkg:
                path = "%s::%s" % (pkg.name, m.name)
                if m.kind == SymbolKind.ClassType:
                    pass
                elif m.kind == SymbolKind.TypeAlias and m.canonicalType.isEnum:
                    pass
                else:
                    continue
                if self.opts.include and not _match(path, self.opts.include):
                    continue
                if _match(path, self.opts.exclude):
                    continue
                if m.kind == SymbolKind.ClassType:
                    self.add_class(m)
                else:
                    self.add_enum(m)

    def _claim(self, sym, path) -> str:
        name = sym.name
        other = self.u.get(name)
        if other is not None:
            raise self._err(sym, "two definitions named '%s': %s and %s" % (
                name, other.sv_ref, path))
        self._by_path[path] = name
        return name

    # -- enums -------------------------------------------------------------
    def add_enum(self, alias) -> str:
        path = alias.lexicalPath
        if path in self._by_path:
            return self._by_path[path]
        name = self._claim(alias, path)
        ct = alias.canonicalType
        values = []
        for v in ct:
            sv = v.value.value
            values.append((v.name, int(sv)))
        self.u.add(EnumDef(name, int(ct.bitWidth), values, signed=bool(ct.isSigned),
                           sv_ref=path))
        return name

    # -- classes -----------------------------------------------------------
    def add_class(self, cls) -> str:
        if cls.isInterface:
            return self._add_interface(cls)
        return self._add_record(cls)

    def _add_record(self, cls) -> str:
        from pyslang.ast import SymbolKind, Visibility, VariableLifetime, VariableFlags, RandMode
        path = cls.lexicalPath
        if path in self._by_path:
            return self._by_path[path]
        if cls.isAbstract:
            raise self._err(cls, "class %s is virtual and cannot be a record "
                            "(copies need to construct it); skip it with --skip-base "
                            "or exclude it" % path)
        ctor = cls.find("new")
        if ctor is not None:
            for a in ctor.arguments:
                if a.defaultValue is None:
                    raise self._err(cls, "class %s cannot be a record: its constructor "
                                    "argument '%s' has no default" % (path, a.name))
        name = self._claim(cls, path)
        rd = RecordDef(name, sv_ref=path)
        self.u.add(rd)

        b = cls.baseClass
        while b is not None and b.kind == SymbolKind.ClassType:
            bpath = b.lexicalPath
            if _match(bpath, self.opts.stop_at):
                break
            if _match(bpath, self.opts.skip_base):
                b = b.baseClass
                continue
            rd.base = self._add_record(b)
            break

        for m in cls:
            if m.kind != SymbolKind.ClassProperty:
                continue
            fpath = "%s.%s" % (path, m.name)
            if m.visibility != Visibility.Public:
                continue
            if m.lifetime == VariableLifetime.Static:
                continue
            if m.flags & VariableFlags.Const:
                continue
            if self.opts.fields == "rand" and m.randMode == RandMode.None_:
                continue
            if self.opts.field_include and not _match(fpath, self.opts.field_include):
                continue
            if _match(fpath, self.opts.field_exclude):
                continue
            try:
                t, sv_type = self._map_type(m.type, m)
            except IrError as e:
                if self.opts.skip_unsupported:
                    self.warnings.append("%s: skipped field %s: %s" % (
                        self._where(m), fpath, str(e)))
                    continue
                raise self._err(m, "field %s: %s (exclude it with --field-exclude "
                                "or pass --skip-unsupported)" % (fpath, str(e)))
            if isinstance(t, IfRef):
                raise self._err(m, "field %s: record fields cannot be interfaces" % fpath)
            rd.fields.append(FieldDef(m.name, t, sv_type if self._is_container(t) else None))
        return name

    @staticmethod
    def _is_container(t) -> bool:
        return isinstance(t, (ListT, BytesT))

    def _add_interface(self, cls) -> str:
        from pyslang.ast import SubroutineKind, ArgumentDirection
        path = cls.lexicalPath
        if path in self._by_path:
            return self._by_path[path]
        name = self._claim(cls, path)
        idef = InterfaceDef(name, sv_ref=path)
        self.u.add(idef)

        seen = set()
        for proto in self._prototypes(cls):
            mname = proto.name
            if mname in seen or mname == "dispose":
                continue
            seen.add(mname)
            mpath = "%s.%s" % (path, mname)
            if self.opts.method_include and not _match(mpath, self.opts.method_include):
                continue
            if _match(mpath, self.opts.method_exclude):
                continue
            is_task = proto.subroutineKind == SubroutineKind.Task
            md = MethodDef(mname, is_task=is_task)
            args = list(proto.arguments)
            if is_task and args and args[0].direction == ArgumentDirection.Out:
                md.rtype, rpat = self._map_type(args[0].type, args[0])
                md.sv_rtype = rpat.replace(" %s", "", 1) if rpat.endswith(" %s") else None
                if md.sv_rtype is None:
                    raise self._err(args[0], "%s: an unpacked result type needs a typedef" % mpath)
                md.sv_ret_name = args[0].name
                args = args[1:]
            for a in args:
                if a.direction != ArgumentDirection.In:
                    raise self._err(a, "%s: argument %s: only input arguments (and a "
                                    "task's leading output) are supported" % (mpath, a.name))
                t, pat = self._map_type(a.type, a)
                md.params.append(ParamDef(a.name, t, pat))
            if not is_task:
                rt = proto.returnType
                if not rt.isVoid:
                    md.rtype, rpat = self._map_type(rt, proto)
                    md.sv_rtype = self._spell(rt)
            idef.methods.append(md)
        return name

    def _prototypes(self, cls):
        """Pure virtual methods of an interface class and those it extends."""
        from pyslang.ast import SymbolKind
        ret = []
        for m in cls:
            if m.kind == SymbolKind.MethodPrototype:
                ret.append(m)
        for base in (cls.implementedInterfaces or []):
            ret.extend(self._prototypes(base))
        return ret

    # -- types -------------------------------------------------------------
    def _spell(self, t) -> str:
        """SV spelling of a type, usable from another package."""
        from pyslang.ast import SymbolKind
        if t.kind in (SymbolKind.TypeAlias, SymbolKind.ClassType):
            return t.lexicalPath
        return str(t)

    def _map_type(self, t, where):
        """Return ``(IR type, declaration pattern)`` for an SV type.

        The pattern is the declaration with ``%s`` for the name.
        """
        from pyslang.ast import SymbolKind
        ct = t.canonicalType
        if ct.isUnpackedArray:
            if ct.isAssociativeArray:
                raise IrError("associative arrays are not supported")
            if ct.isQueue:
                dims = "[$]"
            elif ct.kind == SymbolKind.DynamicArrayType:
                dims = "[]"
            else:
                r = ct.fixedRange
                dims = "[%d:%d]" % (r.left, r.right)
            et = ct.arrayElementType
            if et.canonicalType.isUnpackedArray:
                raise IrError("arrays of arrays are not supported")
            ir = BytesT() if self._is_byte(et) else ListT(self._map_scalar(et))
            return ir, "%s %%s%s" % (self._spell(et), dims)
        return self._map_scalar(t), "%s %%s" % self._spell(t)

    @staticmethod
    def _is_byte(t) -> bool:
        ct = t.canonicalType
        return (ct.isIntegral and not ct.isEnum and ct.bitWidth == 8)

    def _map_scalar(self, t):
        from pyslang.ast import SymbolKind
        ct = t.canonicalType
        if ct.isEnum:
            if t.kind != SymbolKind.TypeAlias:
                raise IrError("anonymous enums are not supported; use a typedef")
            return EnumRef(self.add_enum(t))
        if ct.isClass:
            if ct.kind != SymbolKind.ClassType:
                raise IrError("type %s is not supported" % str(t))
            if ct.genericClass is not None:
                raise IrError("parameterized class %s is not supported" % str(t))
            name = self.add_class(ct)
            return IfRef(name) if ct.isInterface else RecordRef(name)
        if ct.isString:
            return StrT()
        if ct.isFloating:
            return RealT(32 if ct.bitWidth == 32 else 64)
        if ct.isIntegral:
            if ct.kind == SymbolKind.PackedStructType or ct.kind == SymbolKind.PackedUnionType:
                raise IrError("packed structs and unions are not supported yet")
            w = int(ct.bitWidth)
            if w == 1 and not ct.isSigned:
                return BoolT()
            return ScalarT(w, bool(ct.isSigned))
        raise IrError("type %s is not supported" % str(t))


def universe_from_sv(args: List[str], opts: Optional[SvOptions] = None):
    """Build a TypeUniverse from SV sources.

    Args:
        args: Source files and slang options.
        opts: Selection and filtering.

    Returns:
        ``(universe, warnings)``.
    """
    fe = SvFrontEnd(opts)
    comp = fe.compile(args)
    fe.add_compilation(comp)
    fe.u.validate()
    return fe.u, fe.warnings
