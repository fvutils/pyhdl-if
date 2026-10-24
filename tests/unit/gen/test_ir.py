import json
import os
import pytest

from hdl_if.gen.ir import (
    ScalarT, BoolT, RealT, StrT, BytesT, EnumRef, RecordRef, ListT, IfRef,
    EnumDef, FieldDef, RecordDef, ParamDef, MethodDef, InterfaceDef,
    TypeUniverse, IrError, type_str)
from hdl_if.gen.spec import (
    loads_spec, load_spec, dumps_spec, spec_from_dict, spec_to_dict, parse_type)

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
schema_file = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "doc", "pyhdl-if-v2.schema.json")


def _universe():
    u = TypeUniverse()
    u.add(EnumDef("proto_e", 8, [("TCP", 6), ("UDP", 17)]))
    u.add(RecordDef("hdr", [FieldDef("src", ScalarT(32, False)),
                            FieldDef("proto", EnumRef("proto_e"))]))
    u.add(RecordDef("pkt", [FieldDef("ttl", ScalarT(8, False)),
                            FieldDef("h", RecordRef("hdr")),
                            FieldDef("hs", ListT(RecordRef("hdr"))),
                            FieldDef("data", BytesT())]))
    u.add(InterfaceDef("cb", [MethodDef("notify", False, [ParamDef("v", ScalarT(32, True))])]))
    u.add(InterfaceDef("svc", [
        MethodDef("send", True, [ParamDef("p", RecordRef("pkt", True)),
                                 ParamDef("c", IfRef("cb"))], RecordRef("pkt"))]))
    return u


def test_build_and_validate():
    u = _universe()
    u.validate()
    assert [e.name for e in u.enums] == ["proto_e"]
    assert [r.name for r in u.records] == ["hdr", "pkt"]
    assert [i.name for i in u.interfaces] == ["cb", "svc"]
    assert u.resolve("pkt", by_ref=True) == RecordRef("pkt", True)
    assert u.resolve("cb") == IfRef("cb")
    assert u.resolve("proto_e") == EnumRef("proto_e")


def test_resolve_errors():
    u = _universe()
    with pytest.raises(IrError, match="Undefined type 'nope'"):
        u.resolve("nope")
    with pytest.raises(IrError, match="Only records"):
        u.resolve("cb", by_ref=True)


def test_dep_order():
    u = TypeUniverse()
    # Added in reverse dependency order on purpose
    u.add(InterfaceDef("a_if", [MethodDef("m", False, [ParamDef("p", RecordRef("z_outer"))])]))
    u.add(RecordDef("z_outer", [FieldDef("i", RecordRef("m_inner")),
                                FieldDef("e", EnumRef("e1"))]))
    u.add(RecordDef("m_inner", [FieldDef("e", EnumRef("e1"))]))
    u.add(RecordDef("derived", [FieldDef("x", BoolT())], base="z_outer"))
    u.add(EnumDef("e1", 2, [("A", 0), ("B", 1)]))
    u.validate()
    order = [d.name for d in u.dep_order()]
    assert order.index("e1") < order.index("m_inner") < order.index("z_outer")
    assert order.index("z_outer") < order.index("derived")
    assert order.index("z_outer") < order.index("a_if")
    # Deterministic
    assert order == [d.name for d in u.dep_order()]


def test_copy_cycle_rejected():
    u = TypeUniverse()
    u.add(RecordDef("a", [FieldDef("b", RecordRef("b"))]))
    u.add(RecordDef("b", [FieldDef("a", RecordRef("a"))]))
    with pytest.raises(IrError, match="by value: a -> b -> a"):
        u.validate()


def test_self_copy_cycle_rejected():
    u = TypeUniverse()
    u.add(RecordDef("node", [FieldDef("next", RecordRef("node"))]))
    with pytest.raises(IrError, match="node -> node"):
        u.validate()


def test_interface_cycle_allowed():
    u = TypeUniverse()
    u.add(InterfaceDef("a", [MethodDef("m", False, [ParamDef("b", IfRef("b"))])]))
    u.add(InterfaceDef("b", [MethodDef("m", False, [ParamDef("a", IfRef("a"))])]))
    u.validate()


@pytest.mark.parametrize("build,msg", [
    (lambda u: u.add(RecordDef("r", [FieldDef("logic", BoolT())])), "SystemVerilog keyword"),
    (lambda u: u.add(RecordDef("r", [FieldDef("lambda", BoolT())])), "Python keyword"),
    (lambda u: u.add(RecordDef("r", [FieldDef("__x", BoolT())])), "reserved"),
    (lambda u: u.add(RecordDef("r", [FieldDef("copy", BoolT())])), "reserved"),
    (lambda u: u.add(RecordDef("r", [FieldDef("a", BoolT()), FieldDef("a", BoolT())])), "duplicate field"),
    (lambda u: u.add(RecordDef("r", [FieldDef("a", RecordRef("r2", True))])) and
        u.add(RecordDef("r2")), "cannot be references"),
    (lambda u: u.add(RecordDef("r", [FieldDef("a", RecordRef("missing"))])), "not a record"),
    (lambda u: u.add(EnumDef("e", 2, [("A", 4)])), "does not fit"),
    (lambda u: u.add(EnumDef("e", 2, [("A", 1), ("B", 1)])), "duplicate value"),
    (lambda u: u.add(EnumDef("e", 2, [])), "no values"),
    (lambda u: u.add(InterfaceDef("i", [MethodDef("dispose")])), "reserved"),
    (lambda u: u.add(InterfaceDef("i", [MethodDef("m", params=[ParamDef("retval", BoolT())])])), "reserved"),
    (lambda u: u.add(InterfaceDef("i", [MethodDef("m"), MethodDef("m")])), "duplicate method"),
])
def test_validation_errors(build, msg):
    u = TypeUniverse()
    build(u)
    with pytest.raises(IrError, match=msg):
        u.validate()


def test_duplicate_definition():
    u = TypeUniverse()
    u.add(RecordDef("r"))
    with pytest.raises(IrError, match="Duplicate definition of 'r'"):
        u.add(EnumDef("r", 1, [("A", 0)]))


def test_all_fields_with_base():
    u = TypeUniverse()
    u.add(RecordDef("base", [FieldDef("a", BoolT())]))
    u.add(RecordDef("d", [FieldDef("b", BoolT())], base="base"))
    assert [f.name for f in u.all_fields(u.record("d"))] == ["a", "b"]
    u.add(RecordDef("d2", [FieldDef("a", BoolT())], base="base"))
    with pytest.raises(IrError, match="duplicate field"):
        u.validate()


@pytest.mark.parametrize("s,t", [
    ("u8", ScalarT(8, False)), ("i32", ScalarT(32, True)), ("u96", ScalarT(96, False)),
    ("bool", BoolT()), ("f64", RealT(64)), ("f32", RealT(32)), ("str", StrT()),
    ("bytes", BytesT()), ("list<u8>", ListT(ScalarT(8, False))),
    ("list<list<str>>", ListT(ListT(StrT()))),
])
def test_type_spelling_round_trip(s, t):
    u = TypeUniverse()
    assert parse_type(s, u) == t
    assert type_str(t) == s


def test_spec_round_trip():
    u = load_spec(os.path.join(data_dir, "spike.json"))
    text = dumps_spec(u)
    u2 = loads_spec(text)
    assert u2 == u
    assert dumps_spec(u2) == text


def test_spec_dump_is_sorted_and_stable():
    u = _universe()
    d = spec_to_dict(u)
    assert [r["name"] for r in d["records"]] == ["hdr", "pkt"]
    assert [f["name"] for f in d["records"][1]["fields"]] == ["ttl", "h", "hs", "data"]
    assert d["interfaces"][1]["methods"][0] == {
        "name": "send", "kind": "task",
        "params": [{"name": "p", "type": "ref<pkt>"}, {"name": "c", "type": "cb"}],
        "returns": "pkt"}


def test_spec_forward_references():
    # Types may refer to definitions that appear later in the file
    u = spec_from_dict({
        "pyhdl-if-spec": 2,
        "interfaces": [{"name": "i", "methods": [
            {"name": "m", "params": [{"name": "r", "type": "ref<r>"}]}]}],
        "records": [{"name": "r", "fields": [{"name": "e", "type": "e"}]}],
        "enums": [{"name": "e", "width": 1, "values": [{"name": "X", "value": 0}]}]})
    assert u.interface("i").methods[0].params[0].type == RecordRef("r", True)


@pytest.mark.parametrize("d,msg", [
    ({"pyhdl-if-spec": 1}, "Not a pyhdl-if v2 spec"),
    ({}, "Not a pyhdl-if v2 spec"),
    ({"pyhdl-if-spec": 2, "records": [{"name": "r", "fields": [{"name": "a", "type": "nope"}]}]},
     "record r field a: Undefined type 'nope'"),
    ({"pyhdl-if-spec": 2, "records": [{"name": "r", "fields": [{"name": "a", "type": "u8<"}]}]},
     "Malformed type"),
    ({"pyhdl-if-spec": 2, "interfaces": [{"name": "i", "methods": [{"name": "m", "kind": "proc"}]}]},
     "kind must be"),
    ({"pyhdl-if-spec": 2, "records": [{"fields": []}]}, "missing 'name'"),
])
def test_spec_errors(d, msg):
    with pytest.raises(IrError, match=msg):
        spec_from_dict(d)


def test_bad_json():
    with pytest.raises(IrError, match="not valid JSON"):
        loads_spec("{")


def _schema():
    with open(schema_file) as fp:
        return json.load(fp)


def test_schema_is_valid():
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.Draft7Validator.check_schema(_schema())


def test_golden_specs_validate():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _schema()
    for f in os.listdir(data_dir):
        if f.endswith(".json"):
            with open(os.path.join(data_dir, f)) as fp:
                jsonschema.validate(json.load(fp), schema)


def test_dumped_spec_validates():
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.validate(spec_to_dict(_universe()), _schema())
