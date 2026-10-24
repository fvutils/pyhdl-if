"""Python-only tests of the record/interface runtime (hdl_if.rt)."""
import asyncio
import dataclasses as dc
import enum
import gc
import sys
from typing import List, Optional, Protocol

import pytest

from hdl_if import rt
from hdl_if.rt import Ref, u8, i8, i32, u64, uint, sint


class Color(enum.IntEnum):
    RED = 1
    GREEN = 2


@dc.dataclass
class Inner(object):
    a: u8 = 0
    c: Color = Color.RED


@dc.dataclass
class Outer(object):
    i: Inner = dc.field(default_factory=Inner)
    items: List[Inner] = dc.field(default_factory=list)
    data: bytes = b""
    wide: uint(100) = 0
    swide: sint(72) = 0
    name: str = ""
    f: float = 0.0
    b: bool = False
    opt: Optional[Inner] = None


class FakeEp(object):
    """Records calls; answers from a dict of method -> result."""

    def __init__(self):
        self.calls = []
        self.results = {}

    def invoke_hdl_f(self, obj_id, method, args):
        self.calls.append((obj_id, method, args))
        return self.results.get(method, None)


@pytest.fixture
def ep():
    e = FakeEp()
    rt.set_endpoint(e)
    rt.take_released()
    yield e
    rt.set_endpoint(None)


def test_payload_round_trip():
    o = Outer(i=Inner(5, Color.GREEN), items=[Inner(1), Inner(2, Color.GREEN)],
              data=b"\x00\xff", wide=(1 << 99) | 3, swide=-2, name="x",
              f=1.5, b=True, opt=Inner(9))
    p = rt.rec_to_sv(o)
    assert p == ((5, 2), [(1, 1), (2, 2)], [0, 255],
                 "8" + "0" * 23 + "3", "ff" * 8 + "fe", "x", 1.5, True, (9, 1))
    o2 = rt.rec_from_sv(Outer, p)
    assert o2 == o
    assert type(o2.i.c) is Color


def test_none_record():
    o = Outer()
    p = rt.rec_to_sv(o)
    assert p[-1] is None
    assert rt.rec_from_sv(Outer, p).opt is None
    assert rt.rec_from_sv(Outer, None) is None


def test_copy_is_deep():
    o = Outer(items=[Inner(1)])
    c = rt.copy(o)
    c.items[0].a = 7
    c.i.a = 3
    assert o.items[0].a == 1 and o.i.a == 0


def test_ctypes_hints():
    import ctypes

    @dc.dataclass
    class C(object):
        a: ctypes.c_uint8 = 0
        b: ctypes.c_int32 = 0
    assert rt.rec_from_sv(C, (1, -2)) == C(1, -2)


def test_unsupported_hint():
    @dc.dataclass
    class Bad(object):
        a: dict = None
    with pytest.raises(TypeError, match="Bad.a: Type .*dict"):
        rt.rec_to_sv(Bad())


def test_get_set_field():
    o = Outer()
    rt.set_field(o.i, "c", 2)
    assert o.i.c is Color.GREEN
    rt.set_field(o, "data", [1, 2])
    assert o.data == b"\x01\x02"
    assert rt.get_field(o, "wide") == "0"
    rt.set_field(o, "i", (4, 1))
    assert o.i == Inner(4, Color.RED)


class InnerRef(rt.SvRef):
    __slots__ = ()
    _rec_type = Inner

    @property
    def a(self):
        return self._call_f("get_a", ())


def test_sv_ref_calls_endpoint(ep):
    r = rt.sv_obj_new(InnerRef, 7)
    ep.results["get_a"] = 42
    assert r.a == 42
    assert ep.calls[-1] == (7, "get_a", ())
    assert rt.sv_obj_id(r) == 7
    assert rt.sv_obj_id(Inner()) == -1


def test_sv_ref_copy(ep):
    r = rt.sv_obj_new(InnerRef, 3)
    ep.results["__copy"] = (9, 2)
    c = r.copy()
    assert c == Inner(9, Color.GREEN)
    assert rt.copy(r) == c
    # A reference passed where a copy is expected is snapshotted
    assert rt.rec_to_sv(r) == (9, 2)
    assert rt.conv_for(Inner).to_sv(r) == (9, 2)


def test_release_is_deferred_and_deterministic(ep):
    r = rt.sv_obj_new(InnerRef, 11)
    r2 = rt.sv_obj_new(InnerRef, 12)
    del r
    assert rt.take_released() == [11]
    assert rt.take_released() == []
    del r2
    assert rt.take_released() == [12]
    # Nothing called into SV
    assert ep.calls == []


def test_finalizer_safe_without_endpoint():
    rt.set_endpoint(None)
    r = rt.sv_obj_new(InnerRef, 5)
    del r
    gc.collect()
    assert 5 in rt.take_released()


def test_finalizer_never_raises(monkeypatch):
    r = rt.sv_obj_new(InnerRef, 6)
    # Simulate interpreter shutdown: module globals torn down
    import hdl_if.rt.obj as obj_m
    monkeypatch.setattr(obj_m, "_released", None)
    r.__del__()  # must not raise
    monkeypatch.undo()
    rt.take_released()


def test_endpoint_missing_is_clear():
    rt.set_endpoint(None)
    from hdl_if.impl.call.context import Context
    saved = Context.inst()._endpoints
    Context.inst()._endpoints = []
    try:
        r = rt.sv_obj_new(InnerRef, 1)
        with pytest.raises(RuntimeError, match="No simulator endpoint"):
            r.a
    finally:
        Context.inst()._endpoints = saved


def test_ref_hint_is_identity():
    c = rt.conv_for(Ref[Inner])
    o = Inner()
    assert c.to_sv(o) is o and c.from_sv(o) is o
    assert rt.conv_for(Ref[Inner]) is c


class Svc(Protocol):
    def ping(self, v: i32) -> i32: ...


class SvcProxy(rt.SvProxy):
    __slots__ = ()


class SvcAdapter(rt.PyAdapter):
    __slots__ = ()


def test_interface_conv():
    rt.register_interface(Svc, SvcProxy, SvcAdapter)
    c = rt.conv_for(Svc)

    class Impl(object):
        def ping(self, v):
            return v

    impl = Impl()
    a = c.to_sv(impl)
    assert isinstance(a, SvcAdapter) and a._impl is impl
    assert c.from_sv(a) is impl
    assert c.to_sv(a) is a
    p = rt.sv_obj_new(SvcProxy, 2)
    assert c.to_sv(p) is p and c.from_sv(p) is p
    assert c.to_sv(None) is None
    assert rt.py_adapt(SvcAdapter, impl)._impl is impl
    assert rt.py_adapt(SvcAdapter, a) is a
    assert rt.interface_info(Svc) == (SvcProxy, SvcAdapter)


def test_invoke_py_t_delivers_result_and_errors(ep, capsys):
    got = []
    ep.response_py_t = lambda sem_id, res: got.append((sem_id, res))

    class Impl(object):
        async def ok(self, v):
            return v + 1

        async def bad(self):
            raise ValueError("boom")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    from hdl_if.backend import Backend

    class Be(object):
        def mkTask(self, coro):
            return loop.create_task(coro)

        def idle(self):
            pass
    saved = Backend._inst
    Backend._inst = Be()
    try:
        rt.invoke_py_t(1, Impl(), "ok", (41,))
        rt.invoke_py_t(2, Impl(), "bad", ())
        loop.run_until_complete(asyncio.sleep(0))
        loop.run_until_complete(asyncio.sleep(0))
    finally:
        Backend._inst = saved
        loop.close()
    assert (1, 42) in got
    assert (2, rt.ERROR) in got
    assert "ValueError: boom" in capsys.readouterr().err
