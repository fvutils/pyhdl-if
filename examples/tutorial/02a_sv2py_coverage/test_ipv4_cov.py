"""The coverage model's own tests: no simulator, seconds to run."""
from types import SimpleNamespace
from ipv4_cov import Ipv4Coverage, route_of, NO_ROUTE


def pkt(dst, ttl=64, ihl=5, protocol=6, flags=0):
    return SimpleNamespace(dst=dst, ttl=ttl, ihl=ihl, protocol=protocol, flags=flags)


def test_route_of_longest_prefix():
    assert route_of(0x0A090909) == 0          # 10.9.9.9    -> 10/8
    assert route_of(0x0A010909) == 1          # 10.1.9.9    -> 10.1/16
    assert route_of(0x0A010209) == 2          # 10.1.2.9    -> 10.1.2/24
    assert route_of(0xC0A80101) == 3          # 192.168.1.1 -> 192.168/16
    assert route_of(0x08080808) == NO_ROUTE   # 8.8.8.8


def test_every_route_and_protocol_reaches_full_cross():
    cov = Ipv4Coverage()
    for dst in (0x0A090909, 0x0A010909, 0x0A010209, 0xC0A80101, 0x08080808):
        for proto in (1, 6, 17):
            cov.sample(pkt(dst, protocol=proto))
    assert cov.n_sampled == 15
    assert cov.cg.cx_route_proto.get_coverage() == 100.0
    assert cov.cg.cp_ttl.get_coverage() < 100.0   # only ttl=64 was sampled
