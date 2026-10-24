"""The library's implementation: scapy does the protocol work."""
import random

from scapy.compat import raw
from scapy.layers.inet import IP, IPOption_NOP, IPOption_Router_Alert, IPOption_RR
from scapy.packet import Raw, fuzz
from scapy.utils import PcapWriter as _ScapyPcapWriter, RawPcapReader

LINKTYPE_IPV4 = 228     # raw IPv4, no link-layer header

PROTOCOLS = {"icmp": 1, "tcp": 6, "udp": 17}
OPTIONS = {"nop": IPOption_NOP, "rr": IPOption_RR, "router_alert": IPOption_Router_Alert}
OPTION_NAMES = {0: "EOL", 1: "NOP", 7: "RR", 20: "RA"}


def _ones_sum(hdr):
    if len(hdr) % 2:
        hdr += b"\x00"
    s = sum(int.from_bytes(hdr[i:i + 2], "big") for i in range(0, len(hdr), 2))
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return s


class Ipv4PktImpl(object):

    def __init__(self, ip=None, data=None):
        self._ip = ip if ip is not None else IP()
        self._data = data       # the bytes as given, for an unpacked packet
        self._corrupt = False

    def _edit(self):
        # A change: let scapy recompute lengths and the checksum
        self._data = None
        self._ip.len = None
        self._ip.ihl = None
        self._ip.chksum = None

    def set_src(self, addr):
        self._ip.src = addr
        self._edit()

    def set_dst(self, addr):
        self._ip.dst = addr
        self._edit()

    def get_dst(self):
        return self._ip.dst

    def set_ttl(self, ttl):
        self._ip.ttl = ttl
        self._edit()

    def get_ttl(self):
        return self._ip.ttl

    def set_protocol(self, name):
        self._ip.proto = PROTOCOLS[name]
        self._edit()

    def add_option(self, name):
        self._ip.options = list(self._ip.options) + [OPTIONS[name]()]
        self._edit()

    def set_payload(self, data):
        self._ip.remove_payload()
        if data:
            self._ip.add_payload(Raw(data))
        self._edit()

    def corrupt_checksum(self):
        self._corrupt = True

    def pack(self):
        if self._data is not None:
            return self._data
        data = bytearray(raw(self._ip))
        if self._corrupt:
            data[10] ^= 0x01
        return bytes(data)

    def checksum_ok(self):
        data = self.pack()
        ihl = (data[0] & 0xF) * 4
        return ihl >= 20 and len(data) >= ihl and _ones_sum(data[:ihl]) == 0xFFFF

    def summary(self):
        data = self.pack()
        ip = IP(data)
        opts = []
        for o in ip.options:
            opts.append(OPTION_NAMES.get(o.option, str(o.option)))
        return "%s > %s ttl=%d proto=%s%s len=%d chksum=%s" % (
            ip.src, ip.dst, ip.ttl,
            {v: k for k, v in PROTOCOLS.items()}.get(ip.proto, str(ip.proto)),
            (" opts=[%s]" % ",".join(o for o in opts if o != "EOL")) if opts else "",
            len(data), "OK" if self.checksum_ok() else "BAD")


class Ipv4MutatorImpl(object):

    MUTATIONS = ["bad_checksum", "ttl_expired", "short_ihl", "ihl_past_end", "fuzz"]

    def __init__(self, seed):
        self._rand = random.Random(seed)
        self._last = ""

    def mutate(self, data):
        m = self._rand.choice(self.MUTATIONS)
        self._last = m
        ip = IP(data)
        if m == "bad_checksum":
            p = Ipv4PktImpl(ip, data)
            p._data = None
            p.corrupt_checksum()
            return p
        if m == "ttl_expired":
            ip.ttl = self._rand.choice([0, 1])
            ip.chksum = None
            return Ipv4PktImpl(ip)
        if m == "short_ihl":
            out = bytearray(data[:20] + data[(ip.ihl * 4):])
            out[0] = 0x40 | self._rand.randint(0, 4)
            return Ipv4PktImpl(data=bytes(_fix_cksum(out, 20)))
        if m == "ihl_past_end":
            out = bytearray(data[:20])
            out[0] = 0x40 | 15
            return Ipv4PktImpl(data=bytes(_fix_cksum(out, 20)))
        # Random header fields, scapy's fuzz(), keeping the addresses.
        # fuzz() draws from the global random; seed it from ours.
        random.seed(self._rand.getrandbits(32))
        f = fuzz(IP(src=ip.src, dst=ip.dst))
        return Ipv4PktImpl(data=raw(f)[:200])

    def last_mutation(self):
        return self._last


def _fix_cksum(hdr, n):
    """Correct checksum over the first n bytes, so only the mutation is wrong."""
    hdr[10:12] = b"\x00\x00"
    hdr[10:12] = (~_ones_sum(bytes(hdr[:n])) & 0xFFFF).to_bytes(2, "big")
    return hdr


class PcapWriterImpl(object):

    def __init__(self, path):
        self._w = _ScapyPcapWriter(path, linktype=LINKTYPE_IPV4, sync=True)

    def write(self, data, time_ps):
        pkt = Raw(bytes(data))
        pkt.time = time_ps / 1e12
        self._w.write(pkt)

    def close(self):
        self._w.close()


class PcapReaderImpl(object):

    def __init__(self, path):
        self._r = RawPcapReader(path)
        self._it = iter(self._r)

    def read(self):
        rec = next(self._it, None) if self._r is not None else None
        if rec is None:
            return b""
        return bytes(rec[0])

    def close(self):
        if self._r is not None:
            self._r.close()
            self._r = None


class Ipv4LibImpl(object):

    def new_pkt(self):
        return Ipv4PktImpl()

    def unpack(self, data):
        return Ipv4PktImpl(IP(bytes(data)), bytes(data))

    def new_mutator(self, seed):
        return Ipv4MutatorImpl(seed)

    def pcap_writer(self, path):
        return PcapWriterImpl(path)

    def pcap_reader(self, path):
        return PcapReaderImpl(path)
