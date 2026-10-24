# 1. Call Python as a library: a numpy scoreboard model

**Have:** a UVM scoreboard (`../common/env/ipv4_fwd_scoreboard.svh`) whose
reference model, `predict()`, is written in SV.

**Want:** the reference model in Python. It's a few lines of numpy
(`ipv4_model.py`), where the alternative is a DPI-C model that someone has to
write, build and maintain:

```python
def ones_sum(hdr):
    s = int(np.frombuffer(hdr, dtype=">u2").sum(dtype=np.uint64))
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return s
```

**Do:** override `predict()` in a scoreboard subclass (`numpy_sb_pkg.sv`)
that imports the module once and calls its function for every packet:

```systemverilog
ret = model.call_attr("predict", py_tuple::mk_init('{
    py_from_bytes(p.header()), py_from_int(p.pack().size())}));
r = py_tuple::mk(ret);
fate = pkt_fate_e'(r.get_item(0).as_int());
```

`numpy_test` swaps it in with a UVM factory override; nothing else in the env
changes.

**Shows:** a stateless call with plain values (ints and a list of bytes),
with no object lifetime. This is the simplest case and the baseline for
sections 2 and 3, where generated code does the marshaling.

If `predict()` raises, the traceback is printed in the sim log and the
scoreboard reports a `UVM_ERROR`, so the test fails.

## Run

```bash
make run                    # SIM=vlt by default
pytest test_ipv4_model.py   # the model alone, no simulator
```
