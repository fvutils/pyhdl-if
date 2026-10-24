# Records and Interfaces: Implementation, Test, and Doc Plan

Design: `doc/design/neutral_api_and_records.md`.
Tutorial that depends on this: `session_plan.md`.

## Status

Last updated: 2026-10-24. All phases done (0-11). Open items are under
"Follow-ups" at the end; nothing is committed yet.

| Phase | Title | Status |
|---|---|---|
| 0 | Prep and fixes | done |
| 1 | Spike: hand-written generated code | done |
| 2 | Neutral IR and spec format | done |
| 3 | Runtime support (SV + Python) | done |
| 4 | Python back end | done |
| 5 | SV back end | done |
| 6 | `gen-from-py`, `gen-from-spec`, dfm tasks | done |
| 7 | Simulation test suite | done |
| 8 | `gen-from-sv` (pyslang) | done |
| 9 | Drift check and versioning in CI | done |
| 10 | Documentation | done |
| 11 | Map `@api`/`@imp`/`@exp` onto the IR (optional) | done |

Update this table and the phase's checklist as work lands. Log anything
surprising under "Notes" at the bottom.

## Decisions needed before Phase 2

These are not settled by the design doc. Status (2026-10-23): the proposals
below were adopted when implementation started; see "Resolution" under each.

1. **How a method parameter says "copy" vs. "reference" for a record.**
   Proposal:
   - SV: a parameter of the record class type (`pkt`) is a copy; a
     parameter of the accessor interface type (`pkt_if`) is a reference.
     This falls out of the SV types naturally.
   - Python: `p: pkt` is a copy; `p: hdl_if.Ref[pkt]` is a reference.
   - Return values follow the same rule.

   Resolution: adopted as proposed.
2. **Which simulators must pass.** CI runs Verilator (`vlt`) and Icarus
   (`ivl`). Icarus's class support is limited, and interface classes may not
   work at all. Proposal: Verilator is required; Icarus runs only the tests it
   can support, gated by a capability marker. Phase 1 settles what Icarus can
   do. Also confirm which OSS simulator the tutorial ships (Verilator or
   xezim) and add it to the matrix if it is not Verilator.

   Resolution: Icarus has no DPI-C, and everything here runs on pyhdl-if's
   DPI path, so Icarus is out (no marker needed: `available_sims_dpi()`
   never lists it). Verilator is required. xsim (Vivado 2023.1) fails today
   on every DPI test because it does not support `$stacktrace` in
   `pyhdl_if.sv`; that is pre-existing and not fixed here. xezim: see the
   Phase 1 notes.
3. **pyslang dependency.** pyslang 12.0.0 is in the dev/docs dep-sets but
   deliberately not in `default-ci`. Proposal: add a `pyhdl-if[sv]` extra in
   `setup.py` for consumers who run `gen-from-sv`, add pyslang to `default-ci`
   so its tests run in CI, and skip those tests when pyslang is missing.

   Resolution (revised in Phase 8): the `[sv]` extra and the skip were
   adopted, but pyslang is *not* added to `default-ci`: that dep-set builds
   wheels on images pyslang has no wheels for (see the comment on the
   `docs` dep-set in `ivpm.yaml`). It is listed in `default-dev` instead,
   which is what the CI test job installs (`ivpm update -a`), so the tests
   run in CI.
4. **Where new code lives.** Proposal: a new package `src/hdl_if/gen/` (IR,
   front ends, back ends), separate from `src/hdl_if/impl/call/`, so the new
   generators don't get tangled with `gen_sv_class.py`. New runtime code goes
   in `src/hdl_if/rt/` (Python) and `src/hdl_if/share/dpi/` (SV).

   Resolution: adopted as proposed.

## Phase 0: Prep and fixes

- [x] Fix the `@imp`/`@exp` docstrings in `src/hdl_if/decorators.py`
      (lines 29-34, 341-397), which describe the directions backwards.
- [x] Fix `src/hdl_if/__main__.py`: `ifc-gen-sv` has no `set_defaults`, and
      line 78 attaches `CmdIfcGenTypes` to the wrong parser, so
      `ifc-gen-types` has no handler.
- [x] Add a runtime API version, `PYHDL_IF_RT_API_VERSION`, in both the SV
      package and `hdl_if/__init__.py`, plus a single function on each side
      that checks a version. (Phase 9 hooks generated code up to it.)
- [x] Add `python_requires=">=3.9"` to `setup.py`, matching the CI wheel
      matrix. Generated Python must not use 3.10+ syntax (`X | Y` in
      evaluated hints, `dataclass(slots/kw_only)`).

Tests: an existing-suite regression run; a unit test that every subcommand
in `getparser()` has a `func`.

Done (2026-10-23):
- `@imp` = SystemVerilog implements, Python calls; `@exp` = the reverse.
  Fixed in `decorators.py` (module, `api`, `imp`, `exp` docstrings) and in
  the matching comments in `quickstart.rst` and `structs.rst`.
- `ifc-gen-sv` and `ifc-gen-types` now each have their handler.
- Version: `src/hdl_if/rt_api.py` (`PYHDL_IF_RT_API_VERSION`,
  `PYHDL_IF_RT_API_MIN_VERSION`, `check_rt_api_version()`, re-exported from
  `hdl_if`), and the same two parameters plus
  `pyhdl_if_check_rt_api_version()` in `pyhdl_if.sv`. Tests:
  `tests/unit/test_rt_api_version.py` (also checks the SV and Python numbers
  match), `tests/unit/test_cli_parser.py`.
- Regression: 26 tests were failing before any change. 13 were Verilator
  tests reading `out.output[0].basedir`, which dv-flow-libhdlsim no longer
  provides; they now use `sim_run.rundir` and pass. The other 13 are xsim
  (`$stacktrace`, see decision 2). Suite now: 13 failed (all xsim),
  110 passed.

## Phase 1: Spike with hand-written generated code

Goal: prove the runtime approach on real simulators before writing any
generator. Hand-write exactly what the generators will later emit, for:

- record `pkt` (int fields, a string, a `byte[$]`, an enum, a nested `hdr`
  record, a queue of ints),
- interface `I` with a function and a task, each taking and returning a
  record by copy and by reference.

Cases to run on Verilator and Icarus:

- [x] SV → Python copy and Python → SV copy, using generic runtime calls
      only (no new C).
- [x] SV holding a reference to a Python dataclass, through `pkt_py_ref`
      (`get_*`/`set_*`/`dispose`).
- [x] Python holding a reference to an SV `pkt`, through `pkt_sv_ref` and
      the SV adapter.
- [x] `I` implemented in SV and called from Python (function and task), and
      `I` implemented in Python and called from SV (function and task).
- [x] Record what Icarus cannot do (interface classes, parameterized
      adapters, queues of class handles); this answers decision 2.
      (Icarus has no DPI-C at all; see decision 2.)
- [x] Rough timings for copy vs. reference field access, to decide whether
      the copy transport should be field-by-field or packed.

Output: spike code in `tests/unit/data/spike_records/` (to become the golden
reference for Phases 4-5) and a short findings section under "Notes".

Done (2026-10-23): `tests/unit/test_spike_records.py` passes on Verilator
(30/30 repeated runs). The runtime pieces the spike needed were written in
their final locations (`src/hdl_if/rt/`, `share/dpi/pyhdl_if_rt.svh`), so
much of Phase 3 is done too. Findings are under "Notes: Phase 1".

## Phase 2: Neutral IR and spec format

Package: `src/hdl_if/gen/ir.py`.

- [x] Type references: `ScalarT(width, signed)`, `BoolT`, `RealT(width)`,
      `StrT`, `BytesT`, `EnumRef`, `RecordRef(by_ref: bool)`, `ListT(elem)`,
      `IfRef`.
- [x] Definitions: `EnumDef(name, width, values)`,
      `RecordDef(name, fields, bases)`, `FieldDef(name, type)`,
      `InterfaceDef(name, methods)`,
      `MethodDef(name, is_task, params, rtype)`; no direction anywhere.
- [x] `TypeUniverse`: holds every definition, resolves references, sorts by
      dependency order (for SV emission order), and rejects cycles of
      by-copy records.
- [x] Spec format v2: JSON load and dump of the IR, with a JSON Schema at
      `doc/pyhdl-if-v2.schema.json`. The v1 format and
      `api_def_from_json.py` stay unchanged.
- [x] Deterministic dump (sorted where order doesn't matter, stable where it
      does). Golden tests depend on this.

Tests (pure Python, `tests/unit/gen/`): building and resolving the IR;
dependency ordering; cycle detection; spec round trip
(load → dump → load is equal); schema validation of the golden specs.

Done (2026-10-23): `src/hdl_if/gen/ir.py`, `src/hdl_if/gen/spec.py`,
`doc/pyhdl-if-v2.schema.json`; tests in `tests/unit/gen/test_ir.py`; golden
specs `tests/unit/gen/data/spike.json` and `types.json`. Differences from
the list above:
- A record has at most one base (`RecordDef.base`), since SV classes
  extend one class.
- Every definition may carry `py_ref` (`module.Class`) and/or `sv_ref`
  (`pkg::name`): an existing definition to use instead of generating one.
  The SV and Python front ends set these.
- Type spellings in the spec: `u<N>`, `i<N>`, `bool`, `f32`, `f64`, `str`,
  `bytes`, `list<T>`, `ref<record>`, or a definition's name. The top-level
  key `"pyhdl-if-spec": 2` marks the format.
- Validation rejects names that are keywords in either language, start
  with `__`, or are reserved (`copy` for fields, `dispose` for methods,
  `retval` for parameters); `naming.check_names` also rejects names that
  clash with generated names (`pkt` and `pkt_if`), type spellings, or enum
  value names shared between enums (SV puts them all in one scope).
- `jsonschema` was added to the `default-dev` and `default-ci` dep-sets.

## Phase 3: Runtime support

Python (`src/hdl_if/rt/`):

- [x] Record copy entry points, `rec_from_sv(cls, payload)` and
      `rec_to_sv(obj)`, one per direction, so the transport can change later.
      Start with whatever the Phase 1 timings favor.
- [x] `SvRef` base: properties on generated subclasses call the SV adapter's
      `get_<f>`/`set_<f>`. `copy()` returns a dataclass snapshot.
      `__del__` releases the target and is safe at any time: it does nothing
      once the sim has ended or during interpreter shutdown, and it never
      raises.
- [x] `Ref[T]` marker type for Python signatures (decision 1).
- [x] `SvProxy` / `PyAdapter` bases for interfaces, building on
      `CallProxyDPI` and the endpoint's `newObj`/`connectObj`
      (`impl/call/hdl_call_endpoint_dpi.py:109-117`).

SV (`src/hdl_if/share/dpi/`):

- [x] **Release in the object registry.** `allocObjId`
      (`pyhdl_if_call_api.svh:119-138`) never frees a slot. Add
      `pyhdl_if_freeObjId(id)`, called when Python releases a reference to an
      SV object. Handle reuse safely: release goes through the id, so a stale
      id must not hit a new object (use a generation counter or never reuse
      ids within a call). Decide in the spike.
- [x] Base for SV-side references to Python objects: holds the `PyObject`,
      implements `dispose()` (Py_DecRef, then null), and reports use after
      dispose through the runtime's error path.
- [x] Helpers the generated copy code needs (building and reading the copy
      payload), so generated code stays small.
- [x] The version check from Phase 0, callable from generated packages.

Tests: Python-only unit tests for `SvRef`/`Ref`/finalizer behavior using a
fake endpoint; SV runtime pieces are covered by the Phase 7 sim tests.

Done (2026-10-23). Python: `src/hdl_if/rt/` (`types.py`: `Ref`, `u8`...,
`uint(N)`/`sint(N)`; `conv.py`: payload conversion; `obj.py`: `SvRef`,
`SvProxy`, `PyAdapter`, release queue, `invoke_py_t`). SV:
`src/hdl_if/share/dpi/pyhdl_if_rt.svh` (included in `pyhdl_if`): error
reporting, `PyRef` base class, `pyhdl_if_rt_*` helpers, `pyhdl_if_freeObjId`,
`pyhdl_if_rt_reapObjIds`, `pyhdl_if_rt_numObjs`. Tests:
`tests/unit/test_rt.py`. Notes:
- `SvProxy`/`PyAdapter` do not build on `CallProxyDPI`/`newObj`; see the
  Phase 1 notes (reference cycle). They use the endpoint directly.
- Stale ids: ids are released only when the one Python object holding them
  is collected, so no generation counter is needed.

## Phase 4: Python back end

`src/hdl_if/gen/py/`. Input is the IR; output is one module per package.

- [x] `IntEnum` per `EnumDef`.
- [x] `@dataclass` per `RecordDef` (Python 3.9-compatible), with nested
      records and `List[...]` fields using `field(default_factory=...)`.
- [x] `<rec>_sv_ref(SvRef)` with one property per field. Nested record
      fields return refs; list fields return copies (design rule).
- [x] `typing.Protocol` per `InterfaceDef` (`async def` for tasks).
- [x] `<I>_sv_proxy` (SV implements) and `<I>_py_adapter` (Python
      implements).
- [x] File header: source, generator version, runtime API version, and a
      "do not edit" notice. Output is deterministic.

Tests: golden-file tests against the Phase 1 spike's Python half (after the
spike code is cleaned up into the golden files); the generated module
imports and type-checks (`py_compile` plus `mypy` if available);
round-trip tests that run the generated dataclasses and refs against the
fake endpoint.

Done (2026-10-23): `src/hdl_if/gen/py/gen_py.py`. Tests in
`tests/unit/gen/test_backends.py` (goldens, order independence, Python 3.9
compile, mypy, fake-endpoint behavior, name clashes, `py_ref`/`sv_ref`).
Goldens: `tests/unit/data/spike_records/spike_api.py` and
`tests/unit/data/records_types/types_api.py`, regenerated by
`scripts/gen_records_goldens.py`; the spike's hand-written files were
replaced by generated ones, and the spike sim test still passes. Notes:
- The header records `GEN_VERSION` (`hdl_if/gen/naming.py`), the version
  of the generated code's shape, not the pyhdl-if version, so upgrading
  pyhdl-if alone does not make checked-in code stale.
- The module uses `from __future__ import annotations` (interfaces may
  refer to each other) and `list[T]` (valid at run time on 3.9).

## Phase 5: SV back end

`src/hdl_if/gen/sv/`. Output is one package `.sv` per spec.

- [x] `typedef enum` per `EnumDef`.
- [x] `class <rec> implements <rec>_if` with plain fields; its accessors read
      its own fields, and its `dispose()` does nothing.
- [x] `interface class <rec>_if` with `get_*`/`set_*`/`dispose()`.
- [x] `class <rec>_py_ref implements <rec>_if`.
- [x] `<rec>_to_py()` and `<rec>_from_py()` through the runtime entry points.
- [x] Adapter so Python can reach an SV `<rec>` by reference.
- [x] `interface class <I>` (with `dispose()`), `<I>_py_proxy implements
      <I>`, and `<I>_sv_adapter #(type T=<I>) implements pyhdl_if::ICallApi`.
- [x] Package header with versions, and a version check at package init.
      Output is deterministic.
- [x] Emission order follows the IR dependency order. Use forward `typedef
      class` where references create cycles.

Tests: golden files against the spike's SV half; a Verilator lint
(`--lint-only`) pass of every golden package; Icarus parse where decision 2
says it applies.

Done (2026-10-23): `src/hdl_if/gen/sv/gen_sv.py`; goldens
`tests/unit/data/spike_records/spike_pkg.sv` and
`tests/unit/data/records_types/types_pkg.sv`; Verilator lint test in
`test_backends.py`. Notes:
- `<I>_sv_adapter` holds an `<I>` (not `#(type T=<I>)`); see Phase 1.
- Lists use generated typedefs and helpers named `__list_<elem>`; ints
  wider than 64 bits use `__hex_<type>`. Generated locals and helpers all
  start with `__`, which user names cannot, so parameter names like
  `state` or `args` are safe.
- Verilator does not accept inherited methods as implementations of an
  interface class, so value classes implement every accessor (base fields
  too) and `PyRef` subclasses forward `dispose()` explicitly.
- `f32` maps to `shortreal`; Verilator warns and treats it as `real`.

## Phase 6: `gen-from-py`, `gen-from-spec`, dfm tasks

- [x] Python front end, `src/hdl_if/gen/front/py.py`:
  - `dataclasses.fields()` becomes a `RecordDef`, `IntEnum` an `EnumDef`,
    and `Protocol` an `InterfaceDef`, via `typing.get_type_hints`.
  - Hint mapping: ctypes ints and `int`/`bool`/`float`/`str`/`bytes`,
    `List[T]`, nested dataclass, `IntEnum`, `Ref[T]`, and Protocol-typed
    parameters (interface references).
  - Clear errors for unsupported hints, naming the class and field.
- [x] Spec front end: the v2 loader from Phase 2.
- [x] `gen-from-py` and `gen-from-spec` subcommands in `__main__.py` /
      `src/hdl_if/cmd/`. Shared options: `--sv-out`, `--py-out`, package
      name, `--check` (Phase 9). Module selection for `gen-from-py` follows
      `api-gen-sv` (modules, include/exclude, follow-deps).
- [x] dfm tasks `pyhdl-if.GenFromPy` and `pyhdl-if.GenFromSpec` in
      `src/hdl_if/dfm/flow.dv`, modeled on `APIGenSV` (`flow.dv:27`,
      `dfm/api_gen_sv.py`).

Tests: front-end unit tests (dataclass/Protocol/IntEnum → expected IR, error
cases); CLI tests that drive the commands with mock args, like
`test_api_gen_sv_json.py`; `cmdref.rst` picks up the new commands
automatically (sphinx-argparse).

Done (2026-10-23): `src/hdl_if/gen/front/py.py`, `src/hdl_if/cmd/cmd_gen.py`
(registered in `__main__.py`), `src/hdl_if/dfm/gen_from.py` + `flow.dv`.
Tests: `tests/unit/gen/test_front_py.py` (including reading back a
generated module and getting `spike.json` again), `test_cli_gen.py`, and
`tests/unit/test_records_dfm.py` (GenFromSpec feeding the spike sim).
Notes:
- Options: `--sv-out`, `--py-out`, `--spec-out` (dump the definitions as a
  v2 spec), `-p/--package` (default: SV file name), `--py-module` (default:
  Python file name), `--check` (done here rather than in Phase 9: nothing
  is written; exit 1 with a unified diff when a file differs or is
  missing). `gen-from-py` adds `-m`, `-i`, `-e` and `-P/--pythonpath`.
  Exit status 2 on a definition error, with the message on stderr.
- Include/exclude select the root classes; anything they refer to is always
  included, so there is no `--follow-deps`.
- Enum width from Python: the smallest of 8/16/32/64 bits that holds the
  values; a class attribute `__pyhdl_width__` overrides it.
- Protocol methods are those not starting with `_`, flattened across base
  protocols. A missing return annotation means no return value.
- The dfm tasks write `<pkgname>.sv` and `<pymodule>.py` (default
  `<pkgname>_api`) to the run directory and emit a `std.Env` prepending the
  run directory (and `pythonpath`) to `PYTHONPATH`; libhdlsim forwards it
  from SimImage to SimRun.

## Phase 7: Simulation test suite

Location: `tests/unit/test_records_*.py` and `tests/unit/test_ifc_*.py`,
data in `tests/unit/data/<test>/`. The pattern follows
`tests/unit/test_struct.py`: `pyhdl_dvflow` parameterized over
`available_sims_dpi()`, with the generation step as a dfm task.

- [x] Copy, both directions: every field type, nested records, empty and
      large queues and byte queues, enum values, strings with unusual
      characters.
- [x] Reference SV → Python: Python reads and writes through `pkt_sv_ref`
      and SV sees the changes; nested ref; `copy()` gives a snapshot that is
      unaffected by later writes.
- [x] Reference Python → SV: SV accessors through `pkt_py_ref`; `dispose()`
      releases (check the Python refcount or a weakref); use after dispose
      raises a runtime error.
- [x] Same SV code works on a local `pkt` and on a `pkt_py_ref` (through
      `pkt_if`).
- [x] Interface implemented in SV and called from Python, and implemented in
      Python and called from SV: functions and tasks, records by copy and by
      reference, interface-typed parameters (callbacks).
- [x] Lifetime: many references created and released in a loop; registry
      slots are reused and memory doesn't grow without bound.
- [x] Errors: a Python exception inside an adapter call surfaces in SV as a
      runtime error with the traceback.
- [x] Version mismatch: a generated package stamped with a different
      runtime version fails at init with a clear message.
- [x] Benchmark (not a pass/fail test): calls per second for a function
      call, a task call, a record copy, and a field access through a
      reference. This feeds the tutorial's cost slide.

Icarus runs the subset allowed by decision 2, via a marker.

Done (2026-10-23). Tests (all on `available_sims_dpi(excl=["xsm"])`, see
decision 2):
- `test_spike_records.py` (data `spike_records/`): copies, references both
  ways, nested references, `copy()` snapshots, identity on round trips,
  interfaces implemented on each side (functions, tasks, callbacks), use
  after `dispose()`, refcounts, a 500-reference loop with the object table
  staying at 64 slots, Python exceptions in functions and tasks, timings.
- `test_records_types.py` (data `records_types/`, from `types.json`):
  every field/parameter type at its extremes, base/derived records, signed
  and 64-bit enums, 1/12/80/100-bit ints, lists of lists and of records,
  empty and 4 KB byte queues, UTF-8 strings, interface-typed parameters,
  parameter names that clash with generated locals; the same checks run
  against an SV and a Python implementation.
- `test_records_dfm.py`: `GenFromSpec` feeding the spike testbench, and
  `GenFromPy` with a record and interface declared in Python (data
  `records_py/`, the tutorial's 2b shape).
- `test_records_version.py`: a package stamped with a newer version stops
  the simulation with `$fatal` at package init, before any `initial`
  block; the Python module raises on import.

Found and fixed along the way: a parameter named `m_obj` shadowed the
proxy's member (generated bodies now use `this.`); list typedefs were
renamed to public `list_<elem>_t` because SV implementations of interface
methods must spell them; the version check uses `$fatal` because `$finish`
lets the current time step (including `initial` blocks) run.

Benchmark (Verilator; spike record of 10 fields, `test_spike_records.py`
prints these each run):

| Operation | us/op |
|---|---|
| SV calls a Python function (2 ints) | 0.5 |
| Python calls an SV function (2 ints) | 1.5 |
| SV calls a Python task (record copy in and out) | 22 |
| Python calls an SV task (record copy in and out, `#10`) | 24 |
| SV reads one field of a Python object (reference) | 0.08 |
| Python reads one field of an SV object (reference) | 1.6 |
| Copy a record SV->Py / Py->SV, no byte payload | 3.5 / 3 |
| Copy a record SV->Py / Py->SV, 1500-byte payload | 27 / 26 |

Task calls are dominated by scheduling between the two event loops, not by
the data.

## Phase 8: `gen-from-sv` (pyslang)

- [x] SV front end, `src/hdl_if/gen/front/sv.py`:
  - Parse with pyslang from file lists, include dirs, defines and `-f`
    files.
  - Classes become `RecordDef`s (public data members by default),
    `interface class` becomes an `InterfaceDef`, and `typedef enum` an
    `EnumDef`.
  - Type mapping: `bit/logic [N:0]`, `int`/`shortint`/`longint`/`byte`,
    signedness, `real`, `string`, `byte[$]`/`byte unsigned[$]`, queues and
    dynamic arrays, enums, class handles (records or interfaces).
  - Packed structs are a later addition.
- [x] Filters:
  - `--sv-fields=public|rand|all`.
  - Per-class field include/exclude, and method include/exclude.
  - Stopping at or skipping base classes, with UVM library bases
    (`uvm_void`, `uvm_object`, `uvm_transaction`, `uvm_sequence_item`, ...)
    excluded by default and re-includable.
- [x] `gen-from-sv` subcommand and the `pyhdl-if.GenFromSv` dfm task.
- [x] Records taken from existing SV classes: an SV class the user already
      has (e.g. `pkt_item`) can't be regenerated. Generate the *companions*
      instead (`<rec>_if`, copy functions, and the reference adapter) against
      the existing class, rather than a new `class <rec>`. Accessor support on
      the existing class itself comes from a generated wrapper that
      implements `<rec>_if`. Confirm this approach in the spike, with a
      `uvm_sequence_item` subclass.
- [x] Dependency handling per decision 3 (`[sv]` extra; skip if pyslang
      is missing).

Tests: unit tests (SV source → IR) covering every supported type, each
filter, UVM base exclusion (using a minimal UVM stub so pyslang doesn't need
the whole UVM library), and clear errors for unsupported constructs. A sim
test on `available_sims_uvm()`: a `uvm_sequence_item` subclass is copied and
referenced from Python.

Done (2026-10-24): `src/hdl_if/gen/front/sv.py` (pyslang `driver.Driver`, so
`-f`, `-I`/`+incdir+`, `-D`/`+define+` work as in slang), `gen-from-sv` in
`cmd_gen.py`, `GenFromSv` in `dfm/gen_from.py` (sources come from the SV
FileSets it needs, e.g. `SimLibUVM`'s and the user's). Tests:
`tests/unit/gen/test_front_sv.py` (UVM stub in `gen/data/sv/`), and
`tests/unit/test_records_uvm.py`, which runs real UVM on Verilator: a
`uvm_sequence_item` subclass with queue, dynamic and fixed-size array
fields and a queue of class handles is copied to a Python implementation
of the user's `interface class`, and modified from Python through a
reference. Notes:
- IR additions: `FieldDef.sv_type`, `ParamDef.sv_type`,
  `MethodDef.sv_rtype`, `MethodDef.sv_ret_name` keep the user's SV spelling
  (a declaration with `%s` for the name), because generated code must match
  existing SV types exactly: `logic [31:0]` is not `bit [31:0]` in an
  implemented prototype, and unpacked arrays of `byte` and `byte unsigned`
  do not assign to each other. User containers get a typedef (`__svt<N>`)
  and element-by-element helpers. They round-trip through the spec
  (`sv_type`, `sv_returns`, `sv_ret_name`).
- `--sv-fields` is `public` or `rand`; there is no `all`, because `local`
  and `protected` members cannot be reached from generated code.
- Defaults: roots are every class, interface class and enum typedef in
  every package except `std`, `uvm_pkg` and `pyhdl_if`; use `-i` to narrow
  that. Base walk stops at `uvm_pkg::*` (`--no-default-stops` to clear,
  `--stop-at`/`--skip-base` to adjust).
- Records from SV must be constructible: abstract classes, or constructors
  with arguments lacking defaults, are errors that say so.
- A class-typed method parameter is a copy (decision 1). An existing SV
  `interface class` cannot name the generated `<rec>_if`, so passing a
  reference from SV goes through `<rec>_ref_to_py(<rec>_wrap(obj))`.
- A task's leading `output` argument is its result (name kept in
  `sv_ret_name`); other output/inout/ref arguments are errors.
- Not supported yet: packed structs/unions, associative arrays, arrays of
  arrays in class fields, parameterized classes, anonymous enums.
- `<rec>_wrap(v)` became public (it was `__<rec>_wrap`).
- dv-flow-libhdlsim fix revised: listing `__ALL.a` again after `__Dpi.o`
  caused duplicate symbols in the UVM build (something in the archive
  pulls its own `__Dpi.o`). The fix now passes `V<top>__Dpi.o` in
  `VM_USER_LDFLAGS`, which Verilator's link rule puts before the archive.
  Now upstream (see below).
- Found: since dv-flow-libhdlsim `22e5021` (2026-08-28), `SimLibUVM` on
  Verilator uses the UVM DPI backend from verilator-bin and builds with
  `--vpi`. With `--vpi`, Verilator's generated `main()` runs every
  `vlog_startup_routines` it links, including pyhdl-if's VPI-mode start-up,
  which calls `vpi_register_systf` (unsupported by Verilator): abort.
  Decision (2026-10-24): Verilator builds must not use `--vpi`; pyhdl-if
  integrates via DPI. Fixed in dv-flow-libhdlsim
  (upstream): `SimLibUVM` now builds UVM's DPI layer without `--vpi` by
  default. It compiles a generated wrapper (`uvm_dpi_novpi.cc`) with
  `uvm_common.c`, `uvm_regex.cc` and `uvm_svcmd_dpi.c`, and supplies the one
  VPI routine the command-line reader needs (`vpi_get_vlog_info`, from the
  Verilated context, using Verilator's internal `verilated_imp.h` as
  `verilated_vpi.cpp` does). `UVM_HDL_NO_DPI` compiles out the register
  backdoor; a new `backdoor: true` parameter restores the old full build
  with `--vpi`. `test_records_uvm.py` uses the default and checks that
  `--vpi` is absent, that `uvm_re_match` matches a real regex, and that
  UVM's command-line processor sees a plusarg.
- Also guarded pyhdl-if itself (`src/entry.c`): `pyhdl_if_vpi_entry`
  returns at once when `vpi_get_vlog_info` names Verilator, leaving
  start-up to the DPI entry `pyhdl_if.sv` calls. So `backdoor: true`
  (`--vpi`) now works too; `test_records_uvm.py` runs both profiles.

## Phase 9: Drift check and versioning

- [x] `--check` on every `gen-from-*` command: regenerate into memory, diff
      against the checked-in files, exit non-zero and print the diff on
      mismatch.
- [x] Runtime version check wired up in both generated outputs (SV package
      init, Python module import).
- [x] Policy, written into the design doc: when `PYHDL_IF_RT_API_VERSION`
      changes, and how long older versions are accepted.
- [x] CI: run `--check` over every checked-in generated file in the repo
      (tests and examples).

Tests: `--check` passes on clean output and fails on an edited file; an
old-version stamp is accepted or rejected according to the policy.

Done (2026-10-24). `--check` was built in Phase 6 (`test_cli_gen.py`
covers clean, edited and missing files). Version checks are tested in
`test_records_version.py` (SV `$fatal` at package init; Python import) and
`test_rt_api_version.py` (the accepted range, with patched constants). The
policy is in the design doc under "Versioning policy". CI:
`.github/workflows/ci.yml` runs `scripts/gen_records_goldens.py --check`
before the tests; the script lists every checked-in generated file (the
test goldens; the tutorial examples should be added to its `GOLDENS` list
as they are written). The Forgejo workflow builds wheels and docs only, so
it needs no change.

## Phase 10: Documentation

Sphinx, under `doc/source/`:

- [x] New page `records_interfaces.rst`, added to the `index.rst` toctree
      after `structs`. It covers:
  - concepts (records, interfaces, who implements an interface);
  - copy vs. reference, and the asymmetry between the two languages;
  - `dispose()` and lifetime;
  - choosing copy vs. reference, with the measured costs from Phase 7;
  - checking generated code into git, and running `--check` in CI.
- [x] Per-front-end how-tos: from Python (dataclass, Protocol, IntEnum),
      from SV (filters, UVM classes), and from a spec (v2 format and schema).
- [x] Generated-code reference: what each generated class is for, on each
      side, with a small annotated example for one record and one
      interface.
- [x] `cmdref.rst`: no work, since sphinx-argparse picks up the commands.
      Check that the help text reads well.
- [x] Cross-links from `sv_api.rst` and `structs.rst`, explaining when to
      use `@api`/ctypes structs and when to use the new path.
- [x] `doc/ChangeLog.md` entry; mark the design doc "implemented".
- [x] Docstrings on all new public Python APIs (`Ref`, `SvRef`, the
      generator entry points), and SV doc comments in generated code so
      sphinx-systemverilog can document a generated package.

Tests: the docs build with no new warnings (the CI docs job); the doc
examples are taken from files the test suite generates, so they can't
drift.

Done (2026-10-24): `doc/source/records_interfaces.rst` (concepts, copy vs.
reference, interfaces, lifetime, errors, measured costs, versions, relation
to `@api`), with `records_from_py.rst`, `records_from_sv.rst`,
`records_from_spec.rst` and `records_generated.rst` under it; in the index
after `structs`. Every code example is a `literalinclude` of a test file or
generated golden. `py_api.rst` has a "Records and interfaces" section
(`hdl_if.rt`, `hdl_if.rt_api`, the generator entry points). Notes in
`structs.rst` and `sv_api.rst` point to the new chapter. `doc/ChangeLog.md`
has an "Unreleased" entry; the design doc is marked implemented. The docs
build with no warnings (a `uvm_pkg::*` in a `gen-from-sv` help string was
read as RST emphasis in cmdref; reworded). Generated SV carries `/** */`
comments on the interface classes, value classes and public functions.

## Phase 11: Map `@api`/`@imp`/`@exp` onto the IR (optional)

- [x] Convert an `ApiDef` (`impl/call/api_def.py`) into an `InterfaceDef`
      plus a per-method implementer, so existing APIs can use the new back
      ends.
- [x] Decide whether `api-gen-sv` should eventually emit through the new back
      end. It doesn't for now; existing output must not change.

Tests: the existing `api-gen-sv` tests are unchanged; conversion unit tests.

Done (2026-10-24): `src/hdl_if/gen/front/api.py`, `interface_from_api()`
returns the interface plus a method -> `"sv"`/`"py"` map (`@imp` is SV,
`@exp` is Python). Types go through the Python front end's hint mapping,
so `ctypes.Structure` and `ctypes.py_object` parameters are rejected with
a message naming the method and parameter. Tests:
`tests/unit/gen/test_front_api.py`. Decision: `api-gen-sv` keeps its own
generator; its output is unchanged.

## Follow-ups

Not done here; in rough priority order.

1. **xsim**: `pyhdl_if.sv` uses `$stacktrace`, which Vivado 2023.1's xsim
   does not support; every DPI test fails on xsim (pre-existing). The new
   tests exclude xsim.
2. **Faster byte queues**: a DPI open-array helper in the native library
   that builds `bytes` directly; it changes only `pyhdl_if_rt_bytesToPy/
   FromPy` and `hdl_if.rt.conv`, not generated code.
3. **SV front end gaps**: packed structs/unions, associative arrays, arrays
   of arrays, parameterized classes, anonymous enums.
4. **Passing a derived record by reference where the base is expected**:
   SV unwraps a returning reference only to the exact record type
   (`$cast` to `<rec>_sv_adapter`).
5. **Tutorial examples**: done differently (2026-10-24). The examples
   (`examples/tutorial/`) generate their glue in the dfm flow
   (`GenFromSv`/`GenFromPy`) rather than checking it in, so there is
   nothing to add to `GOLDENS`. `tests/unit/test_tutorial_examples.py`
   runs every example on Verilator, and each example's Python-only tests.

## Out of scope here

The tutorial examples (`examples/tutorial/`) are tracked in `session_plan.md`.
Their dependencies on this plan:

- 2a needs Phases 5-8.
- 2b needs Phases 4-7.
- 3a needs Phases 4-7 (plus scapy and the SV facade).
- 3b needs Phases 4-8.

## Notes

### Phase 1 (spike) findings, 2026-10-23

Mechanism, as built:

- **Copy transport.** A record crosses as a *payload*: a tuple of field
  payloads (ints, bools, floats, strs; nested records as nested tuples or
  None; lists as lists; byte queues as a list of ints; ints wider than 64
  bits as a hex string). SV builds and reads payloads with plain C-API calls;
  Python converts payload <-> dataclass in one generic, hint-driven place
  (`hdl_if.rt.conv`: `rec_from_sv`, `rec_to_sv`, `conv_for`). Method
  arguments cross as payloads too, converted by the generated Python
  proxy/adapter. Byte queues go through `pyhdl_if_rt_bytesToPy/FromPy`, so
  their format can change without regenerating.
- **Python references to SV objects** (`pkt_sv_ref`, `I_sv_proxy`): SV
  registers an adapter (`ICallApi`) in the object table and creates the
  Python object with `hdl_if.rt.sv_obj_new(cls, id)`. Not via `newObj`:
  that sets `obj._proxy = CallProxyDPI(obj, ...)`, a reference cycle that
  would defer release to the cyclic GC. Calls go through the endpoint's
  `invoke_hdl_f`/`invoke_hdl_t`.
- **Release.** `SvObj.__del__` only appends the id to a list; it never
  calls SV and never raises. `allocObjId` calls `pyhdl_if_rt_reapObjIds()`
  (which takes that list) before growing the table. Ids are never stale: an
  id is released only once the single Python object holding it is gone.
  500 refs created and dropped in a loop leave the table at 64 slots.
- **SV references to Python objects** (`pkt_py_ref`, `I_py_proxy`) hold a
  `PyObject` with one reference, released by `dispose()`; a second
  `dispose()` is a no-op; use after `dispose()` is a runtime error
  (`pyhdl_if_rt_error`, counted in `pyhdl_if_rt_errors`, fatal unless
  `pyhdl_if_rt_error_fatal` is cleared). Simple fields are read with
  `PyObject_GetAttrString`; enums, byte queues, lists, wide ints and nested
  records go through `hdl_if.rt.get_field/set_field` so Python sees typed
  values (e.g. an `IntEnum`, not an int).
- **Identity is preserved across round trips.** Passing a reference back to
  the side that owns the object unwraps it (SV: `pyhdl_if_rt_svObjGet` +
  `$cast` to the adapter; Python: `PyAdapter._impl`), so SV gets its own
  `pkt` back, not a proxy to a proxy.
- **Ownership rule for references passed into SV methods:** the callee
  owns the reference it receives and should `dispose()` it when done (a
  no-op for a local object). Generated adapters do not dispose arguments,
  because a callee may keep them (callbacks). Generated code disposes the
  temporaries it creates itself (e.g. in `<rec>_from_if`).
- **Python implementations called from SV** go through
  `pyhdl_if_rt_callPyFunc` / `pyhdl_if_rt_callPyTask` (a plain
  `getattr`+call, and `hdl_if.rt.invoke_py_t`), so the Python object needs
  no `_proxy`. A Python exception in a task delivers `hdl_if.rt.ERROR`
  instead of hanging SV.

Deviations from the design doc:

- `I_sv_adapter` is not parameterized (`#(type T=I)`). It holds an `I`
  handle, because SV must `$cast` an incoming object-table entry to the
  adapter to unwrap it, and a parameterized class has no single type to
  cast to.
- Method interfaces get `<I>_to_py()` / `<I>_from_py()` package functions,
  and records `<rec>_to_py()`, `<rec>_from_py()` (copies),
  `<rec>_ref_to_py()`, `<rec>_ref_from_py()` (references), `<rec>_copy()`
  and `<rec>_from_if()` (snapshot through accessors). Setters for nested
  record fields take a value (`set_h(hdr v)`) and copy it.

Fixes to existing runtime code that the new path depends on:

- `pyhdl_if_setSem` stored a borrowed result that could be freed before the
  waiting SV task read it. It now takes a reference (the collector owns it).
- `TaskCallClosure` leaked the task result. It now releases it, but only
  for adapters that implement the new `ICallApiOwnedRes` (which extends
  `ICallApi`), because older generated code returns borrowed `None`.
- Verilator cannot `$cast` between unrelated interface classes, hence
  `ICallApiOwnedRes extends ICallApi`.

Tooling issues found:

- **dv-flow-libhdlsim link order (needs an upstream fix).** For designs big
  enough that Verilator splits its output (`VM_PARALLEL_BUILDS=1`),
  `vlt_sim_image.py` links `V<top>__Dpi.o` after `V<top>__ALL.a`, so the
  DPI export implementations are never pulled from the archive and the
  link fails. Fixed locally in `packages/dv-flow-libhdlsim` by listing the
  archive again after `__Dpi.o`. This must go upstream before CI can run
  these tests.
- Verilator rejects `longint unsigned'(x)` casts and two-word types in
  `for` declarations; generated code uses `64'(x)` and `int` loop indices.
- xezim cannot parse `interface class` (it fails on `pyhdl_if.sv` itself),
  so it cannot run pyhdl-if today. The tutorial must use Verilator.
- Not yet confirmed: generating companions for an existing
  `uvm_sequence_item` class. Moved to Phase 8, which has a UVM sim test.

Timings (Verilator, one record with 10 fields incl. a nested record):

| Operation | us/op |
|---|---|
| copy SV->Py, no byte payload | 3.5 |
| copy Py->SV, no byte payload | 3.0 |
| copy SV->Py / Py->SV, 256-byte payload | 7.5 / 7.5 |
| copy SV->Py / Py->SV, 1500-byte payload | 27.5 / 26 |
| SV calls Py with a copy; Py reads 4 fields | 8 |
| SV calls Py with a ref; Py reads 4 fields via SV | 12.5 |
| SV reads one field of a Python object via a ref | 0.08 |

Decision: keep the field-by-field (tuple) transport. Byte queues dominate
large copies (~17 ns/byte); a hex string built in SV was slower in
Verilator (110 us at 1500 bytes). Follow-up: a DPI open-array helper in
the native library building `bytes` directly; it only changes
`pyhdl_if_rt_bytesToPy/FromPy` and `hdl_if.rt.conv`, not generated code.
