"""Loads and validates the reference packets, and hands them to SV."""
import os

from ref_schema import Expect, RefPacket, RefSuite
from ref_xchg import Fate, RefPkt

PROTOCOLS = {"icmp": 1, "tcp": 6, "udp": 17}
FATES = {
    Expect.forward: Fate.FORWARD,
    Expect.bad_header: Fate.BAD_HEADER,
    Expect.bad_checksum: Fate.BAD_CHECKSUM,
    Expect.ttl: Fate.TTL,
    Expect.no_route: Fate.NO_ROUTE,
}


def to_xchg(p: RefPacket) -> RefPkt:
    """The adapter between the data model and the interchange type."""
    return RefPkt(
        name=p.name,
        src=int(p.src),
        dst=int(p.dst),
        ttl=p.ttl,
        protocol=PROTOCOLS[p.protocol],
        dont_fragment=p.dont_fragment,
        options=bytes.fromhex(p.options),
        payload=bytes.fromhex(p.payload),
        ihl=p.ihl if p.ihl is not None else 0,
        corrupt_checksum=p.corrupt_checksum,
        expected=FATES[p.expect])


def load(path):
    with open(path) as fp:
        return RefSuite.model_validate_json(fp.read())


class JsonRefSource(object):
    """Implements ref_xchg.RefSource over a JSON suite."""

    def __init__(self, path):
        self._pkts = iter([to_xchg(p) for p in load(path).packets])

    def get_next(self):
        return next(self._pkts, None)


def open_source(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref_pkts.json")
    return JsonRefSource(path)
