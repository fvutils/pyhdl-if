# 3b. SV → Python: drive an SV env API from a Python test

**Have:** an API on the UVM env for test writers, as an SV interface class
(`env_api_pkg.sv`), implemented by the env (`ipv4_env_api_impl` in
`py_test_pkg.sv`):

```systemverilog
interface class ipv4_env_api;
    pure virtual task send(pkt_item p);
    pure virtual task set_route(int idx, int unsigned prefix, int len, int port);
    pure virtual task wait_idle();
    pure virtual task get_fwd_count(output int unsigned count, input int port);
    pure virtual task get_drop_count(output int unsigned count, input pkt_fate_e reason);
    pure virtual function int unsigned get_seed();
endclass
```

**Want:** to write the test in Python, so the stimulus is consistent. The
traffic mix is a pyvsc scenario (`pkt_scenario.py`) that knows nothing
about the simulator, so the same scenario can run on the block-level cocotb
bench and in the UVM env. Tests are also something agents write well in
Python.

**Do:**

1. Generate the Python mirror of the API and of `pkt_item` (the flow's
   `api-gen` task):

   ```bash
   pyhdl-if gen-from-sv -I $UVM_HOME/src $UVM_HOME/src/uvm_pkg.sv \
       ../common/env/ipv4_pkt_pkg.sv env_api_pkg.sv \
       -i 'ipv4_pkt_pkg::*' -i 'env_api_pkg::*' \
       --sv-out api_gen_pkg.sv --py-out api_gen_api.py
   ```

2. Write the test (`ipv4_scenario.py`). Each call on `api` is an SV task,
   so it consumes simulation time and is awaited:

   ```python
   async def run(api):
       gen = PacketGen(api.get_seed())
       for _ in range(30):
           await api.send(pkt_item(**gen.next()))
       await api.wait_idle()
       await api.set_route(3, 0xC0A80000, 16, 1)
       ...
   ```

3. Start it from UVM: `py_test` hands the env's implementation to Python
   (`api_gen_pkg::ipv4_env_api_to_py(api)`) and runs `ipv4_scenario.run`
   as a task (`+PY_TEST=<module>` picks another test module).

**Reproducibility:** the Python seed comes from the SV seed
(`get_seed()` draws `$urandom`), so `+verilator+seed+N` reproduces both
sides.

**Failures land in UVM:** an exception or failed `assert` in the Python
test prints its traceback, becomes a `UVM_ERROR`, and the test reports
`TEST FAILED`. (`py_test` clears `pyhdl_if::pyhdl_if_rt_error_fatal` so
the run isn't ended on the spot.)

**Shows:** time-consuming (task) calls from Python into SV. SV is the source
of truth for the API, and Python gets a generated mirror. It's the mirror
image of 3a, where Python was the source and SV got the generated classes.

## Run

```bash
make run                      # SIM=vlt by default
pytest test_pkt_scenario.py   # the scenario alone, no simulator
```
