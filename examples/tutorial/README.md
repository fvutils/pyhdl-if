# Three Ways to Use Python in Your UVM Testbench

Examples for the tutorial session. Each one starts from the same DUT and
UVM env and adds Python in one way. Each runs on its own.

| Example | Have | Want | Mechanism |
|---|---|---|---|
| [00_base](00_base) | a UVM env | (the starting point, no Python) | |
| [01_scoreboard_numpy](01_scoreboard_numpy) | a UVM scoreboard | its reference model in numpy | call a Python function with plain values |
| [02a_sv2py_coverage](02a_sv2py_coverage) | `pkt_item` in SV | sample it in a pyvsc covergroup | SV record and interface class → generated Python mirror (`gen-from-sv`) |
| [02b_py2sv_ref_packets](02b_py2sv_ref_packets) | reference packets in JSON/pydantic | replay them from an SV sequence | Python record and Protocol → generated SV (`gen-from-py`) |
| [03a_py_sv_library](03a_py_sv_library) | scapy | an SV packet library; the consumer writes only SV | Python Protocols → generated SV interface classes, behind an SV facade |
| [03b_sv_api_py_test](03b_sv_api_py_test) | an SV API on the env | the test in Python (pyvsc) | SV interface class with tasks → generated Python proxy |

## The common base (`common/`)

- `rtl/ipv4_fwd.sv`: a minimal IPv4 forwarder. One byte-stream input port
  (valid/ready, sop/eop) carries raw IPv4 packets. It checks the header
  checksum (IHL 5-15, so options are covered), drops a packet with a bad
  checksum, TTL <= 1, a malformed header or no route, decrements TTL,
  updates the checksum, and forwards by longest-prefix match to one of 4
  output ports. Routes and counters are registers.
- `env/`: `ipv4_pkt_pkg` (the `pkt_item` transaction) and `ipv4_env_pkg`
  (agent, output monitors, register access, an SV scoreboard, random
  traffic, and the base test).
- `tb/`: interfaces and `tb_top`.
- `flow.yaml`: the dfm package `tutorial` that every example imports.

## Running

Install `common/requirements.txt` into the Python that the simulator will
use (or use the pyhdl-if development environment), and put Verilator 5.04x
or later on `PATH`. Then, in an example directory:

```bash
make run              # SIM=vlt, mti, vcs or xcm
pytest                # that example's Python on its own, no simulator
```

`make run` runs `dfm run sim-run` and prints PASS when the UVM test reports
`TEST PASSED`. The sim log is `rundir/<package>.sim-run/sim.log`.
