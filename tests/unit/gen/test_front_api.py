"""Mapping @api classes onto the neutral description (Phase 11)."""
import ctypes as ct
import dataclasses as dc

import pytest

from hdl_if.decorators import api, exp, imp
from hdl_if.impl.call.api_def_rgy import ApiDefRgy
from hdl_if.gen.ir import ScalarT, BoolT, StrT, RealT, RecordRef, IrError
from hdl_if.gen.front.api import interface_from_api, IMPL_SV, IMPL_PY
from hdl_if.gen.front.py import PyFrontEnd
from hdl_if.gen.sv import gen_sv
from hdl_if.gen.py import gen_py


@dc.dataclass
class Sample:
    v: ct.c_uint16 = 0


def _api(cls):
    for ad in ApiDefRgy.inst().getApis():
        if ad.pycls is cls:
            return ad
    raise KeyError(cls)


def test_directions_and_types():
    @api
    class Bfm(object):
        @imp
        async def write(self, addr: ct.c_uint32, data: ct.c_uint64) -> None: ...

        @imp
        def status(self) -> ct.c_int32: ...

        @exp
        async def observed(self, s: Sample, ok: bool) -> str:
            return ""

        @exp
        def scale(self, x: float) -> float:
            return x

    fe = PyFrontEnd()
    idef, impl = interface_from_api(_api(Bfm), fe)
    assert impl == {"write": IMPL_SV, "status": IMPL_SV, "observed": IMPL_PY, "scale": IMPL_PY}
    m = {x.name: x for x in idef.methods}
    assert m["write"].is_task and [p.type for p in m["write"].params] == [
        ScalarT(32, False), ScalarT(64, False)]
    assert not m["status"].is_task and m["status"].rtype == ScalarT(32, True)
    assert m["observed"].is_task and m["observed"].params[0].type == RecordRef("Sample")
    assert m["observed"].rtype == StrT() and m["observed"].params[1].type == BoolT()
    assert m["scale"].rtype == RealT(64)
    # The result goes through the back ends like any other interface
    fe.u.validate()
    assert "interface class Bfm;" in gen_sv(fe.u, "p", "m", "s")
    assert "class Bfm_sv_proxy" in gen_py(fe.u, "s")


def test_unsupported_types():
    class Pt(ct.Structure):
        _fields_ = [("x", ct.c_int32)]

    @api
    class Old(object):
        @imp
        def f(self, p: Pt) -> None: ...

    with pytest.raises(IrError, match="Old.f parameter p: type Pt has no SystemVerilog equivalent"):
        interface_from_api(_api(Old))
