# Language-Neutral Interfaces and Records

Status (2026-10-24): implemented. The implementation plan, with the
decisions taken on the way and the deviations from this document, is in
`doc/design/neutral_api_and_records_plan.md`; user documentation is the
"Records and Interfaces" chapter (`doc/source/records_interfaces.rst`).
Driven by the tutorial plan in `session_plan.md` (sections 2 and 3).

## Goal

Let SystemVerilog and Python share two kinds of things, regardless of
which language they were declared in:

- **Records (data).** A value type that can be *copied* across the
  boundary, or *referenced* on the other side.
- **Interfaces (methods).** A set of functions/tasks that *either side*
  can implement, and the other side calls.

Where a type is declared (Python or SV) only picks the front end. It does
not decide who implements anything or which way data flows.

## Principles

1. **Two concepts only: record and interface.** A reference to a record is
   not a third concept; it is a proxy for the record's accessor interface
   (see below).
2. **Implementer is chosen per interface, at bind time.** The definition
   carries no direction. Callbacks are a second interface implemented by
   the opposite side. (Today's `@imp`/`@exp` fix direction per method in
   the definition; that becomes a special case.)
3. **Generated code is written only against the pyhdl-if runtime.**
   - No per-API C/DPI code; nothing for the consumer to compile.
   - Generated `.sv` and `.py` files are checked in as primary source.
   - The generator (pyslang, Protocol/dataclass introspection) is an
     author-time tool. Consumers need only the files plus the pyhdl-if
     wheel.
4. **Generated files are never hand-edited.** Hand-written behavior lives
   in subclasses, facades, or the class that implements an adapter.

## Definitions and front ends

A neutral IR (an extension of today's `ApiDef` and JSON spec):

- **Record:** name, ordered fields. Field types: bool, sized ints/uints,
  real, string, enum, nested record, queue/list of any of these,
  byte queue (`byte[$]` / `bytes`).
- **Enum:** name, base width, named values. Generated as an SV `typedef enum`
  and a Python `IntEnum`, in both directions.
- **Interface:** name, methods. Each method is `func` or `task`, with
  typed params and return. Param/return types are the record field types
  plus records (by copy or by reference) and interfaces (by reference).

Front ends producing the IR:

| Source | Records | Interfaces |
|---|---|---|
| Python | `@dataclass` only | `typing.Protocol` (`async def` = task) |
| SystemVerilog (pyslang) | `class` data members | `interface class` (`task` = task) |
| JSON spec | yes | yes |

SV field selection: **public (non-`local`, non-`protected`) data members
only** by default. The SV front end lets the user filter what is mirrored:

- **Fields:** `--sv-fields=public|rand|all`, plus per-class include/exclude
  lists.
- **Methods:** include/exclude lists, for SV classes whose methods are
  exposed as an interface.
- **Base classes:** the inheritance walk can stop at, or skip, named base
  classes. UVM library bases (`uvm_void`, `uvm_object`, `uvm_transaction`,
  `uvm_sequence_item`, ...) are excluded by default, since their fields are
  rarely useful on the other side; the user can re-include them.
- (later, if needed) an opt-in comment/attribute marker

This is how `uvm_object` subclasses such as `pkt_item` are supported: their
own (and user-chosen base-class) fields are mirrored, the UVM base is not.

Python records are restricted to dataclasses: fields come from
`dataclasses.fields()` with their annotations.

## Copy vs. reference

The two languages are asymmetric:

- **Python** can intercept attribute access, so a copy and a reference look
  the same: `pkt.ttl` works on both.
- **SystemVerilog** cannot intercept field access. A copy has plain fields;
  a reference must go through accessor methods (`get_ttl()`,
  `set_ttl(v)`) on an interface class.

So every record also gets an **accessor interface**, and a reference is a
proxy for it, built with the same proxy/adapter machinery as any other
interface.

Generated for record `pkt`:

| | SV | Python |
|---|---|---|
| Value type (copy) | `class pkt` with plain fields | `@dataclass pkt` |
| Accessor interface | `interface class pkt_if` (`get_*`/`set_*`, `dispose()`) | the dataclass's attributes |
| Value implements accessors | `pkt implements pkt_if` | (trivial) |
| Reference to other side's object | `pkt_py_ref implements pkt_if` | `pkt_sv_ref` (properties) |
| Copy across | `pkt_to_py()`, `pkt_from_py()` | via runtime |

Consequence in SV: code written against `pkt_if` works on a local `pkt` and
on a reference to a Python object. Code that wants direct field access
takes a copy. Fields = snapshot; accessors = live view.

Rules:

- **Nested records:** a reference's `get_hdr()` returns a reference
  (`hdr_if`); a copy deep-copies. An object is a copy or a reference all
  the way down.
- **Queues/lists through a reference:** the getter returns a copy of the
  whole queue; the setter replaces it. Indexed accessors (`size_opts()`,
  `get_opts(i)`, `set_opts(i, v)`) only if a real case needs them.
- **Python hides the difference, but mutation semantics differ.** Setting a
  field on a copy does not change the source. Document it; give both forms
  `copy()` for an explicit snapshot.
- **Lifetime:** a reference holds its target through the runtime's handle
  registry.
  - Python proxies release on GC.
  - SV has no finalizers, so every generated SV interface class (accessor
    interfaces and method interfaces alike) declares `dispose()`. On a
    reference/proxy it releases the target from the registry; on a local
    implementation it is a no-op, so code written against the interface can
    always call it. Using a reference after `dispose()` is an error reported
    by the runtime.
- **Cost:** a reference pays one boundary crossing per field access; a copy
  pays once up front.

## Interfaces

For interface `I`, generate on each side:

- **Proxy:** implements `I` locally and forwards calls to the other side.
- **Adapter:** receives calls from the other side and dispatches to a local
  implementation of `I`.

| | SV | Python |
|---|---|---|
| Interface | `interface class I` (plus `dispose()`) | `Protocol I` |
| Proxy (other side implements) | `I_py_proxy implements I` | `I_sv_proxy` |
| Adapter (this side implements) | `I_sv_adapter #(type T=I) implements pyhdl_if::ICallApi` | `I_py_adapter` |

Binding picks which pair is used. Tasks are allowed in both directions
(already supported today via `ImpTask`/`ExpTask`).

Existing pieces to build on: `pyhdl_if::ICallApi` (`invokeFunc` /
`invokeTask`, `src/hdl_if/share/dpi/pyhdl_if_icall_api.svh`), the
generated `_imp_impl #(ImpT)` dispatcher and `_exp_impl` caller
(`src/hdl_if/impl/call/gen_sv_class.py:411-600`), and the Python C API
already exposed to SV (`PyObject_GetAttrString` etc.).

## Runtime contract

Because generated code is checked in, the runtime API it calls is a
compatibility contract:

- Every generated file records the generator version and the runtime API
  version it targets; the runtime checks this at load time.
- Output is deterministic, so CI can regenerate and diff to catch drift
  between declaration and checked-in code.
- Record copy goes through a single runtime entry point per direction, so
  the transport (field-by-field vs. one packed int/byte array, cf.
  `pack_ints` in `uvm/wrap/object.py`) can change without regenerating.

### Versioning policy

Two numbers, with different jobs:

- **Runtime API version** (`PYHDL_IF_RT_API_VERSION` in `hdl_if/rt_api.py`
  and in the `pyhdl_if` SV package; they must be equal). Generated code is
  stamped with it and checks it when loaded: the SV package at package
  initialization (`$fatal` on mismatch, before any `initial` block runs),
  the Python module at import (`RuntimeError`). A stamp is accepted when
  `PYHDL_IF_RT_API_MIN_VERSION <= stamp <= PYHDL_IF_RT_API_VERSION`.
  - An *additive* change (a new runtime function or Python helper that new
    generated code uses) bumps `VERSION` only. Older generated code keeps
    working; newly generated code asks for a newer pyhdl-if.
  - A *breaking* change (a runtime function removed, or its signature or
    meaning changed) bumps `VERSION` and raises `MIN_VERSION` to it. Older
    generated code then fails with "Regenerate it". Breaking changes are
    made only in a minor release and listed in `doc/ChangeLog.md`; prefer
    keeping the old entry point next to the new one for at least one minor
    release, so `MIN_VERSION` lags `VERSION`.
- **Generator version** (`GEN_VERSION` in `hdl_if/gen/naming.py`): the
  shape of generated code. Bumped whenever the generators emit different
  output for the same input. It is written in the file header for
  information only; nothing checks it at run time. `--check` is what
  catches checked-in code that no longer matches the generator, and CI runs
  it (`scripts/gen_records_goldens.py --check`).

## Relationship to existing features

- `@api` / `@imp` / `@exp` and the JSON spec: kept. They map to a neutral
  interface plus a fixed implementer per method. New code uses the neutral
  form.
- `ctypes.Structure` ↔ SV struct marshaling: kept; records are the
  class-based, nestable successor.
- `uvm/wrap/object.py` (fields found by parsing `sprint()`, pack/unpack per
  attribute access): not used by this design; generated accessors replace
  it for new code.
- Unrelated fix: docstrings in `src/hdl_if/decorators.py` describe
  `@imp`/`@exp` backwards.

## Tutorial mapping

| Section | Mechanism |
|---|---|
| 2a | `pkt_item` record declared in SV; monitor hands Python a copy *or* a reference; coverage code is identical either way |
| 2b | Record declared in Python (dataclass); SV sequence receives copies |
| 3a | `ipv4_pkt` etc. are SV references to scapy-backed Python objects, used through accessor/interface classes; consumer sees only SV |
| 3b | Env API declared as an SV `interface class`, implemented in SV, called from Python through a proxy (tasks) |

Tutorial beats this enables: "no C compiler, no DPI code"; "the generated
mirror is in git, read it"; a measured copy-vs-reference cost slide.

## Decisions

- **Releasing references from SV:** explicit `dispose()` on the generated SV
  interface class, which releases the target from the registry (see
  Lifetime).
- **Enums:** each SV enum generates a Python `IntEnum`, and each Python
  `IntEnum` generates an SV `typedef enum`.
- **`uvm_object` subclasses:** supported through user filtering of base
  classes, methods, and fields; UVM base-class fields excluded by default
  (see Definitions and front ends).
- **CLI:** separate commands per input, because the inputs differ (SV needs
  file lists, include dirs, defines, and a top package; Python needs modules;
  JSON needs a spec file). Each command emits both the SV and Python sides.
  Commands: `gen-from-sv`, `gen-from-py`, `gen-from-spec`. The
  existing `api-gen-sv` stays as-is for compatibility.
- **No context manager / explicit release on Python proxies.** CPython's
  reference counting already releases a proxy as soon as its last reference
  goes away, so release is deterministic except for reference cycles, and
  the cost of a delayed release is a little memory. Resources with real
  close semantics (e.g. a pcap file) get an ordinary interface method like
  `close()`; that's behavior, not lifetime. Can be added later without
  breaking anything. Constraint this puts on the runtime: the release path
  run from `__del__` must be safe at any time, including after the
  simulation has ended or during interpreter shutdown (no-op if the SV side
  is gone, never raises).

## Open questions

None at present.
