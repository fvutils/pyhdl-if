import dataclasses as dc
import enum
import os
import sys
import types
from typing import Dict, List, Protocol, Union

import pytest

from hdl_if.rt import Ref, u8
from hdl_if.gen.ir import (
    ScalarT, BoolT, RealT, StrT, BytesT, EnumRef, RecordRef, ListT, IfRef,
    IrError)
from hdl_if.gen.front.py import PyFrontEnd, universe_from_py
from hdl_if.gen.spec import load_spec, spec_to_dict

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(data_dir))))


@pytest.fixture(autouse=True)
def pymods_path():
    sys.path.insert(0, os.path.join(data_dir, "pymods"))
    yield
    sys.path.pop(0)


def test_basic_module():
    u = universe_from_py(["fe_basic"])
    assert sorted(d.name for d in u.enums) == ["Color", "Sign", "Wide"]
    assert u.enum("Color").width == 16 and not u.enum("Color").signed
    assert u.enum("Sign").width == 8 and u.enum("Sign").signed
    assert u.enum("Wide").width == 4
    assert u.enum("Color").py_ref == "fe_basic.Color"

    outer = {f.name: f.type for f in u.record("Outer").fields}
    assert outer == {
        "i": RecordRef("Inner"), "items": ListT(RecordRef("Inner")),
        "nums": ListT(ScalarT(64, True)), "data": BytesT(),
        "w": ScalarT(100, False), "o": RecordRef("Inner"),
        "ct": ScalarT(16, False), "cb": BoolT(), "cf": RealT(32),
        "f": RealT(64), "s": StrT(), "b": BoolT()}
    d = u.record("Derived")
    assert d.base == "Outer" and [f.name for f in d.fields] == ["extra"]

    svc = u.interface("Svc")
    assert [m.name for m in svc.methods] == ["get", "put"]
    put = svc.methods[1]
    assert put.is_task and put.rtype == BoolT()
    assert [(p.name, p.type) for p in put.params] == [
        ("p", RecordRef("Outer", True)), ("cb", IfRef("Cb"))]
    assert svc.methods[0].rtype == RecordRef("Outer")
    assert [m.name for m in u.interface("SvcPlus").methods] == ["more", "get", "put"]
    assert u.interface("Cb").methods[0].rtype is None
    assert "NotExported" not in u


def test_include_exclude():
    u = universe_from_py(["fe_basic"], include=["fe_basic.Svc"])
    # Svc and everything it uses, nothing else
    assert sorted(d.name for d in u.records) == ["Inner", "Outer"]
    assert sorted(d.name for d in u.interfaces) == ["Cb", "Svc"]
    assert "Sign" not in u
    u = universe_from_py(["fe_basic"], exclude=["fe_basic.Svc*", "fe_basic.Derived"])
    assert "Svc" not in u and "Derived" not in u and "Outer" in u


def test_round_trip_with_generated_module():
    """The Python front end reads back what the Python back end wrote."""
    sys.path.insert(0, os.path.join(root_dir, "tests/unit/data/spike_records"))
    try:
        u = universe_from_py(["spike_api"])
    finally:
        sys.path.pop(0)
    expect = spec_to_dict(load_spec(os.path.join(data_dir, "spike.json")))
    got = spec_to_dict(u)
    for k in ("enums", "records", "interfaces"):
        for d in got[k]:
            assert d.pop("py_ref").startswith("spike_api.")
    assert got == expect


def _mod(**classes):
    m = types.ModuleType("fe_tmp")
    for k, v in classes.items():
        v.__module__ = "fe_tmp"
        setattr(m, k, v)
    return m


def _err(cls, msg):
    fe = PyFrontEnd()
    with pytest.raises(IrError, match=msg):
        fe.add_class(cls)


def test_errors():
    @dc.dataclass
    class BadField:
        d: Dict[str, int] = None
    _err(BadField, r"BadField.d: type Dict.*no SystemVerilog equivalent")

    @dc.dataclass
    class NoHint:
        x = 1
        y: "Undefined" = 0
    _err(NoHint, "cannot resolve type hints")

    class E(enum.Enum):
        A = 1

    @dc.dataclass
    class BadEnum:
        e: E = E.A
    _err(BadEnum, "must derive from enum.IntEnum")

    @dc.dataclass
    class BadUnion:
        u: Union[int, str] = 0
    _err(BadUnion, "unions other than Optional")

    @dc.dataclass
    class BadRef:
        pass

    @dc.dataclass
    class RefField:
        r: Ref[BadRef] = None
    _err(RefField, "cannot be references")

    class NotDc:
        pass

    class P(Protocol):
        def m(self, r: Ref[NotDc]) -> None: ...
    _err(P, "Ref.* must name a dataclass")

    class P2(Protocol):
        def m(self, x) -> None: ...
    _err(P2, "parameter x has no type annotation")

    class P3(Protocol):
        def m(self, *args: int) -> None: ...
    _err(P3, "only plain positional parameters")

    @dc.dataclass
    class ListRef:
        l: List[Ref[BadRef]] = None
    _err(ListRef, "list elements must be values")

    _err(NotDc, "is not a dataclass, IntEnum or Protocol")


def test_duplicate_names_in_two_modules():
    @dc.dataclass
    class pkt:
        a: u8 = 0
    pkt.__qualname__ = "pkt"
    m1 = _mod(pkt=pkt)

    @dc.dataclass
    class pkt:  # noqa: F811
        b: u8 = 0
    pkt.__module__ = "fe_tmp2"
    m2 = types.ModuleType("fe_tmp2")
    m2.pkt = pkt
    fe = PyFrontEnd()
    fe.add_module(m1)
    with pytest.raises(IrError, match="Two definitions named 'pkt'"):
        fe.add_module(m2)


def test_import_error():
    with pytest.raises(IrError, match="Failed to import module 'no_such_mod'"):
        universe_from_py(["no_such_mod"])
