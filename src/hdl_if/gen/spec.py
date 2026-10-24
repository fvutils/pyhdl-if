#****************************************************************************
#* spec.py
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
"""Spec format v2: a JSON description of records, enums and interfaces.

Example::

    {
      "pyhdl-if-spec": 2,
      "enums": [
        {"name": "proto_e", "width": 8,
         "values": [{"name": "TCP", "value": 6}, {"name": "UDP", "value": 17}]}
      ],
      "records": [
        {"name": "pkt", "fields": [
          {"name": "ttl", "type": "u8"},
          {"name": "payload", "type": "bytes"},
          {"name": "kind", "type": "proto_e"}]}
      ],
      "interfaces": [
        {"name": "pkt_svc", "methods": [
          {"name": "send", "kind": "task",
           "params": [{"name": "p", "type": "pkt"}], "returns": "u32"}]}
      ]
    }

Type spellings: ``u<N>`` / ``i<N>`` (unsigned / signed integer of N bits),
``bool``, ``f32``, ``f64``, ``str``, ``bytes``, ``list<T>``, the name of an
enum, record or interface, and ``ref<record>`` for a record passed by
reference. The schema is ``doc/pyhdl-if-v2.schema.json``.

:func:`dump_spec` output is deterministic: definitions are sorted by name;
fields, enum values, methods and parameters keep their order.

The v1 format (``api_def_from_json``) is unrelated and unchanged.
"""
import json
import re
from typing import Any, Dict

from .ir import (
    ScalarT, BoolT, RealT, StrT, BytesT, EnumRef, RecordRef, ListT, IfRef,
    EnumDef, FieldDef, RecordDef, ParamDef, MethodDef, InterfaceDef,
    TypeUniverse, IrError, type_str,
)

__all__ = ["SPEC_VERSION", "load_spec", "loads_spec", "spec_from_dict",
           "dump_spec", "dumps_spec", "spec_to_dict", "parse_type"]

#: Value of the ``pyhdl-if-spec`` key this module reads and writes.
SPEC_VERSION = 2

_INT_RE = re.compile(r"^([ui])(\d+)$")


def parse_type(s: str, u: TypeUniverse):
    """Parse a type spelling, resolving names against ``u``.

    Raises:
        IrError: If the spelling is malformed or names an undefined type.
    """
    if not isinstance(s, str):
        raise IrError("Type must be a string (got %r)" % (s,))
    s = s.strip()
    m = _INT_RE.match(s)
    if m is not None:
        return ScalarT(int(m.group(2)), m.group(1) == "i")
    if s == "bool":
        return BoolT()
    if s in ("f32", "f64"):
        return RealT(int(s[1:]))
    if s == "str":
        return StrT()
    if s == "bytes":
        return BytesT()
    if s.startswith("list<") and s.endswith(">"):
        return ListT(parse_type(s[5:-1], u))
    if s.startswith("ref<") and s.endswith(">"):
        return u.resolve(s[4:-1].strip(), by_ref=True)
    if s.isidentifier():
        return u.resolve(s)
    raise IrError("Malformed type '%s'" % s)


def _req(d: Dict, key: str, what: str):
    if key not in d:
        raise IrError("%s: missing '%s'" % (what, key))
    return d[key]


def spec_from_dict(d: Dict[str, Any]) -> TypeUniverse:
    """Build a :class:`TypeUniverse` from a parsed v2 spec.

    Raises:
        IrError: If the spec is malformed or invalid.
    """
    if not isinstance(d, dict):
        raise IrError("Spec must be a JSON object")
    ver = d.get("pyhdl-if-spec", None)
    if ver != SPEC_VERSION:
        raise IrError("Not a pyhdl-if v%d spec ('pyhdl-if-spec' is %r)" % (
            SPEC_VERSION, ver))

    u = TypeUniverse()

    # Pass 1: names, so types can refer to definitions in any order
    for e in d.get("enums", []):
        what = "enum %s" % e.get("name", "?")
        values = []
        for v in _req(e, "values", what):
            values.append((_req(v, "name", what), int(_req(v, "value", what))))
        u.add(EnumDef(
            name=_req(e, "name", "enum"),
            width=int(_req(e, "width", what)),
            values=values,
            signed=bool(e.get("signed", False)),
            py_ref=e.get("py_ref", None),
            sv_ref=e.get("sv_ref", None)))
    for r in d.get("records", []):
        u.add(RecordDef(
            name=_req(r, "name", "record"),
            base=r.get("base", None),
            py_ref=r.get("py_ref", None),
            sv_ref=r.get("sv_ref", None)))
    for i in d.get("interfaces", []):
        u.add(InterfaceDef(
            name=_req(i, "name", "interface"),
            py_ref=i.get("py_ref", None),
            sv_ref=i.get("sv_ref", None)))

    # Pass 2: members
    for r in d.get("records", []):
        rd = u.record(r["name"])
        for f in r.get("fields", []):
            what = "record %s field %s" % (rd.name, f.get("name", "?"))
            try:
                t = parse_type(_req(f, "type", what), u)
            except IrError as e:
                raise IrError("%s: %s" % (what, str(e)))
            rd.fields.append(FieldDef(_req(f, "name", what), t, f.get("sv_type", None)))
    for i in d.get("interfaces", []):
        idef = u.interface(i["name"])
        for m in i.get("methods", []):
            what = "interface %s method %s" % (idef.name, m.get("name", "?"))
            kind = m.get("kind", "func")
            if kind not in ("func", "task"):
                raise IrError("%s: kind must be 'func' or 'task'" % what)
            md = MethodDef(name=_req(m, "name", what), is_task=(kind == "task"),
                           sv_rtype=m.get("sv_returns", None),
                           sv_ret_name=m.get("sv_ret_name", None))
            for p in m.get("params", []):
                pwhat = "%s parameter %s" % (what, p.get("name", "?"))
                try:
                    t = parse_type(_req(p, "type", pwhat), u)
                except IrError as e:
                    raise IrError("%s: %s" % (pwhat, str(e)))
                md.params.append(ParamDef(_req(p, "name", pwhat), t, p.get("sv_type", None)))
            if m.get("returns", None) is not None:
                try:
                    md.rtype = parse_type(m["returns"], u)
                except IrError as e:
                    raise IrError("%s return: %s" % (what, str(e)))
            idef.methods.append(md)

    u.validate()
    return u


def loads_spec(text: str) -> TypeUniverse:
    """Parse a v2 spec from a JSON string."""
    try:
        d = json.loads(text)
    except json.JSONDecodeError as e:
        raise IrError("Spec is not valid JSON: %s" % str(e))
    return spec_from_dict(d)


def load_spec(path: str) -> TypeUniverse:
    """Load a v2 spec from a JSON file."""
    with open(path, "r") as fp:
        try:
            return loads_spec(fp.read())
        except IrError as e:
            raise IrError("%s: %s" % (path, str(e)))


def _refs(d, out):
    if d.py_ref is not None:
        out["py_ref"] = d.py_ref
    if d.sv_ref is not None:
        out["sv_ref"] = d.sv_ref
    return out


def _typed(f) -> Dict[str, Any]:
    ret = {"name": f.name, "type": type_str(f.type)}
    if f.sv_type is not None:
        ret["sv_type"] = f.sv_type
    return ret


def spec_to_dict(u: TypeUniverse) -> Dict[str, Any]:
    """Return the v2 spec for ``u`` as a JSON-ready dict."""
    ret = {"pyhdl-if-spec": SPEC_VERSION}
    if u.enums:
        ret["enums"] = []
        for e in u.enums:
            ed = {"name": e.name, "width": e.width}
            if e.signed:
                ed["signed"] = True
            ed["values"] = [{"name": n, "value": v} for n, v in e.values]
            ret["enums"].append(_refs(e, ed))
    if u.records:
        ret["records"] = []
        for r in u.records:
            rd = {"name": r.name}
            if r.base is not None:
                rd["base"] = r.base
            rd["fields"] = [_typed(f) for f in r.fields]
            ret["records"].append(_refs(r, rd))
    if u.interfaces:
        ret["interfaces"] = []
        for i in u.interfaces:
            methods = []
            for m in i.methods:
                md = {"name": m.name, "kind": "task" if m.is_task else "func"}
                md["params"] = [_typed(p) for p in m.params]
                if m.rtype is not None:
                    md["returns"] = type_str(m.rtype)
                if m.sv_rtype is not None:
                    md["sv_returns"] = m.sv_rtype
                if m.sv_ret_name is not None:
                    md["sv_ret_name"] = m.sv_ret_name
                methods.append(md)
            ret["interfaces"].append(_refs(i, {"name": i.name, "methods": methods}))
    return ret


def dumps_spec(u: TypeUniverse) -> str:
    """Return the v2 spec for ``u`` as JSON text (deterministic)."""
    return json.dumps(spec_to_dict(u), indent=2) + "\n"


def dump_spec(u: TypeUniverse, path: str):
    """Write the v2 spec for ``u`` to a file."""
    with open(path, "w") as fp:
        fp.write(dumps_spec(u))
