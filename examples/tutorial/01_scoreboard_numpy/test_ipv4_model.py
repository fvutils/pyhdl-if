"""The reference model's own tests: no simulator, seconds to run."""
import pytest
import ipv4_model as m

ROUTES = [(0x0A000000, 8, 0), (0x0A010000, 16, 1), (0x0A010200, 24, 2), (0xC0A80000, 16, 3)]


def header(dst, ttl=64, ihl=5, bad_cksum=False):
    """A 20-byte (or longer, with NOP options) IPv4 header."""
    h = bytearray(ihl * 4)
    h[0] = 0x40 | ihl
    h[2:4] = (ihl * 4).to_bytes(2, "big")
    h[8], h[9] = ttl, 17
    h[12:16] = bytes([10, 0, 0, 1])
    h[16:20] = dst.to_bytes(4, "big")
    for i in range(20, ihl * 4):
        h[i] = 1
    cks = ~m.ones_sum(bytes(h)) & 0xFFFF
    h[10:12] = (cks ^ (0x0100 if bad_cksum else 0)).to_bytes(2, "big")
    return list(h)


@pytest.fixture(autouse=True)
def routes():
    m.set_routes(ROUTES)


def test_forward_longest_prefix_and_checksum():
    fate, port, cks = m.predict(header(0x0A010203, ttl=64), 20)
    assert (fate, port) == (m.FWD, 2)
    # A header carrying the new checksum sums to 0xFFFF
    h = bytearray(header(0x0A010203, ttl=63))
    h[10:12] = cks.to_bytes(2, "big")
    assert m.ones_sum(bytes(h)) == 0xFFFF


@pytest.mark.parametrize("hdr,plen,fate", [
    (header(0x0A000001, bad_cksum=True), 20, m.BAD_CKSUM),
    (header(0x0A000001, ttl=1), 20, m.TTL),
    (header(0x08080808), 20, m.NO_ROUTE),
    (header(0x0A000001, ihl=6), 20, m.BAD_HDR),     # header longer than packet
])
def test_drops(hdr, plen, fate):
    assert m.predict(hdr, plen)[0] == fate
