# Documenting the SystemVerilog APIs properly with `sphinx-systemverilog`

**Status:** Phases 0–5 complete; see §11. Release of sphinx-systemverilog 0.6.1 outstanding.
**Date:** 2026-09-14
**Scope:** the SystemVerilog API surface under `src/hdl_if/share/`, the doc comments in
it, and the pages in `doc/source/` that publish it.

**Relationship to the other two plan documents.**
`doc/sphinx-systemverilog-migration.md` is a completed record: it replaced the
Verilator→Perl→Doxygen→Breathe chain with the extension, and is history.
`doc/documentation-plan.md` is the live repo-wide restructuring plan (Phases 1–6, Python
and SV); its **Phase 4** covers SV doc comments and is marked "mostly done".
**This document supersedes Phase 4** — it treats the SV reference as its own deliverable,
measures it, and takes it from 11% coverage to complete. Phase 4's D4-1…D4-4 are real and
retained; D4-5…D4-8 are folded into the phases below with the blockers named.

---

## 1. What "fully and properly" means

Three things, none of which is true today:

1. **Complete** — every SystemVerilog declaration a user can legitimately write against
   appears in the published reference, and nothing internal does. Today the split is
   accidental: 64 of the 114 published classes are internal transport machinery, and the
   modules users actually instantiate are absent.
2. **Described** — every published declaration carries prose that says what it does, what
   its arguments mean, and whether it works. 11% of our SV objects carry a doc comment.
3. **Enforced** — the build fails when either of those slips. Today `make html` fails for
   an unrelated reason and there is no coverage check at all.

---

## 2. Measured baseline

All numbers below were produced by building the extension's index over the real sources
(`uvm_pkg.sv` + `pyhdl_if.sv` + `pyhdl_uvm.sv`, the current `conf.py` configuration) and
by reading `doc/build/html/objects.inv`. They are counts of *indexed objects* — packages,
classes, functions, tasks, properties, typedefs, macros — not of lines.

Measured against `sphinx-systemverilog` **0.6.0** (`de136a1`, `main`, tag `v0.6.0`,
confirmed against the remote), installed editable into `packages/python` and re-validated
after `ivpm update --py-force-install`. A clean `make html` reproduces every figure here:
6896 objects indexed, 270 published, four warnings, exit 2 under `-W`.

### 2.1 Doc-comment coverage, by file

1662 objects come from `src/hdl_if/share/`. 193 carry a doc comment: **11%**.

| File | Objects | Documented | |
|---|---:|---:|---:|
| `dpi/pyhdl_dpi_imports.svh` | 597 | 0 | 0% |
| `uvm/pyhdl_uvm_apis.svh` | 537 | 0 | 0% |
| **subtotal, the two bulk files** | **1134** | **0** | **0%** |
| `dpi/pyhdl_if.sv` | 47 | 14 | 29% |
| `dpi/py_object.svh` | 18 | 15 | 83% |
| `dpi/py_utils.svh` | 17 | 9 | 52% |
| `dpi/py_list.svh` | 8 | 5 | 62% |
| `dpi/py_tuple.svh` | 7 | 5 | 71% |
| `dpi/py_dict.svh` | 6 | 2 | 33% |
| `dpi/py_iter.svh` | 6 | 6 | 100% |
| `dpi/py_ctxt.svh` | 4 | 4 | 100% |
| `dpi/pyhdl_if_call_api.svh` | 9 | 0 | 0% |
| `dpi/pyhdl_if_macros.svh` | 7 | 0 | 0% |
| `dpi/pyhdl_if_taskcall_closure.svh` | 7 | 0 | 0% |
| `dpi/pyhdl_if_time_cb.svh` | 6 | 0 | 0% |
| `dpi/pyhdl_if_icall_api.svh` | 3 | 1 | 33% |
| `dpi/pyhdl_if_call_dpi.svh` | 3 | 0 | 0% |
| `dpi/pyhdl_if_{init,call_init,pi_dpi,tlm_init}.svh` | 4 | 0 | 0% |
| `dpi/pyhdl_if_pytest.svh` | 1 | 1 | 100% |
| `uvm/pyhdl_uvm_component_proxy.svh` | 44 | 39 | 88% |
| `uvm/pyhdl_uvm_sequence_proxy.svh` | 42 | 37 | 88% |
| `uvm/pyhdl_uvm_analysis_port.svh` | 36 | 23 | 63% |
| `uvm/pyhdl_uvm_object.svh` | 30 | 25 | 83% |
| `uvm/pyhdl_uvm_object_rgy.svh` | 29 | 1 | 3% |
| `uvm/pyhdl_uvm_enum_rgy.svh` | 25 | 2 | 8% |
| `uvm/pyhdl_uvm_object_map.svh` | 22 | 0 | 0% |
| `uvm/pyhdl_uvm_object_string.svh` | 21 | 1 | 5% |
| `uvm/pyhdl_uvm_object_list.svh` | 20 | 1 | 5% |
| `uvm/pyhdl_uvm_object_type.svh` | 13 | 0 | 0% |
| `uvm/pyhdl_uvm_component.svh` | 13 | 0 | 0% |
| `uvm/pyhdl_uvm_reg.svh` | 13 | 0 | 0% |
| `uvm/pyhdl_uvm_reg_field.svh` | 11 | 0 | 0% |
| `uvm/pyhdl_uvm_pygen.svh` | 11 | 0 | 0% |
| `uvm/pyhdl_uvm_reg_block.svh` | 10 | 0 | 0% |
| `uvm/pyhdl_uvm_wrapper_factory.svh` | 10 | 0 | 0% |
| `uvm/pyhdl_uvm_cmdline_processor.svh` | 9 | 0 | 0% |
| `uvm/pyhdl_uvm_phase.svh` | 9 | 0 | 0% |
| `uvm/pyhdl_uvm_object_if.svh` | 3 | 0 | 0% |
| `uvm/pyhdl_uvm_macros.svh` | 3 | 2 | 66% |
| `uvm/pyhdl_uvm.sv` | 1 | 0 | 0% |
| **subtotal, hand-written sources** | **528** | **193** | **36%** |

The shape: four headline UVM units are at 83–88% (Phase 4's work), the `py_*` wrapper
classes are at 52–100%, and **everything else is at zero**. 26 files have no doc comment
at all.

### 2.2 What is published today

`objects.inv` contains **270** `sv:` objects across two pages:

| Page | Objects | Composition |
|---|---:|---|
| `uvm.html` | 220 | 114 classes, of which **60 are generated `*_exp_if` / `*_exp_impl` / `*_imp_if` / `*_imp_impl` transport classes** from `pyhdl_uvm_apis.svh`, all undocumented |
| `sv_api.html` | 50 | the six `py_*` classes and ten `py_from_*` / `py_import` / `py_gil_*` functions |

So **a clear majority of the classes** on the UVM reference page — 60 of 114 — are
machinery no user writes against, and the `pyhdl_if` reference page covers the
Python-C-API wrapper layer and nothing else. Counted as objects rather than classes the
generated layer is 60 of 220, because the hand-written classes carry documented members
and the generated ones contribute little beyond their own names.

### 2.3 What is not published at all

| Surface | Objects | Why absent |
|---|---:|---|
| `ICallApi`, `TaskCallClosure`, `PyHdlDpiTimeCB`, `CallEmptyBase`, the `pyhdl_if_call_api` functions, package globals | ~70 | no directive names them; `sv_api.rst` lists classes and functions one by one |
| `share/dpi/tlm_hdl2hvl_fifo.sv`, `tlm_hvl2hdl_fifo.sv` | 2 modules + ports/params | **not parsed** — excluded in `conf.py`, see F19 |
| `share/pyhdl_if_req_fifo.sv`, `pyhdl_if_rsp_fifo.sv`, `pyhdl_if_reqrsp_fifo.sv` | 3 modules | never in a build unit; same F19 defect |
| `share/vpi/tlm_*_fifo.sv` | 2 modules | same |
| `pyhdl_if_macros.svh`, `pyhdl_uvm_macros.svh` | 10 macros | indexed, never referenced by a directive (Phase 4's D4-7) |
| `py_builtins.svh` | 3 | F18 — the file does not compile and is unreferenced |

The TLM FIFO modules are the sharpest case: they are the only things in this repo a user
*instantiates* rather than calls, they have hand-written doc comments already, and they
are invisible.

### 2.4 Build health

`make html` **fails today**. `SPHINXOPTS = -W --keep-going`, and there are four warnings:

```
source/sv_api.rst:10:  WARNING: Literal block expected; none found.
source/uvm.rst:526:    WARNING: Literal block expected; none found.
source/uvm.rst:656:    WARNING: Literal block expected; none found.
source/uvm.rst:660:    WARNING: Literal block expected; none found.
```

The reported locations are in generated content; the causes are four correctly-authored
rST literal blocks in doc comments — `py_iter.svh:6`, `pyhdl_uvm_component_proxy.svh:33`,
`pyhdl_uvm_sequence_proxy.svh:41` and `:47`. See F1.

---

## 3. What the updated extension makes newly available

`packages/sphinx-systemverilog` is at **0.6.0** (`de136a1`). The migration was done against
0.1.x. Capabilities that exist now and that this repo does not use:

| Capability | Config / directive | What it buys us |
|---|---|---|
| Macro-content filtering | `sv_ignore_macro_content`, `:macro-members:` | Suppresses `` `uvm_*_utils ``-generated members that currently pad every registered class, with a note on the class saying what was hidden. **93** of our indexed members are macro-generated. |
| Trivial-`new` hiding | `sv_uvm_hide_trivial_new` (default on) | Already helping; worth stating as a decision rather than an accident. |
| Whole-tree scoping by path | `autosvsummary` `:files:` / `:exclude:` | The mechanism that removes the 64 generated classes from `uvm.html` without a hand-maintained class list. |
| Macros as first-class objects | `sv_document_macros` (already on) + `autosvsummary :kinds: macro` | **Closes D4-7.** Our 10 macros are already in the index; nothing references them. Verified: `PYHDL_IF_DEBUG`, `pyhdl_uvm_type_utils`, `pyhdl_uvm_enum_utils` all index with signature and doc. |
| Module parameters & ports | `autosvmodule :members:` | The TLM FIFO layer's real interface. Ports/params are shown even when undocumented, so this pays off the moment the modules are parsed. |
| Structural views | `:show-instances:`, `:show-used-by:`, `:show-parameters-used:`, `sv:instance-tree` | Applicable to the examples, not to the library. Low priority — noted so it is a decision, not an oversight. |
| Inheritance diagrams | `:show-inheritance:`, `sv:inheritance-diagram` | `pyhdl_uvm` is a wrapper hierarchy four levels deep; a diagram on `pyhdl_uvm_object` is worth more than its member list. Needs `dot`. |
| UVM testbench views | `sv:uvm-tree`, `sv:uvm-config`, `sv:uvm-schematic`, `sv:uvm-sequence`, `sv:uvm-binding` | Not for the library — it has no testbench. Candidate for a worked-example page built from `examples/uvm/component_proxy_smoke`. See Q3. |
| Coverage gate | the extension's own `scripts/check-docs-coverage.py` | A pattern to copy: compare the parsed index against the published `objects.inv` so a class that falls between two `:files:` patterns fails the build instead of vanishing. |
| `autosvpackage` | — | Documents a package and its contents in one directive; an alternative to the per-class lists in `sv_api.rst`. |

---

## 4. Findings and decisions to make

### F1 — rST literal blocks in doc comments are flattened (build-breaking)

`py_iter.svh` documents its usage with a correctly-formed rST literal block:

```
 * maps onto a SystemVerilog `while` loop::
 *
 *     py_iter it = new(PyObject_GetIter(seq));
 *     while (it.valid()) begin
```

The published HTML renders it as one run-on paragraph:

> `py_iter it = new(PyObject_GetIter(seq)); while (it.valid()) begin py_object item = it.next(); // … item.dispose(); end`

and docutils emits `Literal block expected; none found`, which `-W` turns into a build
failure. The doxygen docparse strips the ` * ` prefix without preserving the relative
indentation that makes the block a block.

**Verified not a regression from today's update** — 0.5.0 (`085b6b4`) produces the same
four warnings. It is a standing bug.

This is the one item that is upstream work in `sphinx-systemverilog`, not in this repo.
It gates everything else, because until it is fixed we either cannot build under `-W` or
cannot write a code example in a doc comment — and §5's conventions depend on being able
to do both. Two smaller things travel with it: single backticks (`` `valid` ``) render as
literal backtick characters rather than as code, and `documentation-plan.md` §5.1 already
records the Markdown-fence trap. All three are the same question — what subset of markup
a doc comment may contain — and should be answered once, upstream, and documented in
`docs/usage/doxygen-style.md`.

### F2 — `pyhdl_uvm_apis.svh` is generated, undocumented, and half the published reference

4461 lines, 537 indexed objects, zero doc comments, regenerated by:

```
% python -m hdl_if api-gen-sv -m hdl_if.uvm.wrap -o src/hdl_if/share/uvm/pyhdl_uvm_apis.svh
```

Hand-writing comments into it is not an option — the next regeneration discards them.
Three ways forward:

- **(a) Exclude it.** `autosvsummary :exclude:` / a `:files:` scope that omits it. The
  page drops from 220 objects to 160 — and from 114 classes to 54 — all of them
  hand-written API. Cheapest, and
  defensible: these are transport-layer classes generated from a Python API that *is*
  documented, on the Python side.
- **(b) Generate doc comments.** `ApiDef` already carries `_pycls`, so the Python class
  and its methods' `__doc__` are in hand at generation time; `MethodDef` would need a
  `doc` field threaded from `inspect`. `gen_sv_class.py` then emits `/** … */` above each
  generated class and method. ~a day's work, and it makes the SV and Python halves of the
  same API say the same thing by construction.
- **(c) Document the shape, not the members.** One hand-written page explaining the
  `*_exp_if` / `*_imp_impl` pattern, with the classes excluded from the reference.

**Recommendation: (a) now, (c) alongside it, (b) as a follow-up.** (a) is a one-line
change that removes the single biggest quality problem in the published docs; (b) is
worth doing but should not block it.

### F3 — `pyhdl_dpi_imports.svh` should stay undocumented, explicitly

597 objects: raw `import "DPI-C"` declarations of the CPython C API. These are not our
API and CPython documents them better than we would. `documentation-plan.md` §2.4 already
says this; the plan here is to make it *enforced* (excluded by scope) rather than merely
unreferenced, so the coverage gate in §7 does not count them against us.

### F4 — The TLM FIFO layer cannot be documented until it compiles (F19)

Unchanged and re-verified: `ICallApi::invokeTask` takes four arguments
(`retval`, `state`, `method`, `args`); all six implementations pass three, omitting
`state`. Confirmed today in `dpi/tlm_hdl2hvl_fifo.sv:116` and
`share/pyhdl_if_req_fifo.sv:117`.

This is not a documentation problem, but it is the binding constraint on documenting the
one part of the API users instantiate. The doc comments are already written. The work is
threading `state` through six closures and releasing the GIL around the blocking waits —
which is a correctness fix the code needs regardless.

**Decision needed (Q1):** fix F19 as part of this effort, or publish the TLM guide with
the modules documented by hand-written `sv:module::` directives until it lands?
Recommendation: fix it. Hand-written directives for code that does not compile documents
an API that does not exist.

### F20 — Each TLM interface is declared three times, under one name

Surfaced by parsing the TLM layer for the first time. `tlm_hdl2hvl_fifo` and
`tlm_hvl2hdl_fifo` each exist in **three** files:

| File | Contains | Entity declared |
|---|---|---|
| `share/dpi/tlm_hvl2hdl_fifo.sv` | DPI only | `tlm_hvl2hdl_fifo` |
| `share/vpi/tlm_hvl2hdl_fifo.sv` | VPI only | `tlm_hvl2hdl_fifo` |
| `share/pyhdl_if_req_fifo.sv` | both, selected by `` `ifdef PYHDL_IF_VPI `` | `tlm_hvl2hdl_fifo` |

(and the same three for `tlm_hdl2hvl_fifo`, via `share/pyhdl_if_rsp_fifo.sv`.)

The bodies are the same logic. The `share/` copies wrap it in `` `ENTITY_TYPE ``
macros so one file serves both back-ends; the split copies hard-code `interface`.
Only the `share/dpi` copies carry the doc comments written for D4-6.

Two consequences:

- **For documentation:** parsing more than one copy puts two objects with the same name
  in the index — a duplicate anchor and an ambiguous cross-reference. `conf.py` therefore
  parses exactly one copy of each, and says which and why.
- **For the build:** `ivpm.yaml` declares `src/hdl_if/share` as a lib-dir, and a lib-dir
  search resolves a name by *filename*. `share/pyhdl_if_req_fifo.sv` declares
  `tlm_hvl2hdl_fifo`, so that copy can never be found by name — which suggests the
  `share/` copies are either superseded or reached by some path other than lib-dir search.

**This is not a documentation decision and I have not made it.** Three copies of one
entity is a maintenance hazard regardless of the docs: the F19 fix had to be applied six
times because of it. Deciding which copy survives needs someone who knows whether the VPI
back-end is still live.


### F5 — The macro layer has a home now

D4-7 was parked because "the extension has no macro directive". It does:
`autosvsummary :kinds: macro`. Ten macros are already indexed. Seven are user-facing
(`PYHDL_IF_DEBUG`/`ENTER`/`LEAVE`/`ERROR`/`FATAL`, `pyhdl_uvm_type_utils`,
`pyhdl_uvm_enum_utils`); three are include guards and get excluded by name.

`pyhdl_uvm_type_utils` deserves care: it generates whole classes (`pyhdl_uvm_object_w`,
`pyhdl_uvm_component_w`, … — 12 of them, currently published undocumented). Document the
macro; exclude its output.

### F6 — `py_builtins.svh` (F18) is a decision, not a task

Does not compile, is unreferenced, is an abandoned sketch. Finish it or delete it. It
should not appear in the reference either way until that is resolved.

---

## 5. Target: what gets published

Three tiers, applied by scope rather than by enumeration, so a new file lands in the right
tier without anyone editing a list:

| Tier | Contents | Mechanism |
|---|---|---|
| **A — published reference** | `pyhdl_if` classes/functions/macros; `pyhdl_uvm` hand-written classes/macros; the five TLM FIFO modules | `autosvsummary` scoped by `:files:` / `:kinds:` |
| **B — parsed, not published** | `pyhdl_dpi_imports.svh`, `pyhdl_uvm_apis.svh`, `*_w` macro output, include guards | `:exclude:` / `:files:` exclusion, recorded with a reason |
| **C — not parsed** | the UVM library itself (needed for elaboration, never documented) | already the case |

Page structure — expressed against `documentation-plan.md` §4's target layout, and
equally applicable to today's flat `doc/source/`:

```
reference/sv_api.rst            pyhdl_if: the Python-C-API wrapper layer
  Classes                       py_object, py_ctxt, py_dict, py_iter, py_list, py_tuple
  Call interface                ICallApi, TaskCallClosure, PyHdlDpiTimeCB, CallEmptyBase
  Functions                     py_from_*, py_import, py_call_builtin, py_gil_*
  Macros                        PYHDL_IF_* (autosvsummary :kinds: macro)

reference/sv_tlm.rst            NEW — the TLM/FIFO modules
                                autosvmodule :members: x5, ports and parameters

reference/sv_uvm_api.rst        pyhdl_uvm, generated classes excluded
  Proxies                       component_proxy, sequence_proxy, analysis_port
  Object model                  pyhdl_uvm_object, object_type, object_if
  Registries                    object_rgy, type_rgy, enum_rgy, wrapper_factory
  Containers                    object_list, object_map, object_string
  Register model                reg, reg_block, reg_field
  Macros                        pyhdl_uvm_type_utils, pyhdl_uvm_enum_utils

guides/tlm.rst                  NEW — prose; the TLM API has no guide today
guides/uvm.rst                  existing prose, reference split out
```

Splitting `sv_uvm_api.rst` into sections by `:files:` groups means each group is a path
pattern, and the coverage gate catches anything that falls between two of them.

---

## 6. Configuration changes

`doc/source/conf.py`, added to what is there today:

```python
from sphinx_systemverilog import UVM_BOILERPLATE_MACROS

# Our own class-generating macro joins the UVM boilerplate set: it emits the
# *_w wrapper classes, which are an implementation detail of the registry.
sv_ignore_macro_content = [*UVM_BOILERPLATE_MACROS, "pyhdl_uvm_type_utils"]

# Every directive documents members unless it says otherwise.
sv_default_options = {"members": True}
```

plus, once F19 is fixed, the `sv_build_units` block that `conf.py:103-106` currently keeps
commented out, extended to the three top-level FIFO modules and the two VPI variants.

`sv_uvm_hide_trivial_new` stays at its default (`True`) — recorded as a decision.

No new dependency. `graphviz` is needed only if we take up inheritance diagrams (Q2).

---

## 7. The gate

Documentation that is not enforced regresses. Two checks, both cheap:

**G1 — build clean under `-W`.** Already configured in `doc/Makefile`; currently failing
on F1's four warnings. This becomes true and stays true.

**G2 — coverage check.** `scripts/check-sv-doc-coverage.py`, modelled on the extension's
`scripts/check-docs-coverage.py`, run in CI:

- builds the index over the same build units as `conf.py`;
- restricts to objects whose location is under `src/hdl_if/share/`, minus tier B;
- **fails** if any such object lacks a doc comment, or is absent from the built
  `objects.inv`.

The tier-B exclusion list lives in one place and each entry carries a reason. That makes
"we deliberately do not document this" a reviewable statement rather than an absence.

Threshold handling: start with the check reporting a count and failing only on
*regression* against a committed baseline number, then flip to absolute zero when Phase 3
completes. That keeps CI green through the work without letting new gaps in.

---

## 8. Phases

Each phase leaves the tree buildable. Phase 0 must go first; 1–3 can overlap.

### Phase 0 — Unblock (upstream + this repo)

| ID | Item | Acceptance |
|---|---|---|
| S0-1 | Fix literal-block handling in the doxygen docparse (F1), upstream | `py_iter` renders a code block; the four warnings are gone |
| S0-2 | Decide and document what markup a doc comment may contain — literal blocks, inline code, lists (F1) | `docs/usage/doxygen-style.md` states it; `documentation-plan.md` §5.1 points at it |
| S0-3 | Release the fix and raise the CI floor for `sphinx-systemverilog` | CI builds against a version that has it |
| S0-4 | `make html` exits 0 under `-W` | G1 met |

### Phase 1 — Scope: publish the right things

| ID | Item | Acceptance |
|---|---|---|
| S1-1 | Exclude `pyhdl_uvm_apis.svh` from the UVM reference (F2a) | the 64 generated classes leave `objects.inv`; nothing hand-written leaves with them |
| S1-2 | Exclude `pyhdl_dpi_imports.svh` explicitly, with a reason (F3) | tier B is a list with reasons, not an accident |
| S1-3 | Add `sv_ignore_macro_content` incl. `pyhdl_uvm_type_utils` (F5) | `*_w` classes and `uvm_*_utils` members gone; each affected class carries the extension's "hidden members" note |
| S1-4 | Restructure `sv_uvm_api.rst` into `:files:`-scoped sections per §5 | every hand-written `pyhdl_uvm` class appears exactly once |
| S1-5 | Extend `sv_api.rst` to the call-interface classes and package functions (§2.3, ~70 objects) | `ICallApi`, `TaskCallClosure`, `PyHdlDpiTimeCB`, `CallEmptyBase` published |
| S1-6 | Publish the macro layer — `autosvsummary :kinds: macro`, guards excluded (F5, closes D4-7) | 7 macros published |
| S1-7 | Write a short page explaining the generated `*_exp_if`/`*_imp_impl` pattern (F2c) | the excluded layer is explained, not merely missing |

### Phase 2 — Fix the TLM layer, then document it

| ID | Item | Acceptance |
|---|---|---|
| S2-1 | Fix F19: thread `state` through all six `invokeTask` implementations; release the GIL around blocking waits | all five FIFO modules compile against `ICallApi` |
| S2-2 | Add them as build units (`conf.py:103-106`, plus the three top-level and two VPI modules) | they appear in the index with no new parser diagnostics |
| S2-3 | Write `reference/sv_tlm.rst` with `autosvmodule :members:` | every port and parameter of all five modules is published |
| S2-4 | Document ports/parameters that lack comments | no bare port entries |
| S2-5 | Write `guides/tlm.rst` (closes D5-7) | a user can wire up a FIFO from this page |

### Phase 3 — Write the missing doc comments

Ordered by what a user hits first. 335 undocumented objects in tier A, per §2.1.

| ID | Item | Objects | Acceptance |
|---|---|---:|---|
| S3-1 | `pyhdl_if.sv` package level, `pyhdl_if_call_api.svh`, `pyhdl_if_icall_api.svh`, `pyhdl_if_taskcall_closure.svh`, `pyhdl_if_time_cb.svh` | ~70 | 100% |
| S3-2 | Finish `py_dict` (33%), `py_utils` (52%), `py_list` (62%), `py_tuple` (71%), `py_object` (83%) | 31 | 100% |
| S3-3 | The registries — `object_rgy`, `type_rgy`, `enum_rgy`, `wrapper_factory`, `object_type` | ~90 | 100% |
| S3-4 | The containers — `object_list`, `object_map`, `object_string` | ~60 | 100% |
| S3-5 | The register model — `reg`, `reg_block`, `reg_field` | 34 | 100% |
| S3-6 | `pyhdl_uvm_component`, `pyhdl_uvm_phase`, `pyhdl_uvm_pygen`, `cmdline_processor`, `object_if` | ~45 | 100% |
| S3-7 | Finish `pyhdl_uvm_analysis_port` (63%) | 13 | 100% |
| S3-8 | Document the 7 published macros | 7 | 100% |
| S3-9 | Resolve `py_builtins.svh` — finish or delete (F6) | 3 | decided, not deferred |

Carry forward Phase 4's convention: **stubs are documented as stubs**, with an explicit
`@warning`. Eleven such methods are already marked; S3-3…S3-6 will find more.

### Phase 4 — Enforce

| ID | Item | Acceptance |
|---|---|---|
| S4-1 | Write `scripts/check-sv-doc-coverage.py` (§7 G2) | runs locally; reports the current gap |
| S4-2 | Add it to CI in regression mode with a committed baseline | a new undocumented object fails the PR |
| S4-3 | Flip to absolute zero once Phase 3 lands | tier A is 100% |
| S4-4 | Record the tier rules and doc-comment conventions where contributors will read them | closes D6-6 for the SV half |

### Phase 5 — Optional, pending Q2/Q3

| ID | Item |
|---|---|
| S5-1 | `:show-inheritance:` on the `pyhdl_uvm` object hierarchy (needs `dot` in CI) |
| S5-2 | A worked-example page using `sv:uvm-tree` / `sv:uvm-config` on `examples/uvm/component_proxy_smoke` |
| S5-3 | Teach `api-gen-sv` to emit doc comments from Python docstrings (F2b) |

---

## 9. Effort

| Phase | Rough size |
|---|---|
| 0 — unblock (mostly upstream) | 0.5–1 day |
| 1 — scope | 1 day |
| 2 — TLM fix + docs | 2–3 days (S2-1 is the unknown) |
| 3 — write ~335 doc comments | 4–6 days |
| 4 — enforce | 0.5 day |
| 5 — optional | 1–3 days |

Phase 1 alone is the largest visible improvement per hour spent: it halves the published
object count and everything left is real API.

---

## 10. Open questions for review

**Q1 — Fix F19 in this effort, or route around it?** Recommendation: fix it. It is a
real deadlock risk, not only a doc blocker, and the TLM modules are the most
documentation-worthy surface we have.

**Q2 — Inheritance diagrams?** They suit `pyhdl_uvm`'s wrapper hierarchy well, but they
add `graphviz` to the CI doc job. Recommendation: yes, but as Phase 5.

**Q3 — Do we document an example testbench?** The extension's UVM directives
(`sv:uvm-tree`, `sv:uvm-config`, `sv:uvm-schematic`) need a testbench, and
`examples/uvm/component_proxy_smoke` is one. This would make the docs demonstrate the
integration rather than describe it — and would dogfood those directives against real
code. It is also net-new scope. Recommendation: Phase 5, after the reference is complete.

**Q4 — F2: exclude the generated layer, or generate its doc comments?** Recommendation as
in F2: exclude now, generate later. Worth an explicit decision because (b) changes the
`api-gen-sv` output format and therefore the checked-in `pyhdl_uvm_apis.svh`.

**Q5 — Coverage gate strictness.** 100% of tier A is the stated target. The alternative
is "100% of classes, modules, macros and public methods; private/local members exempt".
Recommendation: the strict form — tier B already carries everything we genuinely do not
want to describe, and an exemption category tends to grow.

---

## 11. As-built — Phases 0 and 1 (2026-09-14)

Review decisions taken: **Q1** fix F19, **Q4** exclude the generated layer now and
generate its doc comments later, **Q2** inheritance diagrams in scope, **Q3** the example
testbench page deferred.

### 11.1 Phase 0 — two upstream bugs, not one

**F1 (literal blocks) — fixed.** The cause was in `sanitize.py`: `_render_block` folds
over-indented lines into the line above and dedents each block to its own minimum. Both
are right for prose and fatal for code, so a `::` block was joined into one paragraph and
left unindented, and docutils then reported `Literal block expected; none found` with no
symbol or file to point at.

The fix is a `literal_line_mask()` that marks the lines belonging to a `::`-introduced
block; `strip_rules`, `unwrap_continuations` and the inline escaper all skip them, so a
code sample is passed through exactly as typed. A second defect surfaced while testing:
when a comment's *first* paragraph is the one ending in `::`, summary extraction takes it
and orphans the block, so `reintroduce_literal_block()` puts RST's bare `::` marker back
at the head of the body. Doxygen needed the mask computed before inline conversion (it
escapes line-by-line, ahead of `sanitize_prose`); `plain` needed its escaping done over
whole text rather than per line, or the mask could never see a block at all.

**Not a regression from the 0.6.0 update** — v0.5.0 produces the same four warnings.

**F1b (macro names) — found and fixed.** Publishing the macro layer immediately exposed a
second bug: `_signature_name()` had no `macro` branch, so a signature
`` `define PYHDL_IF_DEBUG(x) `` resolved to the name `` `define ``. Every macro in a
project collided on one anchor and one inventory entry, and a page built with
`:kinds: macro` published exactly one of them. This had survived because the extension's
own docs *show* the directive in a code block without ever running it; that page now
renders the macro fixture, so the path is dogfooded.

**F1c (macro-generated classes) — found and fixed.** `sv_ignore_macro_content` filtered
macro-generated *members* but not the top-level objects `autosvsummary` selects. A
registration macro that emits a whole class therefore left 11 identical `*_w` wrappers on
the page while hiding the members that would have explained them. `autosvsummary` now
applies the same list, with an exact-name glob still winning.

19 + 11 + 3 new tests; the suite is at **804 passed** (was 768). `make html` in this repo
exits **0** under `-W` for the first time, and the extension's own doc set still builds
clean.

### 11.2 Phase 1 — measured effect

| | Before | After |
|---|---:|---:|
| `sv:` objects published | 270 | **242** |
| ...on `sv_api.html` | 50 | **91** |
| ...on `uvm.html` | 220 | **151** |
| Classes | 114 | **49** |
| Generated transport classes (`*_exp_if`/`*_imp_impl`/…) | 60 | **0** |
| Macro-generated `*_w` wrapper classes | 11 | **0** |
| Macros | 0 | **8** |

Every class now published is hand-written API. The 41 added objects on `sv_api.html` are
S1-5 and S1-6: `ICallApi`, `TaskCallClosure`, `PyHdlDpiTimeCB`, `CallEmptyBase`,
`CallEmptyUvmBase`, `PyHdlPiRunnable`, the `pyhdl_if_call_api` functions, the runtime
entry points, and the `PYHDL_IF_*` macro layer — none of which had ever appeared.

Both reference pages are now scoped by `:files:` rather than by symbol lists, which is
what makes §7's coverage gate meaningful: a file in no section is a detectable hole.

Two incidental fixes: `sv_api.rst`'s new headings were renormalized to the page's `-`/`~`
levels (a `=` section produced a level-2→4 skip), and `suppress_warnings =
['misc.highlighting_failure']` was added to `conf.py` — Pygments' SystemVerilog lexer
cannot tokenize `pyhdl_if.sv` (it stops on the string in `import "DPI-C"`), and viewcode
highlights whole files. Sphinx recovers in relaxed mode; only the warning, fatal under
`-W`, needed suppressing.

### 11.3 What this does not yet fix

Doc-comment coverage is **unchanged at 11%** — Phase 1 moved what is published, not what
is described. The thin entries are now concentrated in files that are genuinely ours,
which is what Phase 3 addresses.

CI still installs `sphinx-systemverilog` from PyPI, so the published build stays red until
0.6.1 ships. Phases 0 and 1 are both uncommitted.

### 11.4 Phase 2 — F19 fixed, the TLM layer published

**S2-1.** All six `Closure::invokeTask` implementations now take `ICallApi`'s
`inout PyGILState_STATE state` and release the GIL across their blocking transfer:

```systemverilog
// `get` blocks until the producer supplies a word, which can be any number of
// clocks away.  Holding the GIL across that stalls every Python thread --
// including the one that would drive the producer -- so release it for the wait.
PyGILState_Release(state);
get(tmp[Twidth-1:0]);
state = PyGILState_Ensure();
```

Before/after, measured through pyslang on the two DPI interfaces: **2 elaboration
diagnostics → 0**.

Worth recording *why this survived*: **Verilator lints the broken code clean.**
`verilator --lint-only` accepts the three-argument `invokeTask` against the four-argument
`ICallApi` without complaint, both before and after the fix. The project's own toolchain
could not have caught this; the doc build is what found it.

**S2-2/3/4.** The three distinct interfaces are parsed and published on a new
`sv_tlm.rst`: **29 objects** — 3 interfaces, 8 parameters, 18 ports — none of which had
ever appeared. Ports and parameters are shown whether or not they carry comments, which
is the right default for a module's public face.

**S2-5.** The guide content lives on the same page rather than in a separate
`guides/tlm.rst`: which interface to choose, how to wire the `valid`/`ready` pair, and
what the GIL release means for a blocking transfer. Splitting guide from reference is
`documentation-plan.md` D5-2/D5-7's job, and doing it here would move the page twice.

One more upstream fix was needed: `autosvmodule` warned `'tlm_hvl2hdl_fifo' is a
interface, not a module`, though the extension's own documentation points at that
directive for modules *and* interfaces. It now accepts `interface` and `program` — an
entity's keyword is a property of the design, not a documentation choice.

### 11.5 Phases 3, 4 and 5 — complete

**Phase 3 was one sixth the size the plan estimated.** §8 budgeted ~335 doc comments
against the *indexed* object count. The number that matters is the *published* one, and
Phase 1's scoping had already removed the bulk: the real backlog was **57**. All 57 are
written; coverage of the published reference is **100%**.

That distinction is worth keeping. "Document everything we parse" would have meant
writing prose for 597 CPython imports and 537 generated transport declarations — work
that makes the reference worse. "Document everything we publish" is the honest target,
and scoping first is what made it small.

**F20 resolved.** Per review, the VPI back-end is not currently relevant, so the
`share/dpi` copies are the ones documented. The duplicate declarations in `share/vpi` and
`share/pyhdl_if_{req,rsp}_fifo.sv` are left in place — removing shipped source is a
project decision, not a documentation one — but they remain a maintenance hazard, and the
F19 fix had to be applied six times because of it.

**Phase 4 went straight to absolute zero.** `scripts/check-sv-doc-coverage.py` checks both
failures a green doc build cannot show:

- a published object carrying no doc comment;
- a tier-A source file matching no `:files:` pattern, and therefore absent from every page.

It found five files in the second category on its first run — the init and DPI-export
plumbing, plus the `pyhdl_uvm` package declaration — all now tier B with a written reason.
Since the backlog was already paid off, the `--baseline` mode in §7 was never needed; the
gate runs at zero in both CI workflows.

**Phase 5.** Inheritance diagrams on `pyhdl_uvm_component_proxy` and `pyhdl_uvm_object`.
`conf.py` gates them on a `have_dot` tag, because `sphinx.ext.graphviz` warns and skips
when `dot` is absent and `-W` would turn that into a failed build. Gating alone would make
a graphviz-less CI image ship diagram-free pages silently, so both workflows install
graphviz and the Forgejo job asserts the diagram is in the output.

### 11.6 Upstream: five fixes, released as 0.6.1

Every one was found by using the extension on this repo rather than by reading it:

| # | Fix | Found by |
|---|---|---|
| 1 | rST literal blocks in doc comments folded and dedented | four code samples rendering as run-on paragraphs |
| 2 | An orphaned literal block when the summary split takes the `::` paragraph | writing tests for #1 |
| 3 | Every `` `define `` indexed under the name `` `define `` | publishing the macro layer (S1-6) |
| 4 | `autosvsummary` ignored `sv_ignore_macro_content` for top-level objects | 11 macro-generated wrapper classes surviving the filter (S1-3) |
| 5 | `autosvmodule` rejected `interface`/`program`, which its own docs promise | documenting the TLM interfaces (S2-3) |
| 6 | A declaration whose keyword comes from a macro loses its doc comment | `pyhdl_if_reqrsp_fifo` reading as undescribed despite having a comment |

Extension suite: **815 passed** (was 768). Its own doc set builds clean under `-W`, and
now renders the macro fixture — the gap that let #3 survive.

### 11.7 Final state

| | Start of this work | Now |
|---|---:|---:|
| `make html` under `-W` | **fails** | **passes** |
| Published `sv:` objects | 270 | 271 |
| ...that are hand-written API | 210 | **271** |
| Generated transport classes published | 60 | 0 |
| Macro-generated wrapper classes published | 11 | 0 |
| Macros published | 0 | 8 |
| TLM interfaces published | 0 | 3 (+8 params, +18 ports) |
| Published objects with no description | 60 | **0** |
| Coverage enforced in CI | no | **yes** |
| Inheritance diagrams | none | 2 |

The object count barely moved; what it contains changed entirely.
