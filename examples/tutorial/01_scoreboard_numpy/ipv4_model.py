"""Reference model of the IPv4 forwarder, in numpy.

predict() takes plain values (the header bytes and the packet length) and
returns plain values, so the scoreboard calls it like any library function.
"""
import numpy as np

# Same order as pkt_fate_e in ipv4_pkt_pkg.sv
FWD, BAD_HDR, BAD_CKSUM, TTL, NO_ROUTE = range(5)

_routes = []


def set_routes(routes):
    """routes: (prefix, length, port) tuples."""
    global _routes
    _routes = [tuple(r) for r in routes]


def ones_sum(hdr):
    """One's-complement sum of 16-bit big-endian words, folded."""
    s = int(np.frombuffer(hdr, dtype=">u2").sum(dtype=np.uint64))
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return s


def lookup(dst):
    """Longest-prefix match: the output port, or -1."""
    best, port = -1, -1
    for prefix, plen, p in _routes:
        mask = (0xFFFFFFFF << (32 - plen)) & 0xFFFFFFFF
        if (dst & mask) == (prefix & mask) and plen > best:
            best, port = plen, p
    return port


def predict(header, pkt_len):
    """Returns (fate, port, checksum after the TTL decrement)."""
    hdr = bytes(header)
    version, ihl = hdr[0] >> 4, hdr[0] & 0xF
    if version != 4 or ihl < 5 or ihl * 4 > pkt_len:
        return (BAD_HDR, -1, 0)
    hdr = hdr[:ihl * 4]
    if ones_sum(hdr) != 0xFFFF:
        return (BAD_CKSUM, -1, 0)
    ttl = hdr[8]
    if ttl <= 1:
        return (TTL, -1, 0)
    port = lookup(int.from_bytes(hdr[16:20], "big"))
    if port < 0:
        return (NO_ROUTE, -1, 0)
    fwd = bytearray(hdr)
    fwd[8] = ttl - 1
    fwd[10:12] = b"\x00\x00"
    return (FWD, port, ~ones_sum(bytes(fwd)) & 0xFFFF)
