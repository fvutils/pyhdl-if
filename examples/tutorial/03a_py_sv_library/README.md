# 3a. Python → SV: ship an SV library implemented in Python

**Have:** scapy, a mature, protocol-aware packet library, in Python.

**Want:** an SV packet library for the UVM team, where the consumer sees
only SystemVerilog (`import ipv4_lib::*;`). They don't learn pyhdl-if,
don't write Python, and don't need to know Python is underneath.

## The consumer (`lib_test_pkg.sv`)

All SV. A sequence builds packets with options, an error sequence makes
malformed variants, and a monitor logs a one-line summary of every packet
and writes `in.pcap` / `out.pcap` for Wireshark:

```systemverilog
ipv4_pkt p = new();
p.set_dst("10.1.2.200");
p.add_option("rr");
req.unpack(p.pack());
...
bad = mutator.mutate(good);
`uvm_info("err", $sformatf("%s %s", mutator.last_mutation(), bad.summary()), UVM_LOW)
```

```
[in_cap]  172.16.0.1 > 10.1.2.200 ttl=126 proto=icmp opts=[RR,NOP,RR] len=32 chksum=OK
[out_cap] port 2: 172.16.0.1 > 10.1.2.200 ttl=125 proto=icmp opts=[RR,NOP,RR] len=32 chksum=OK
```

## The library (`ipv4_lib/`), as its author ships it

| File | What it is |
|---|---|
| `ipv4_lib_if.py` | The API, declared as Python `Protocol`s: `Ipv4Lib` (the factory), `Ipv4Pkt`, `Ipv4Mutator`, `PcapWriter`, `PcapReader` |
| `ipv4_lib_impl.py` | The implementation, on scapy |
| `ipv4_lib.sv` | A thin hand-written SV facade, package `ipv4_lib`: UVM-friendly classes (`ipv4_pkt`, `ipv4_mutator`, `pcap_writer`, `pcap_reader`) over the generated interface classes |
| `requirements.txt` | The consumer installs it into the simulator's Python |

The author generates the SV interface classes (the flow's `lib-gen` task):

```bash
pyhdl-if gen-from-py -P ipv4_lib -m ipv4_lib_if \
    --sv-out ipv4_lib_gen.sv --py-out ipv4_lib_gen_api.py
```

Each facade object holds a handle to a Python object: an `ipv4_pkt` is a
scapy packet, and a `pcap_writer` is an open capture file. The factory's
methods return those handles (`Ipv4Lib.new_pkt() -> Ipv4Pkt`).

**Shows:** packaging and encapsulation. The generated SV classes are the
library's public interface, not an integration seam the consumer sees. It
also shows object lifetime and state, which section 1 didn't have (call
`free()` to release a packet early). It's the mirror image of 3b, where the
consumer writes Python and never touches SV.

## Run

```bash
make run                  # SIM=vlt by default
pytest test_ipv4_lib.py   # the library's Python side, no simulator
wireshark rundir/py_sv_lib.sim-run/in.pcap
```
