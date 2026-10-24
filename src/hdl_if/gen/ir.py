#****************************************************************************
#* ir.py
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
"""Language-neutral description of records, enums and interfaces.

Front ends (Python, SystemVerilog, JSON spec) build a :class:`TypeUniverse`;
back ends generate code from it. Nothing here says which language a type was
declared in or which side implements an interface: that is decided when the
generated code is bound.
"""
import dataclasses as dc
import keyword
from typing import Dict, List, Optional, Tuple, Union

__all__ = [
    "ScalarT", "BoolT", "RealT", "StrT", "BytesT",
    "EnumRef", "RecordRef", "ListT", "IfRef", "TypeRef",
    "EnumDef", "FieldDef", "RecordDef", "ParamDef", "MethodDef",
    "InterfaceDef", "TypeUniverse", "IrError",
]


class IrError(Exception):
    """A definition is invalid. The message names the offending element."""
    pass


#****************************************************************************
#* Type references
#****************************************************************************
@dc.dataclass(frozen=True)
class ScalarT(object):
    """A two-state integer of ``width`` bits."""
    width: int
    signed: bool

    def __post_init__(self):
        if self.width < 1:
            raise IrError("Integer width must be at least 1 (got %d)" % self.width)


@dc.dataclass(frozen=True)
class BoolT(object):
    """A single-bit boolean."""
    pass


@dc.dataclass(frozen=True)
class RealT(object):
    """A floating-point value of 32 or 64 bits."""
    width: int = 64

    def __post_init__(self):
        if self.width not in (32, 64):
            raise IrError("Real width must be 32 or 64 (got %d)" % self.width)


@dc.dataclass(frozen=True)
class StrT(object):
    """A string."""
    pass


@dc.dataclass(frozen=True)
class BytesT(object):
    """A variable-length sequence of bytes."""
    pass


@dc.dataclass(frozen=True)
class EnumRef(object):
    """A use of an enum, by name."""
    name: str


@dc.dataclass(frozen=True)
class RecordRef(object):
    """A use of a record, by name: a copy, or a reference when ``by_ref``."""
    name: str
    by_ref: bool = False


@dc.dataclass(frozen=True)
class ListT(object):
    """A variable-length list of ``elem``."""
    elem: "TypeRef"


@dc.dataclass(frozen=True)
class IfRef(object):
    """A use of an interface, by name. Always a reference."""
    name: str


TypeRef = Union[ScalarT, BoolT, RealT, StrT, BytesT,
                EnumRef, RecordRef, ListT, IfRef]


def type_str(t: TypeRef) -> str:
    """Return the spec-format spelling of a type (see :mod:`.spec`)."""
    if isinstance(t, ScalarT):
        return "%s%d" % ("i" if t.signed else "u", t.width)
    if isinstance(t, BoolT):
        return "bool"
    if isinstance(t, RealT):
        return "f%d" % t.width
    if isinstance(t, StrT):
        return "str"
    if isinstance(t, BytesT):
        return "bytes"
    if isinstance(t, ListT):
        return "list<%s>" % type_str(t.elem)
    if isinstance(t, RecordRef):
        return ("ref<%s>" % t.name) if t.by_ref else t.name
    if isinstance(t, (EnumRef, IfRef)):
        return t.name
    raise IrError("Unknown type %s" % str(t))


#****************************************************************************
#* Definitions
#****************************************************************************
@dc.dataclass
class EnumDef(object):
    """An enumeration.

    Attributes:
        name: Enum name, used unchanged in both languages.
        width: Width in bits of the underlying integer.
        values: ``(name, value)`` pairs, in declaration order.
        signed: Whether the underlying integer is signed.
        py_ref: ``module.Class`` of an existing Python ``IntEnum`` to use
            instead of generating one.
        sv_ref: ``pkg::name`` of an existing SV enum typedef to use instead
            of generating one.
    """
    name: str
    width: int
    values: List[Tuple[str, int]]
    signed: bool = False
    py_ref: Optional[str] = None
    sv_ref: Optional[str] = None


@dc.dataclass
class FieldDef(object):
    """One field of a record.

    Attributes:
        name: Field name.
        type: Field type.
        sv_type: For a field of an existing SV class, its declaration as
            written there, with ``%s`` for the name (e.g. ``"byte %s[$]"``).
            Generated code uses it where the exact SV type matters.
    """
    name: str
    type: TypeRef
    sv_type: Optional[str] = None


@dc.dataclass
class RecordDef(object):
    """A record: a value type with ordered fields.

    Attributes:
        name: Record name, used unchanged in both languages.
        fields: The record's own fields, in order (not including the base's).
        base: Name of the record this one extends, or None.
        py_ref: ``module.Class`` of an existing Python dataclass to use
            instead of generating one.
        sv_ref: ``pkg::name`` of an existing SV class to use instead of
            generating one.
    """
    name: str
    fields: List[FieldDef] = dc.field(default_factory=list)
    base: Optional[str] = None
    py_ref: Optional[str] = None
    sv_ref: Optional[str] = None


@dc.dataclass
class ParamDef(object):
    """One parameter of a method.

    Attributes:
        name: Parameter name.
        type: Parameter type.
        sv_type: For a method of an existing SV interface class, the
            parameter's declaration as written there, with ``%s`` for the
            name. Generated code that implements the interface class uses it,
            since SV requires matching types.
    """
    name: str
    type: TypeRef
    sv_type: Optional[str] = None


@dc.dataclass
class MethodDef(object):
    """A method of an interface.

    Attributes:
        name: Method name.
        is_task: True for a task (may consume time; ``async`` in Python).
        params: Parameters, in order.
        rtype: Return type, or None for no return value.
        sv_rtype: For a method of an existing SV interface class, the
            return type as written there (a task's leading ``output``
            argument, for a task).
        sv_ret_name: For a task of an existing SV interface class, the name
            of the leading ``output`` argument that carries the result.
    """
    name: str
    is_task: bool = False
    params: List[ParamDef] = dc.field(default_factory=list)
    rtype: Optional[TypeRef] = None
    sv_rtype: Optional[str] = None
    sv_ret_name: Optional[str] = None


@dc.dataclass
class InterfaceDef(object):
    """A set of methods that either side may implement.

    Attributes:
        name: Interface name.
        methods: Methods, in order.
        py_ref: ``module.Class`` of an existing Python Protocol to use
            instead of generating one.
        sv_ref: ``pkg::name`` of an existing SV interface class to use
            instead of generating one.
    """
    name: str
    methods: List[MethodDef] = dc.field(default_factory=list)
    py_ref: Optional[str] = None
    sv_ref: Optional[str] = None


Definition = Union[EnumDef, RecordDef, InterfaceDef]


#****************************************************************************
#* Names
#****************************************************************************
SV_KEYWORDS = frozenset("""
accept_on alias always always_comb always_ff always_latch and assert assign
assume automatic before begin bind bins binsof bit break buf bufif0 bufif1
byte case casex casez cell chandle checker class clocking cmos config const
constraint context continue cover covergroup coverpoint cross deassign
default defparam design disable dist do edge else end endcase endchecker
endclass endclocking endconfig endfunction endgenerate endgroup
endinterface endmodule endpackage endprimitive endprogram endproperty
endspecify endsequence endtable endtask enum event eventually expect export
extends extern final first_match for force foreach forever fork forkjoin
function generate genvar global highz0 highz1 if iff ifnone ignore_bins
illegal_bins implements implies import incdir include initial inout input
inside instance int integer interconnect interface intersect join join_any
join_none large let liblist library local localparam logic longint
macromodule matches medium modport module nand negedge nettype new nexttime
nmos nor noshowcancelled not notif0 notif1 null or output package packed
parameter pmos posedge primitive priority program property protected pull0
pull1 pulldown pullup pulsestyle_ondetect pulsestyle_onevent pure rand randc
randcase randsequence rcmos real realtime ref reg reject_on release repeat
restrict return rnmos rpmos rtran rtranif0 rtranif1 s_always s_eventually
s_nexttime s_until s_until_with scalared sequence shortint shortreal
showcancelled signed small soft solve specify specparam static string strong
strong0 strong1 struct super supply0 supply1 sync_accept_on sync_reject_on
table tagged task this throughout time timeprecision timeunit tran tranif0
tranif1 tri tri0 tri1 triand trior trireg type typedef union unique unique0
unsigned until until_with untyped use uwire var vectored virtual void wait
wait_order wand weak weak0 weak1 while wildcard wire with within wor xnor
xor
""".split())

#: Names the generated code uses for its own members.
RESERVED_FIELD_NAMES = frozenset(["copy"])
RESERVED_METHOD_NAMES = frozenset(["dispose"])


def check_name(name: str, what: str):
    """Raise :class:`IrError` unless ``name`` is legal in both languages."""
    if not isinstance(name, str) or not name.isidentifier() or not name.isascii():
        raise IrError("%s: '%s' is not a valid identifier" % (what, name))
    if name.startswith("__"):
        raise IrError("%s: names starting with '__' are reserved ('%s')" % (what, name))
    if keyword.iskeyword(name) or name in ("None", "True", "False"):
        raise IrError("%s: '%s' is a Python keyword" % (what, name))
    if name in SV_KEYWORDS:
        raise IrError("%s: '%s' is a SystemVerilog keyword" % (what, name))


#****************************************************************************
#* Universe
#****************************************************************************
class TypeUniverse(object):
    """All the definitions a generator works on.

    Definitions share one namespace. Iteration order is by name, so output
    is independent of the order in which definitions were added.
    """

    def __init__(self):
        self._defs: Dict[str, Definition] = {}

    # -- building ----------------------------------------------------------
    def add(self, d: Definition) -> Definition:
        """Add a definition. Raises :class:`IrError` on a duplicate name."""
        if d.name in self._defs:
            raise IrError("Duplicate definition of '%s'" % d.name)
        self._defs[d.name] = d
        return d

    # -- access ------------------------------------------------------------
    def get(self, name: str) -> Optional[Definition]:
        return self._defs.get(name, None)

    def __contains__(self, name):
        return name in self._defs

    def __len__(self):
        return len(self._defs)

    @property
    def enums(self) -> List[EnumDef]:
        return [d for _, d in sorted(self._defs.items()) if isinstance(d, EnumDef)]

    @property
    def records(self) -> List[RecordDef]:
        return [d for _, d in sorted(self._defs.items()) if isinstance(d, RecordDef)]

    @property
    def interfaces(self) -> List[InterfaceDef]:
        return [d for _, d in sorted(self._defs.items()) if isinstance(d, InterfaceDef)]

    def enum(self, name: str) -> EnumDef:
        d = self._defs.get(name, None)
        if not isinstance(d, EnumDef):
            raise IrError("'%s' is not an enum" % name)
        return d

    def record(self, name: str) -> RecordDef:
        d = self._defs.get(name, None)
        if not isinstance(d, RecordDef):
            raise IrError("'%s' is not a record" % name)
        return d

    def interface(self, name: str) -> InterfaceDef:
        d = self._defs.get(name, None)
        if not isinstance(d, InterfaceDef):
            raise IrError("'%s' is not an interface" % name)
        return d

    def all_fields(self, rec: RecordDef) -> List[FieldDef]:
        """Return a record's fields, base fields first."""
        ret = []
        if rec.base is not None:
            ret.extend(self.all_fields(self.record(rec.base)))
        ret.extend(rec.fields)
        return ret

    # -- resolution --------------------------------------------------------
    def resolve(self, name: str, by_ref: bool = False) -> TypeRef:
        """Return the reference type for a named definition.

        Raises:
            IrError: If ``name`` is undefined, or ``by_ref`` is set for
                something other than a record.
        """
        d = self._defs.get(name, None)
        if d is None:
            raise IrError("Undefined type '%s'" % name)
        if by_ref and not isinstance(d, RecordDef):
            raise IrError("Only records can be passed by reference ('%s')" % name)
        if isinstance(d, EnumDef):
            return EnumRef(name)
        if isinstance(d, RecordDef):
            return RecordRef(name, by_ref)
        return IfRef(name)

    # -- validation --------------------------------------------------------
    def validate(self):
        """Check every definition and reference.

        Raises:
            IrError: On the first problem found; the message names the
                definition and member.
        """
        for d in self._defs.values():
            check_name(d.name, "definition")
            if isinstance(d, EnumDef):
                self._validate_enum(d)
            elif isinstance(d, RecordDef):
                self._validate_record(d)
            else:
                self._validate_interface(d)
        self.dep_order()

    def _validate_enum(self, e: EnumDef):
        if e.width < 1 or e.width > 64:
            raise IrError("enum %s: width must be 1-64 (got %d)" % (e.name, e.width))
        if len(e.values) == 0:
            raise IrError("enum %s: has no values" % e.name)
        names = set()
        vals = set()
        lo = -(1 << (e.width - 1)) if e.signed else 0
        hi = ((1 << (e.width - 1)) if e.signed else (1 << e.width)) - 1
        for n, v in e.values:
            check_name(n, "enum %s value" % e.name)
            if n in names:
                raise IrError("enum %s: duplicate value name '%s'" % (e.name, n))
            if v in vals:
                raise IrError("enum %s: duplicate value %d ('%s')" % (e.name, v, n))
            if v < lo or v > hi:
                raise IrError("enum %s: value %s=%d does not fit in %d bits" % (
                    e.name, n, v, e.width))
            names.add(n)
            vals.add(v)

    def _validate_record(self, r: RecordDef):
        if r.base is not None:
            self.record(r.base)
        names = set()
        for f in self.all_fields(r):
            what = "record %s field %s" % (r.name, f.name)
            check_name(f.name, "record %s field" % r.name)
            if f.name in RESERVED_FIELD_NAMES:
                raise IrError("%s: '%s' is reserved" % (what, f.name))
            if f.name in names:
                raise IrError("%s: duplicate field" % what)
            names.add(f.name)
            self._validate_type(f.type, what, allow_ref=False)

    def _validate_interface(self, i: InterfaceDef):
        names = set()
        for m in i.methods:
            what = "interface %s method %s" % (i.name, m.name)
            check_name(m.name, "interface %s method" % i.name)
            if m.name in RESERVED_METHOD_NAMES:
                raise IrError("%s: '%s' is reserved" % (what, m.name))
            if m.name in names:
                raise IrError("%s: duplicate method" % what)
            names.add(m.name)
            pnames = set()
            for p in m.params:
                check_name(p.name, "%s parameter" % what)
                if p.name == (m.sv_ret_name or "retval"):
                    raise IrError("%s: parameter name '%s' is reserved" % (what, p.name))
                if p.name in pnames:
                    raise IrError("%s: duplicate parameter %s" % (what, p.name))
                pnames.add(p.name)
                self._validate_type(p.type, "%s parameter %s" % (what, p.name), True)
            if m.rtype is not None:
                self._validate_type(m.rtype, "%s return" % what, True)

    def _validate_type(self, t, what, allow_ref):
        if isinstance(t, (ScalarT, BoolT, RealT, StrT, BytesT)):
            return
        if isinstance(t, ListT):
            if isinstance(t.elem, (IfRef,)) or (
                    isinstance(t.elem, RecordRef) and t.elem.by_ref):
                raise IrError("%s: list elements must be values" % what)
            self._validate_type(t.elem, what, False)
            return
        if isinstance(t, EnumRef):
            self.enum(t.name)
            return
        if isinstance(t, RecordRef):
            self.record(t.name)
            if t.by_ref and not allow_ref:
                raise IrError("%s: record fields cannot be references" % what)
            return
        if isinstance(t, IfRef):
            self.interface(t.name)
            if not allow_ref:
                raise IrError("%s: record fields cannot be interfaces" % what)
            return
        raise IrError("%s: unknown type %s" % (what, str(t)))

    # -- ordering ----------------------------------------------------------
    def deps(self, d: Definition) -> List[str]:
        """Return the names ``d`` needs defined before it, by value.

        For a record: its base and the records and enums its fields contain.
        For an interface: the enums and records in its signatures. Interface
        references are not dependencies (they need only a forward
        declaration).
        """
        ret = []

        def add_type(t):
            if isinstance(t, ListT):
                add_type(t.elem)
            elif isinstance(t, (EnumRef, RecordRef)):
                if t.name not in ret:
                    ret.append(t.name)

        if isinstance(d, RecordDef):
            if d.base is not None:
                ret.append(d.base)
            for f in d.fields:
                add_type(f.type)
        elif isinstance(d, InterfaceDef):
            for m in d.methods:
                for p in m.params:
                    add_type(p.type)
                if m.rtype is not None:
                    add_type(m.rtype)
        return ret

    def dep_order(self) -> List[Definition]:
        """Return all definitions, each after the ones it depends on.

        Ties are broken by kind (enums, records, interfaces) and then name,
        so the order is deterministic.

        Raises:
            IrError: If records contain each other by value in a cycle.
        """
        kind_rank = {EnumDef: 0, RecordDef: 1, InterfaceDef: 2}
        ret = []
        state = {}  # name -> 1 (visiting), 2 (done)

        def visit(name, path):
            st = state.get(name, 0)
            if st == 2:
                return
            if st == 1:
                cyc = path[path.index(name):] + [name]
                raise IrError("Records contain each other by value: %s" % " -> ".join(cyc))
            state[name] = 1
            d = self._defs[name]
            for dep in sorted(self.deps(d)):
                if dep in self._defs:
                    visit(dep, path + [name])
            state[name] = 2
            ret.append(d)

        for d in sorted(self._defs.values(), key=lambda d: (kind_rank[type(d)], d.name)):
            visit(d.name, [])
        return ret

    def __eq__(self, other):
        if not isinstance(other, TypeUniverse):
            return False
        return self._defs == other._defs

    def __repr__(self):
        return "TypeUniverse(%s)" % ", ".join(sorted(self._defs.keys()))
