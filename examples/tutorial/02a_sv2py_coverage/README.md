# 2a. SV → Python: sample SV packets in a pyvsc covergroup

**Have:** `pkt_item extends uvm_sequence_item`, already in the UVM env
(`../common/env/ipv4_pkt_pkg.sv`).

**Want:** to sample it in the block team's Python coverage model
(`ipv4_cov.py`, pyvsc), which they wrote for their cocotb bench. The SoC env
reuses it instead of keeping a second SV copy that drifts.

**Do:**

1. Say what the env needs from a coverage model, as an SV interface class
   (`cov_if_pkg.sv`):

   ```systemverilog
   interface class pkt_cov_if;
       pure virtual function void sample(pkt_item p);
       pure virtual function real report();
   endclass
   ```

2. Generate the glue from the SV declarations. The flow does it in the
   `cov-gen` task; by hand:

   ```bash
   pyhdl-if gen-from-sv -I $UVM_HOME/src $UVM_HOME/src/uvm_pkg.sv \
       ../common/env/ipv4_pkt_pkg.sv cov_if_pkg.sv \
       -i 'ipv4_pkt_pkg::*' -i 'cov_if_pkg::*' \
       --sv-out cov_gen_pkg.sv --py-out cov_gen_api.py
   ```

   `cov_gen_api.py` has a typed Python mirror of `pkt_item` (a dataclass);
   `cov_gen_pkg.sv` has the SV side that copies a `pkt_item` into it.

3. Add a subscriber on the input monitor (`cov_test_pkg.sv`). It turns the
   Python `Ipv4Coverage` object into a `pkt_cov_if` handle once, then
   calls it for every packet:

   ```systemverilog
   cov = cov_gen_pkg::pkt_cov_if_from_py(model.borrow());
   ...
   function void write(pkt_item t);
       cov.sample(t);
   endfunction
   ```

`ipv4_cov.py` doesn't import anything generated: it samples any object with
`ttl`, `ihl`, `protocol`, `flags` and `dst`, so it still runs on the cocotb
bench.

**Shows:** SV stays the source of truth for the type. Python gets a
generated mirror, so nothing is kept in sync by hand.

## Run

```bash
make run              # SIM=vlt by default
pytest test_ipv4_cov.py   # the coverage model alone, no simulator
```

The sim log (`rundir/sv2py_cov.sim-run/sim.log`) ends with pyvsc's report.
Random traffic leaves holes (TTL 2 and 64, malformed IHL), which is the
next step: write a sequence for them. The UCIS XML database is
`rundir/sv2py_cov.sim-run/ipv4_cov.xml`.
