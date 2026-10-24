"""SV front end: SV source -> IR (needs pyslang)."""
import os
import shutil
import subprocess
import pytest

pytest.importorskip("pyslang")

from hdl_if.gen.ir import (
    ScalarT, BoolT, RealT, StrT, BytesT, EnumRef, RecordRef, ListT, IfRef, IrError)
from hdl_if.gen.front.sv import SvOptions, universe_from_sv
from hdl_if.gen.sv import gen_sv
from hdl_if.gen.py import gen_py

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sv")
SRC = [os.path.join(data_dir, "uvm_stub.sv"), os.path.join(data_dir, "fe_pkg.sv")]
GOOD = ["fe_pkg::pkt_item", "fe_pkg::pkt_svc", "fe_pkg::sign_e"]


def _u(**kw):
    kw.setdefault("include", GOOD)
    u, w = universe_from_sv(SRC, SvOptions(**kw))
    return u, w


def test_records_and_types():
    u, w = _u()
    assert w == []
    pkt = u.record("pkt_item")
    assert pkt.sv_ref == "fe_pkg::pkt_item"
    # UVM bases are stopped at; user bases become records
    assert pkt.base == "mid_item" and u.record("mid_item").base == "base_item"
    assert u.record("base_item").base is None
    f = {x.name: x for x in pkt.fields}
    assert list(f.keys()) == ["ttl", "addr", "s12", "tag", "data", "udata", "mac", "names",
                              "nums", "hdrs", "kind", "sgn", "flag", "r", "sr", "h"]
    assert f["ttl"].type == ScalarT(8, False) and f["ttl"].sv_type is None
    assert f["addr"].type == ScalarT(32, False)
    assert f["s12"].type == ScalarT(12, True)
    assert f["tag"].type == ScalarT(96, False)
    assert f["data"].type == BytesT() and f["data"].sv_type == "byte %s[$]"
    assert f["udata"].type == BytesT() and f["udata"].sv_type == "byte unsigned %s[]"
    assert f["mac"].type == BytesT() and f["mac"].sv_type == "bit[7:0] %s[0:5]"
    assert f["names"].type == ListT(StrT())
    assert f["nums"].type == ListT(ScalarT(32, True))
    assert f["hdrs"].type == ListT(RecordRef("hdr_c")) and f["hdrs"].sv_type == "fe_pkg::hdr_c %s[$]"
    assert f["kind"].type == EnumRef("proto_e")
    assert f["flag"].type == BoolT()
    assert f["r"].type == RealT(64) and f["sr"].type == RealT(32)
    assert f["h"].type == RecordRef("hdr_c")
    e = u.enum("proto_e")
    assert e.width == 8 and not e.signed and e.values == [("P_ICMP", 1), ("P_TCP", 6), ("P_UDP", 17)]
    s = u.enum("sign_e")
    assert s.width == 32 and s.signed and s.values == [("S_NEG", -1), ("S_POS", 1)]


def test_interfaces():
    u, w = _u()
    svc = u.interface("pkt_svc")
    assert svc.sv_ref == "fe_pkg::pkt_svc"
    m = {x.name: x for x in svc.methods}
    assert sorted(m.keys()) == ["get_bytes", "ping", "send", "subscribe"]
    send = m["send"]
    assert send.is_task and send.rtype == ScalarT(32, False)
    assert send.sv_rtype == "int unsigned" and send.sv_ret_name == "n"
    assert [(p.name, p.type, p.sv_type) for p in send.params] == [
        ("p", RecordRef("pkt_item"), "fe_pkg::pkt_item %s")]
    gb = m["get_bytes"]
    assert gb.rtype == BytesT() and gb.sv_rtype == "fe_pkg::bytes_t"
    assert [(p.type, p.sv_type) for p in gb.params] == [
        (BytesT(), "byte unsigned %s[$]"), (ScalarT(16, False), "logic[15:0] %s")]
    assert m["subscribe"].params[0].type == IfRef("cb_if")
    assert u.interface("cb_if").sv_ref == "fe_pkg::cb_if"


def test_field_filters():
    u, _ = _u(fields="rand")
    assert [f.name for f in u.record("pkt_item").fields] == ["ttl", "addr"]
    u, _ = _u(field_exclude=["fe_pkg::pkt_item.h*", "fe_pkg::pkt_item.n*"])
    names = [f.name for f in u.record("pkt_item").fields]
    assert "h" not in names and "hdrs" not in names and "names" not in names
    assert "hdr_c" not in u
    u, _ = _u(field_include=["fe_pkg::pkt_item.ttl", "fe_pkg::*.id"])
    assert [f.name for f in u.record("pkt_item").fields] == ["ttl"]
    assert [f.name for f in u.record("base_item").fields] == ["id"]


def test_method_filters():
    u, _ = _u(method_exclude=["fe_pkg::pkt_svc.get_*", "fe_pkg::pkt_svc.ping"])
    assert [m.name for m in u.interface("pkt_svc").methods] == ["send", "subscribe"]


def test_base_walk():
    u, _ = _u(skip_base=["fe_pkg::mid_item"])
    assert u.record("pkt_item").base == "base_item" and "mid_item" not in u
    u, _ = _u(stop_at=["fe_pkg::mid_item", "uvm_pkg::*"])
    assert u.record("pkt_item").base is None and "base_item" not in u
    # Re-including UVM bases: uvm_sequence_item is virtual, so it can't be a record
    with pytest.raises(IrError, match="uvm_pkg::uvm_sequence_item is virtual"):
        _u(stop_at=[])


@pytest.mark.parametrize("root,msg", [
    ("fe_pkg::has_event", r"fe_pkg.sv:\d+: field fe_pkg::has_event.e: type event is not supported"),
    ("fe_pkg::has_assoc", "associative arrays are not supported"),
    ("fe_pkg::needs_args", "constructor argument 'x' has no default"),
    ("fe_pkg::abstract_c", "is virtual"),
    ("fe_pkg::bad_dir_if", "only input arguments"),
])
def test_errors(root, msg):
    with pytest.raises(IrError, match=msg):
        _u(include=[root])


def test_skip_unsupported():
    u, w = _u(include=["fe_pkg::has_event"], skip_unsupported=True)
    assert u.record("has_event").fields == []
    assert len(w) == 1 and "skipped field fe_pkg::has_event.e" in w[0]


def test_compile_errors(tmpdir):
    bad = tmpdir.join("bad.sv")
    bad.write("package p; class c; int x endclass endpackage\n")
    with pytest.raises(IrError, match="SV sources have errors"):
        universe_from_sv([str(bad)])


def test_generates():
    """The generated code for existing SV definitions has the expected shape."""
    u, _ = _u()
    sv = gen_sv(u, "fe_gen_pkg", "fe_gen_api", "fe_pkg.sv")
    assert "class pkt_item_sv_wrap implements pkt_item_if;" in sv
    assert "fe_pkg::pkt_item m_obj;" in sv
    assert "typedef byte __svt" in sv
    # The proxy implements the user's interface class with its exact types
    assert "class pkt_svc_py_proxy extends pyhdl_if::PyRef implements fe_pkg::pkt_svc;" in sv
    assert "virtual task send(output int unsigned n, input fe_pkg::pkt_item p);" in sv
    assert "virtual function fe_pkg::bytes_t get_bytes(byte unsigned d[$], logic[15:0] w);" in sv
    py = gen_py(u, "fe_pkg.sv")
    assert "class pkt_item(mid_item):" in py
    assert "async def send(self, p: pkt_item) -> u32:" in py


@pytest.mark.skipif(shutil.which("verilator") is None, reason="verilator not found")
def test_generated_lints(tmpdir):
    u, _ = _u()
    gen = tmpdir.join("fe_gen_pkg.sv")
    gen.write(gen_sv(u, "fe_gen_pkg", "fe_gen_api", "fe_pkg.sv"))
    import hdl_if
    dpi = os.path.join(hdl_if.share(), "dpi")
    res = subprocess.run(
        ["verilator", "--lint-only", "-Wno-fatal", "-Wno-WIDTH", "-Wno-lint",
         "-Wno-style", "-Wno-SHORTREAL", "-I" + dpi, os.path.join(dpi, "pyhdl_if.sv")]
        + SRC + [str(gen), "--top-module", "fe_gen_pkg", "--Mdir", str(tmpdir.join("obj"))],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert res.returncode == 0 and "%Error" not in res.stdout, res.stdout
