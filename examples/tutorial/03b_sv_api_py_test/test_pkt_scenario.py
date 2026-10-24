"""The scenario on its own: no simulator, seconds to run."""
from pkt_scenario import NO_ROUTE, ROUTES, PacketGen


def test_same_seed_same_packets():
    a, b = PacketGen(42), PacketGen(42)
    assert [a.next() for _ in range(20)] == [b.next() for _ in range(20)]
    assert PacketGen(43).next() != PacketGen(42).next()


def test_mix():
    gen = PacketGen(1)
    pkts = [gen.next() for _ in range(300)]
    for p in pkts:
        assert 5 <= p["ihl"] <= 15 and len(p["options"]) == 4 * (p["ihl"] - 5)
        assert p["protocol"] in (1, 6, 17)
        assert len(p["payload"]) <= 64
    # Every route, and some unroutable packets, show up
    hit = set()
    for p in pkts:
        for i, (prefix, plen) in enumerate(ROUTES + [NO_ROUTE]):
            if p["dst"] >> (32 - plen) == prefix >> (32 - plen):
                hit.add(i)
    assert hit == set(range(len(ROUTES) + 1))
    assert any(p["ttl"] <= 1 for p in pkts)
