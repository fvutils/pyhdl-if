"""The block team's IPv4 coverage model (pyvsc).

It samples anything with IPv4 header attributes (ttl, ihl, protocol, flags,
dst): an object from their cocotb bench, or the Python mirror of the UVM
env's pkt_item. Nothing here knows about SystemVerilog.
"""
import vsc

# The routing table under test: (prefix, length), in route order
ROUTES = [(0x0A000000, 8), (0x0A010000, 16), (0x0A010200, 24), (0xC0A80000, 16)]
NO_ROUTE = len(ROUTES)


def route_of(dst):
    """Index of the longest matching route, or NO_ROUTE."""
    best, idx = -1, NO_ROUTE
    for i, (prefix, plen) in enumerate(ROUTES):
        mask = (0xFFFFFFFF << (32 - plen)) & 0xFFFFFFFF
        if (dst & mask) == (prefix & mask) and plen > best:
            best, idx = plen, i
    return idx


@vsc.covergroup
class ipv4_cg(object):

    def __init__(self):
        self.with_sample(dict(
            ttl=vsc.uint8_t(), ihl=vsc.uint8_t(), proto=vsc.uint8_t(),
            df=vsc.bit_t(), route=vsc.uint8_t()))

        self.cp_ttl = vsc.coverpoint(self.ttl, bins=dict(
            expired=vsc.bin(0, 1), last_hop=vsc.bin(2), low=vsc.bin([3, 63]),
            typical=vsc.bin(64), high=vsc.bin([65, 254]), max=vsc.bin(255)))
        self.cp_ihl = vsc.coverpoint(self.ihl, bins=dict(
            malformed=vsc.bin([0, 4]), no_options=vsc.bin(5),
            options=vsc.bin([6, 14]), max_options=vsc.bin(15)))
        self.cp_proto = vsc.coverpoint(self.proto, bins=dict(
            icmp=vsc.bin(1), tcp=vsc.bin(6), udp=vsc.bin(17)))
        self.cp_df = vsc.coverpoint(self.df, bins=dict(
            may_fragment=vsc.bin(0), dont_fragment=vsc.bin(1)))
        self.cp_route = vsc.coverpoint(self.route, bins=dict(
            net10_8=vsc.bin(0), net10_1_16=vsc.bin(1), net10_1_2_24=vsc.bin(2),
            net192_168_16=vsc.bin(3), none=vsc.bin(NO_ROUTE)))
        self.cx_route_proto = vsc.cross([self.cp_route, self.cp_proto])


class Ipv4Coverage(object):

    def __init__(self):
        self.cg = ipv4_cg()
        self.n_sampled = 0

    def sample(self, pkt):
        self.cg.sample(pkt.ttl, pkt.ihl, pkt.protocol, (pkt.flags >> 1) & 1,
                       route_of(pkt.dst))
        self.n_sampled += 1

    def report(self):
        """Print the report, write a UCIS XML database; return coverage %."""
        print(vsc.get_coverage_report(details=True), flush=True)
        vsc.write_coverage_db("ipv4_cov.xml")
        return self.cg.get_coverage()
