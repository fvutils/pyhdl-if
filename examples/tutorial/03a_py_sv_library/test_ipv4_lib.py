"""The library's Python side on its own: no simulator, seconds to run."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ipv4_lib"))
from ipv4_lib_impl import Ipv4LibImpl  # noqa: E402

lib = Ipv4LibImpl()


def build():
    p = lib.new_pkt()
    p.set_src("172.16.0.1")
    p.set_dst("10.1.2.3")
    p.set_ttl(9)
    p.set_protocol("tcp")
    p.add_option("rr")
    p.set_payload(b"\x01\x02\x03")
    return p


def test_build_pack_unpack():
    p = build()
    data = p.pack()
    assert data[0] == 0x40 | (len(data) - 3) // 4    # header = all but the payload
    assert p.checksum_ok()
    q = lib.unpack(data)
    assert q.pack() == data
    assert (q.get_dst(), q.get_ttl()) == ("10.1.2.3", 9)
    assert q.summary() == "172.16.0.1 > 10.1.2.3 ttl=9 proto=tcp opts=[RR] len=%d chksum=OK" % len(data)


def test_corrupt_checksum():
    p = build()
    p.corrupt_checksum()
    assert not p.checksum_ok()
    assert p.summary().endswith("chksum=BAD")


def test_mutator_is_reproducible_and_covers_all_mutations():
    data = build().pack()
    runs = []
    for _ in range(2):
        m = lib.new_mutator(7)
        runs.append([(m.mutate(data).pack(), m.last_mutation()) for _ in range(40)])
    assert runs[0] == runs[1]
    assert {name for _, name in runs[0]} == set(lib.new_mutator(0).MUTATIONS)


def test_pcap_round_trip(tmp_path):
    path = str(tmp_path / "x.pcap")
    pkts = [build().pack(), lib.new_mutator(1).mutate(build().pack()).pack()]
    w = lib.pcap_writer(path)
    for i, d in enumerate(pkts):
        w.write(d, i * 10**6)
    w.close()
    r = lib.pcap_reader(path)
    got = []
    while (d := r.read()):
        got.append(d)
    r.close()
    assert got == pkts
