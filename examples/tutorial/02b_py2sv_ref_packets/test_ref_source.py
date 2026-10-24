"""The reference data and the adapter: no simulator, seconds to run."""
import pydantic
import pytest
from ref_schema import RefPacket
from ref_source import open_source, to_xchg
from ref_xchg import Fate


def test_suite_loads_and_converts():
    src = open_source()
    pkts = []
    while (p := src.get_next()) is not None:
        pkts.append(p)
    assert len(pkts) == 13
    rr = next(p for p in pkts if p.name == "record-route")
    assert rr.dst == 0x0A010203
    assert rr.options == bytes.fromhex("0707040000000000")
    assert rr.expected == Fate.FORWARD


def test_adapter():
    p = RefPacket(name="x", src="10.0.0.1", dst="192.168.0.9", protocol="tcp",
                  payload="beef", expect="no_route")
    x = to_xchg(p)
    assert (x.src, x.dst, x.protocol, x.payload, x.ihl, x.expected) == \
        (0x0A000001, 0xC0A80009, 6, b"\xbe\xef", 0, Fate.NO_ROUTE)


@pytest.mark.parametrize("bad", [
    dict(ttl=256),
    dict(options="0101"),          # not a multiple of 4 bytes
    dict(payload="xyz"),           # not hex
    dict(dst="10.0.0.256"),
])
def test_schema_rejects(bad):
    fields = dict(name="x", src="10.0.0.1", dst="10.0.0.2", expect="forward")
    fields.update(bad)
    with pytest.raises(pydantic.ValidationError):
        RefPacket(**fields)
