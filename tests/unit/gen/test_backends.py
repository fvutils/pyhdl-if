"""Golden-file and behavior tests of the Python and SV back ends."""
import importlib
import os
import shutil
import subprocess
import sys

import pytest

from hdl_if import rt
from hdl_if.gen.ir import (
    ScalarT, BoolT, ListT, RecordRef, EnumRef, IfRef, EnumDef, FieldDef,
    RecordDef, ParamDef, MethodDef, InterfaceDef, TypeUniverse, IrError)
from hdl_if.gen.spec import load_spec, spec_from_dict, spec_to_dict
from hdl_if.gen.sv import gen_sv
from hdl_if.gen.py import gen_py

unit_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(os.path.dirname(unit_dir))
sys.path.insert(0, os.path.join(root_dir, "scripts"))
import gen_records_goldens as goldens  # noqa: E402


@pytest.mark.parametrize("spec,pkg,mod,outdir", goldens.GOLDENS)
def test_goldens_up_to_date(spec, pkg, mod, outdir):
    """Checked-in generated files match the generators.

    After an intended change, run scripts/gen_records_goldens.py.
    """
    for name, text in goldens.generate(spec, pkg, mod).items():
        with open(os.path.join(root_dir, outdir, name)) as fp:
            assert fp.read() == text, "%s/%s is stale" % (outdir, name)


def test_output_independent_of_definition_order():
    u = load_spec(os.path.join(root_dir, "tests/unit/gen/data/types.json"))
    d = spec_to_dict(u)
    for k in ("enums", "records", "interfaces"):
        d[k] = list(reversed(d[k]))
    u2 = spec_from_dict(d)
    assert gen_sv(u2, "p", "m", "s") == gen_sv(u, "p", "m", "s")
    assert gen_py(u2, "s") == gen_py(u, "s")


@pytest.mark.skipif(shutil.which("python3.9") is None, reason="python3.9 not found")
@pytest.mark.parametrize("spec,pkg,mod,outdir", goldens.GOLDENS)
def test_py_compiles_on_39(spec, pkg, mod, outdir):
    path = os.path.join(root_dir, outdir, mod + ".py")
    subprocess.check_call(["python3.9", "-m", "py_compile", path])


@pytest.mark.skipif(shutil.which("verilator") is None, reason="verilator not found")
@pytest.mark.parametrize("spec,pkg,mod,outdir", goldens.GOLDENS)
def test_sv_lints(spec, pkg, mod, outdir, tmpdir):
    dpi = os.path.join(root_dir, "src", "hdl_if", "share", "dpi")
    res = subprocess.run(
        ["verilator", "--lint-only", "-Wno-fatal", "-Wno-WIDTH", "-Wno-lint",
         "-Wno-style", "-Wno-SHORTREAL", "-I" + dpi,
         os.path.join(dpi, "pyhdl_if.sv"),
         os.path.join(root_dir, outdir, pkg + ".sv"),
         "--top-module", pkg, "--Mdir", str(tmpdir)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert res.returncode == 0, res.stdout
    assert "%Error" not in res.stdout, res.stdout


class FakeEp(object):
    def __init__(self):
        self.calls = []
        self.results = {}

    def invoke_hdl_f(self, obj_id, method, args):
        self.calls.append((obj_id, method, args))
        return self.results.get(method, None)


@pytest.fixture
def types_api():
    sys.path.insert(0, os.path.join(root_dir, "tests/unit/data/records_types"))
    try:
        yield importlib.import_module("types_api")
    finally:
        sys.path.pop(0)


@pytest.fixture
def ep():
    e = FakeEp()
    rt.set_endpoint(e)
    yield e
    rt.set_endpoint(None)
    rt.take_released()


def test_generated_dataclasses(types_api):
    t = types_api
    d = t.derived_rec(a=1, b=-5, c=(1 << 64) - 1, d=-(1 << 63), items=[t.base_rec(b=3)],
                      grid=[[1, 2], []], strs=["x"], w=-(1 << 79), sev=t.sev_e.SEV_LOW,
                      big=t.big_e.BIG_TOP, blobs=[b"\x00"], flag=True, x=0.5)
    assert isinstance(d, t.base_rec)
    p = rt.rec_to_sv(d)
    assert rt.rec_from_sv(t.derived_rec, p) == d
    c = d.copy()
    c.items[0].b = 9
    assert d.items[0].b == 3
    assert t.empty_rec() == t.empty_rec()
    assert t.derived_rec().sev is t.sev_e.SEV_LOW


def test_generated_sv_ref(types_api, ep):
    t = types_api
    r = rt.sv_obj_new(t.derived_rec_sv_ref, 4)
    assert isinstance(r, t.base_rec_sv_ref)
    ep.results["get_w"] = "ffff" + "0" * 16
    assert r.w == -(1 << 64)
    ep.results["get_sev"] = 0
    assert r.sev is t.sev_e.SEV_MID
    r.grid = [[1]]
    assert ep.calls[-1] == (4, "set_grid", ([[1]],))
    r.b = -1
    assert ep.calls[-1] == (4, "set_b", (-1,))
    r.blobs = [b"\x01\x02"]
    assert ep.calls[-1] == (4, "set_blobs", ([[1, 2]],))


def test_generated_sv_proxy(types_api, ep):
    t = types_api
    s = rt.sv_obj_new(t.svc2_sv_proxy, 9)
    ep.results["f_list"] = [rt.rec_to_sv(t.derived_rec(b=2))]
    out = s.f_list([t.derived_rec(b=1)])
    assert out == [t.derived_rec(b=2)]
    assert ep.calls[-1][1] == "f_list"
    assert ep.calls[-1][2][0][0][1] == 1
    ep.results["f_wide"] = "f" * 25
    assert s.f_wide(-1) == (1 << 100) - 1
    assert ep.calls[-1][2] == ("f" * 20,)
    ep.results["f_names"] = 5
    assert s.f_names(1, 2, 3, 4, 5, 6) == 5
    # Interfaces: a Python implementation is wrapped in the adapter
    impl = object()
    s.f_if(impl)
    sent = ep.calls[-1][2][0]
    assert isinstance(sent, t.svc2_py_adapter) and sent._impl is impl


def test_generated_py_adapter(types_api):
    t = types_api

    class Impl(object):
        def f_list(self, l):
            assert all(type(x) is t.derived_rec for x in l)
            return [x.copy() for x in reversed(l)]

        def f_enum(self, e):
            assert e is t.sev_e.SEV_HIGH
            return t.big_e.BIG_TOP

        def f_if(self, i):
            return i

        def f_bytes(self, b):
            return b + b"!"

    impl = Impl()
    a = t.svc2_py_adapter(impl)
    p = [rt.rec_to_sv(t.derived_rec(b=1)), rt.rec_to_sv(t.derived_rec(b=2))]
    out = a.f_list(p)
    assert [x[1] for x in out] == [2, 1]
    assert a.f_enum(7) == (1 << 64) - 1
    assert a.f_bytes([104]) == [104, 33]
    # An adapter passed back in is unwrapped to the implementation; the
    # result is wrapped again
    back = a.f_if(a)
    assert isinstance(back, t.svc2_py_adapter) and back._impl is impl


def _u(*defs):
    u = TypeUniverse()
    for d in defs:
        u.add(d)
    return u


@pytest.mark.parametrize("u,msg", [
    (lambda: _u(RecordDef("pkt"), RecordDef("pkt_if")), "clashes with a name generated for 'pkt'"),
    (lambda: _u(InterfaceDef("i"), RecordDef("i_py_proxy")), "clashes"),
    (lambda: _u(RecordDef("u8")), "type spelling"),
    (lambda: _u(EnumDef("a", 2, [("X", 0)]), EnumDef("b", 2, [("X", 1)])), "clashes with a value of enum a"),
    (lambda: _u(EnumDef("a", 2, [("b", 0)]), RecordDef("b")), "clashes with another name"),
])
def test_name_clashes(u, msg):
    with pytest.raises(IrError, match=msg):
        gen_sv(u(), "p", "m", "s")
    with pytest.raises(IrError, match=msg):
        gen_py(u(), "s")


def test_py_ref_and_sv_ref():
    u = _u(EnumDef("e", 2, [("A", 0)], py_ref="user.mod.E", sv_ref="user_pkg::e_t"),
           RecordDef("r", [FieldDef("x", EnumRef("e"))], py_ref="user.mod.r", sv_ref="user_pkg::r_c"),
           InterfaceDef("i", [MethodDef("m", params=[ParamDef("p", RecordRef("r"))])],
                        py_ref="user.mod.I", sv_ref="user_pkg::i_c"))
    py = gen_py(u, "s")
    assert "from user.mod import E as e" in py
    assert "from user.mod import r\n" in py
    assert "from user.mod import I as i" in py
    assert "class r(" not in py and "class i(" not in py and "class e(" not in py
    assert "class r_sv_ref(_rt.SvRef)" in py and "class i_sv_proxy" in py
    sv = gen_sv(u, "p", "m", "s")
    assert "typedef enum" not in sv
    assert "class r implements" not in sv
    assert "interface class i;" not in sv
    assert "class r_sv_wrap implements r_if;" in sv
    assert "user_pkg::r_c m_obj;" in sv
    assert "function automatic user_pkg::r_c r_copy(user_pkg::r_c v);" in sv
    assert "class i_py_proxy extends pyhdl_if::PyRef implements user_pkg::i_c;" in sv
    assert "user_pkg::e_t'(" in sv


def test_bad_py_ref():
    u = _u(RecordDef("r", py_ref="nomodule"))
    with pytest.raises(IrError, match="must be module.Class"):
        gen_py(u, "s")


@pytest.mark.parametrize("spec,pkg,mod,outdir", goldens.GOLDENS)
def test_py_type_checks(spec, pkg, mod, outdir):
    pytest.importorskip("mypy")
    env = dict(os.environ)
    env["MYPYPATH"] = os.path.join(root_dir, "src")
    res = subprocess.run(
        [sys.executable, "-m", "mypy", "--ignore-missing-imports",
         "--follow-imports=silent", "--no-incremental", mod + ".py"],
        cwd=os.path.join(root_dir, outdir), env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert res.returncode == 0, res.stdout
