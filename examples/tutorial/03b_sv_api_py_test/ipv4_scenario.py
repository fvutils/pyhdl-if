"""The test, in Python: the pkt_scenario traffic mix, run through the env's
SV API (ipv4_env_api). Every api call is an SV task or function."""
from api_gen_api import pkt_fate_e, pkt_item
from pkt_scenario import NO_ROUTE, PacketGen


async def burst(api, gen, n):
    for _ in range(n):
        await api.send(pkt_item(**gen.next()))
    await api.wait_idle()


async def run(api):
    # The SV seed picks the scenario's seed, so one seed reproduces both
    gen = PacketGen(api.get_seed())

    # With the routing table the base test programmed
    await burst(api, gen, 30)

    # Move 192.168/16 from port 3 to port 1, and add 8.8.8/24 -> port 3
    await api.set_route(3, 0xC0A80000, 16, 1)
    await api.set_route(4, NO_ROUTE[0], NO_ROUTE[1], 3)
    await burst(api, gen, 30)

    fwd = [await api.get_fwd_count(p) for p in range(4)]
    drops = {f.name: await api.get_drop_count(f) for f in (
        pkt_fate_e.FATE_BAD_HDR, pkt_fate_e.FATE_BAD_CKSUM,
        pkt_fate_e.FATE_TTL, pkt_fate_e.FATE_NO_ROUTE)}
    print("[py] forwarded per port %s; dropped %s" % (fwd, drops), flush=True)
    assert sum(fwd) + sum(drops.values()) == 60, "packets went missing"
