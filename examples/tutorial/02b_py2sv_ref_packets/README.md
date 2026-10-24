# 2b. Python → SV: reference packets into a directed SV sequence

**Have:** conformance packets as JSON (`ref_pkts.json`), validated by the
protocol team's pydantic model (`ref_schema.py`). Each one says what the
forwarder should do with it.

**Want:** to replay them from an SV sequence, without translating them into
SV by hand (a parser, or a generated `.svh` of constants) and keeping that
copy in sync.

**Do:**

1. Declare the *interchange* type in Python (`ref_xchg.py`): a flat
   dataclass with sized fields, and a `Protocol` the sequence pulls from:

   ```python
   @dc.dataclass
   class RefPkt:
       name: str = ""
       src: u32 = 0
       dst: u32 = 0
       ttl: u8 = 64
       ...
       expected: Fate = Fate.FORWARD

   class RefSource(Protocol):
       def get_next(self) -> Optional[RefPkt]: ...
   ```

2. Generate the SV side. The flow does it in the `ref-gen` task; by hand:

   ```bash
   pyhdl-if gen-from-py -m ref_xchg --sv-out ref_xchg_pkg.sv --py-out ref_xchg_api.py
   ```

3. Write the adapter from the data model to the interchange type
   (`to_xchg()` in `ref_source.py`) and a source that loads, validates and
   converts the JSON.

4. In SV (`ref_test_pkg.sv`), pull the packets and turn each one into a
   `pkt_item`:

   ```systemverilog
   src = ref_xchg_pkg::RefSource_from_py(obj.borrow());
   while ((r = src.get_next()) != null) begin
       ...
       req.dst = r.dst;
   ```

   The sequence also checks that the scoreboard predicts the fate the
   reference data expects, so a disagreement between the protocol team and
   the env shows up as a `UVM_ERROR`.

**Shows:** Python is the source of truth for the type; SV gets a generated
one. The teaching point: *your Python data model (pydantic) is not your
interchange type.* Addresses as strings, hex payloads and validators stay in
Python; a small adapter (`to_xchg`) bridges the two. The generator also
protects the SV side: naming a field `expect`, an SV keyword, is an error at
generation time.

## Run

```bash
make run                    # SIM=vlt by default
pytest test_ref_source.py   # schema, data and adapter, no simulator
```
