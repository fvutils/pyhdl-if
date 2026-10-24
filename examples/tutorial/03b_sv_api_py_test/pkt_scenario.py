"""The traffic scenario: a pyvsc packet mix, independent of any bench.

PacketGen yields the header fields of each packet as a dict. The UVM test
(ipv4_scenario.py) turns them into pkt_items; a cocotb bench can turn the
same dicts into its own packets, so both benches see the same stimulus.
"""
import random

import vsc

ROUTES = [(0x0A000000, 8), (0x0A010000, 16), (0x0A010200, 24), (0xC0A80000, 16)]
NO_ROUTE = (0x08080800, 24)


@vsc.randobj
class PktScenario(object):
    """One packet of the mix: where it goes, its TTL, options and size."""

    def __init__(self):
        self.route = vsc.rand_uint8_t()         # 0-3: a route; 4: no route
        self.ttl = vsc.rand_uint8_t()
        self.opt_words = vsc.rand_uint8_t()
        self.payload_len = vsc.rand_uint8_t()
        self.protocol = vsc.rand_uint8_t()

    @vsc.constraint
    def c_mix(self):
        vsc.dist(self.route, [
            vsc.weight(0, 3), vsc.weight(1, 3), vsc.weight(2, 3), vsc.weight(3, 3),
            vsc.weight(4, 1)])
        vsc.dist(self.ttl, [
            vsc.weight(1, 1), vsc.weight(2, 1), vsc.weight(vsc.rng(3, 254), 8),
            vsc.weight(255, 1)])
        self.opt_words <= 10
        self.payload_len <= 64
        self.protocol.inside(vsc.rangelist(1, 6, 17))


class PacketGen(object):
    """Packets from one seed; the same seed gives the same packets."""

    def __init__(self, seed):
        self._rnd = random.Random(seed)
        self._s = PktScenario()
        self._s.set_randstate(vsc.RandState.mkFromSeed(seed))
        self._id = 0

    def next(self):
        s = self._s
        s.randomize()
        prefix, plen = ROUTES[s.route] if s.route < len(ROUTES) else NO_ROUTE
        opts = bytes([1] * (4 * s.opt_words - 1) + [0]) if s.opt_words else b""
        fields = dict(
            version=4, ihl=5 + s.opt_words, ttl=s.ttl, protocol=s.protocol,
            id=self._id, src=0xAC100001, dst=prefix | self._rnd.getrandbits(32 - plen),
            options=opts,
            payload=bytes(self._rnd.getrandbits(8) for _ in range(s.payload_len)))
        self._id += 1
        return fields
