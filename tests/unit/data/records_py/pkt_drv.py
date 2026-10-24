"""Python side: builds reference packets and sends them to the SV sink."""
from pkt_model import RefPkt, Proto
import pkt_api


async def run(sink):
    assert isinstance(sink, pkt_api.PktSink_sv_proxy), type(sink)
    total = 0
    for i in range(10):
        p = RefPkt(src=0x0A000000 + i, dst=0xC0A80001, ttl=i + 1,
                   proto=Proto.TCP if i % 2 else Proto.UDP,
                   payload=bytes(range(i)), opts=[i, 0xFFFF])
        total += await sink.send(p)
    n = sink.count()
    ok = (n == 10 and total == sum(range(10)))
    print("[Py] sent %d, total %d" % (n, total), flush=True)
    return 1 if ok else 0
