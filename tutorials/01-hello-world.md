# Tutorial 1 — Hello World: Your First Python UVM Component

**Series:** PyHDL-IF UVM Tutorial Series  
**Difficulty:** Beginner  
**Time:** ~30 minutes  
**Cross-reference:** ["Unlocking the Combined Strength of UVM and Python"](https://bitsbytesgates.com) (blog, 2025-10-25)

---

## Learning Goals

By the end of this tutorial you will be able to:

- Describe what the PyHDL-IF *component proxy* is and why it exists
- Write a minimal UVM testbench that launches a Python component
- Implement `build_phase`, `connect_phase`, and `run_phase` in Python
- Compile and run the simulation with the DV Flow Manager (`dfm`)
- Use `--log-level=INFO` to inspect every command the tool sends to the simulator

---

## Before You Start

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.9+ | Must be on `PATH` |
| pyhdl-if | latest | `pip install pyhdl-if` or dev install |
| dv-flow-mgr | latest | `pip install dv-flow-mgr` |
| dv-flow-libhdlsim | latest | `pip install dv-flow-libhdlsim` |
| A UVM simulator | — | Xcelium (`xcm`), Questa (`mti`), or VCS (`vcs`) |

> **Using the development environment?** If you cloned this repository and ran
> `ivpm update`, all of the above (plus Verilator for non-UVM examples) is
> already in `packages/`. Source `packages/python/bin/activate` or prefix
> commands with `./packages/python/bin/`.
>
> **GitHub Codespaces:** A one-click Codespaces configuration is provided at
> the repository root. The environment comes pre-configured with all
> dependencies. Click the badge in `README.md` to launch.

### Verify your setup

```bash
python -c "import hdl_if; print(hdl_if.__version__)"
dfm --version
```

Both commands should print version strings without errors.

---

## Concepts

### The Bridge Problem

UVM testbenches are written in SystemVerilog. Python has a richer ecosystem
for data analysis, machine learning, scripting, and test orchestration — but
nothing in the Python standard library knows how to call a UVM `run_phase`.

PyHDL-IF solves this with a *proxy pattern*: a lightweight SystemVerilog class
(`pyhdl_uvm_component_proxy`) acts as a stand-in inside the UVM component
hierarchy. At simulation startup it loads a Python module, instantiates a
user-supplied class, and then delegates every UVM lifecycle callback (phases,
etc.) to that Python object.

### Diagram 1 — The Python / SystemVerilog Bridge

```
┌─────────────────────────────────────────────────────────────┐
│  Simulator process                                          │
│                                                             │
│  ┌──────────────────────────────────────────────┐          │
│  │  UVM world (SystemVerilog)                   │          │
│  │                                              │          │
│  │   uvm_root                                   │          │
│  │     └─ hello_test (uvm_test)                 │          │
│  │          └─ m_pycomp                         │          │
│  │               (pyhdl_uvm_component_proxy)    │          │
│  │                    │                         │          │
│  │                    │  DPI-C / Python C API   │          │
│  │                    ▼                         │          │
│  │         ┌──────────────────────┐             │          │
│  │         │  Python interpreter  │             │          │
│  │         │  (embedded)          │             │          │
│  │         │                      │             │          │
│  │         │  HelloComp instance  │             │          │
│  │         │  (uvm_component_impl)│             │          │
│  │         └──────────────────────┘             │          │
│  └──────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

*The Python interpreter runs **inside** the simulator process. PyHDL-IF
embeds it at elaboration time via the DPI-C Python C API. There is no
separate process or socket.*

### Diagram 2 — UVM Component Hierarchy at Runtime

```
uvm_root  (created by run_test())
  └─ hello_test  [uvm_test]
       └─ m_pycomp  [pyhdl_uvm_component_proxy]
            pyclass = "hello::HelloComp"
```

The proxy is a real UVM component. It appears in `+UVM_OBJECTION_TRACE`,
in `uvm_factory.print()`, and in the component tree just like any other
component. Python is an implementation detail invisible to the rest of the
testbench.

### Diagram 3 — Phase Execution Timeline

```
UVM phase       SV (hello_test)          SV (m_pycomp proxy)      Python (HelloComp)
──────────────  ───────────────────────  ───────────────────────  ─────────────────────
build_phase()   build_phase() ──────────► build_phase():          build_phase():
                  create m_pycomp          import hello module      print("build_phase")
                  set pyclass              instantiate HelloComp
                                           call Python build_phase ─►
                                                                   ◄─ return

connect_phase() connect_phase()          connect_phase():         connect_phase():
                                           call Python ───────────►  print("connect_phase")
                                                                   ◄─ return

run_phase()     raise objection          run_phase():             async run_phase():
                #1 delay                   start asyncio loop       print("Hello, World!")
                drop objection             await Python task ─────►
                                                                   ◄─ coroutine completes
```

Key observations:
- `build_phase` is a SV `function` (no time); Python's `build_phase` is also sync.
- `run_phase` is a SV `task` (may consume time); Python's `run_phase` is `async`.
- The Python interpreter runs on the same thread as the simulator. PyHDL-IF
  uses `asyncio` to co-operatively schedule Python coroutines between simulator
  time steps.

---

## Project Layout

All source files for this tutorial live in `tutorials/01-hello-world/`:

```
tutorials/01-hello-world/
├── flow.yaml       # DV Flow Manager build/run recipe
├── defines.v       # Simulator-specific defines (e.g. `timescale for VCS)
├── top_pkg.sv      # UVM test — creates the component proxy
├── top.sv          # Top-level module — calls run_test()
└── hello.py        # Python component — the code we're writing
```

### Diagram 4 — File Relationships

```
flow.yaml
  │ references
  ├──► defines.v       (included first; simulator-specific)
  ├──► top_pkg.sv      (`include "uvm_macros.svh", imports uvm_pkg & pyhdl_uvm)
  │         imports pyhdl_uvm::*
  │         ──────────────────────────────────────────────────────────
  │         At build_phase runtime:
  │           pyclass = "hello::HelloComp"
  │                        │        └── class name in hello.py
  │                        └────────── Python module file name (hello.py)
  └──► top.sv          (calls run_test())
  
PYTHONPATH set by flow.yaml to include tutorials/01-hello-world/
  └──► hello.py        (imported as module "hello" by the proxy)
```

---

## Step-by-Step

### Step 1 — `defines.v`

A tiny file included before any SystemVerilog. Currently only needed by VCS,
which requires a `` `timescale `` before any module definition.

```verilog
`ifdef VCS
`timescale 1ps/1ps
`endif
```

Nothing to understand here — this is boilerplate that keeps the tutorial
runnable on all supported simulators.

---

### Step 2 — `top.sv`

The simulation top-level module. It has one job: call `run_test()` to hand
control to the UVM test selected by `+UVM_TESTNAME`.

```systemverilog
`include "uvm_macros.svh"

module top;
    import uvm_pkg::*;
    import top_pkg::*;

    initial begin
        run_test();
    end

endmodule
```

This is standard UVM boilerplate. Note the import of `top_pkg::*` — our test
class lives there.

---

### Step 3 — `top_pkg.sv`

This is the heart of the SystemVerilog side. We define a UVM test that:

1. Declares a `pyhdl_uvm_component_proxy` member
2. Creates it via the UVM factory in `build_phase`
3. Sets the `pyclass` string to point at the Python class we want

```systemverilog
`include "uvm_macros.svh"

package top_pkg;
    import uvm_pkg::*;
    import pyhdl_uvm::*;              // (1)

    class hello_test extends uvm_test;
        `uvm_component_utils(hello_test)

        pyhdl_uvm_component_proxy m_pycomp;  // (2)

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            m_pycomp = pyhdl_uvm_component_proxy::type_id::create( // (3)
                "m_pycomp", this);
            m_pycomp.pyclass = "hello::HelloComp";                  // (4)
        endfunction

        task run_phase(uvm_phase phase);
            phase.raise_objection(this);  // (5)
            #1;
            phase.drop_objection(this);
        endtask

    endclass

endpackage
```

Annotations:

**(1)** `import pyhdl_uvm::*` — brings in `pyhdl_uvm_component_proxy` and all
other PyHDL-IF UVM classes. These are provided by the `pyhdl-if` package and
linked in by the `flow.yaml` build recipe.

**(2)** `pyhdl_uvm_component_proxy` is a plain `uvm_component`. Declaring it
as a member is exactly what you would do for any other child component.

**(3)** Factory creation with `type_id::create` makes the proxy overridable
via `uvm_factory` — this is standard UVM style.

**(4)** `pyclass` is the only PyHDL-IF-specific field. The string format is
`"<module>::<ClassName>"` where `<module>` is the Python module filename
(without `.py`) and `<ClassName>` is the class inside that module.

> **Why `"::"` as the separator?** The double-colon mirrors SystemVerilog's
> scope resolution operator, making the string visually consistent with SV
> naming conventions. The proxy parses this string by finding the last `::`.

**(5)** The test's own `run_phase` raises and drops an objection to keep the
simulation alive for at least one time step (`#1`). This gives the Python
`run_phase` coroutine time to execute. The proxy's `run_phase` is also active
concurrently — UVM runs `run_phase` in all active components simultaneously
as forked tasks.

---

### Step 4 — `hello.py`

The Python file. This is the only file you would normally change between
tutorials — the SV scaffolding stays the same.

```python
from hdl_if.uvm import uvm_component_impl   # (1)


class HelloComp(uvm_component_impl):         # (2)

    def build_phase(self, phase):             # (3)
        print("HelloComp: build_phase", flush=True)

    def connect_phase(self, phase):
        print("HelloComp: connect_phase", flush=True)

    async def run_phase(self, phase):         # (4)
        print("Hello, World! from Python inside UVM run_phase",
              flush=True)
```

Annotations:

**(1)** `uvm_component_impl` is a dataclass defined in PyHDL-IF. It provides
the interface your class must implement (all methods have no-op defaults, so
you only override what you need).

**(2)** `HelloComp` is a plain Python class. There are no special decorators
required on the class itself. The name here must match the class name in the
`pyclass` string on the SV side.

**(3)** `build_phase` and `connect_phase` are regular synchronous methods.
The `phase` argument is a wrapped `uvm_phase` object. We don't need it here
(we're not raising objections in Python), but it's always passed.

**(4)** `run_phase` is an **`async` method** (`async def`). This is required
because `run_phase` is a UVM task that may span multiple simulation time steps.
PyHDL-IF runs the Python asyncio event loop inside the simulator's time-step
scheduler. Any Python code that needs to wait for simulation time or other
async events must be in a coroutine.

> **Why `flush=True`?** Python's `print()` buffers output by default. Without
> `flush=True`, messages may not appear in the simulator log until the buffer
> fills or the simulation ends — making them appear out of order. Always use
> `flush=True` in simulation code.

> **Why doesn't Python raise a phase objection?**  
> In this first tutorial, the SV test already holds an objection for `#1` of
> simulation time. That's enough for the Python `run_phase` to execute. In
> later tutorials (starting with Tutorial 2) we'll see how to raise and drop
> objections from Python when the Python code needs to control simulation
> duration directly.

---

### Step 5 — `flow.yaml`

The DV Flow Manager recipe file. This describes the build graph: what files
to compile, in what order, with which simulator.

```yaml
# yaml-language-server: $schema=https://dv-flow.github.io/flow.dv.schema.json
package:
  name: hello_world
  with:
    sim:
      type: str
      value: "vlt"            # default simulator; override with -Dsim=xcm/mti/vcs

  tasks:
  - name: defines
    uses: std.FileSet
    with:
      type: systemVerilogSource
      include: [defines.v]

  - name: src
    uses: std.FileSet
    with:
      type: systemVerilogSource
      include: [top_pkg.sv, top.sv]

  - name: pythonpath
    uses: std.SetEnv
    with:
      prepend_path:
        PYTHONPATH: ${{ srcdir }}   # (1)

  - name: sim-img
    desc: Builds the simulation image
    uses: "hdlsim.${{ sim }}.SimImage"
    needs:
    - defines
    - "hdlsim.${{ sim }}.SimLibUVM"   # (2)
    - pyhdl-if.UVMPkg                 # (3)
    - src
    with:
      top: [top]

  - name: sim-run
    uses: "hdlsim.${{ sim }}.SimRun"
    needs: [pythonpath, sim-img, pyhdl-if.DpiLib]  # (4)
    with:
      plusargs:
      - UVM_TESTNAME=hello_test
      - pyhdl.debug=0
```

Annotations:

**(1)** `PYTHONPATH: ${{ srcdir }}` adds the directory containing `hello.py`
to the Python module search path so that `import hello` works at runtime.
`${{ srcdir }}` is a DFM variable that expands to the directory containing
this `flow.yaml`.

**(2)** `hdlsim.${{ sim }}.SimLibUVM` is a DFM task provided by
`dv-flow-libhdlsim` that compiles the UVM library for the chosen simulator.

**(3)** `pyhdl-if.UVMPkg` is a DFM task provided by `pyhdl-if` that compiles
the PyHDL-IF UVM package (`pyhdl_uvm`, including `pyhdl_uvm_component_proxy`).
It depends on UVM being compiled first.

**(4)** `pyhdl-if.DpiLib` provides the pre-built DPI-C shared library
(`.so` / `.dll`) that embeds the Python interpreter inside the simulator.

---

## Running the Simulation

Navigate to the example directory and run:

```bash
cd tutorials/01-hello-world
dfm run -Dsim=xcm sim-run          # Cadence Xcelium
# dfm run -Dsim=mti sim-run        # Siemens Questa
# dfm run -Dsim=vcs sim-run        # Synopsys VCS
```

### Expected output

```
UVM_INFO @ 0: reporter [RNTST] Running test hello_test...
HelloComp: build_phase
HelloComp: connect_phase
Hello, World! from Python inside UVM run_phase
UVM_INFO @ 1: reporter [TEST_DONE] UVM-provided test sequence...
--- UVM Report Summary ---
```

The Python messages appear interleaved with UVM's own logging, at the
correct phase boundaries.

### Inspecting the simulator commands

To see every command `dfm` sends to the simulator:

```bash
dfm --log-level=INFO run -Dsim=xcm sim-run
```

You will see lines like:

```
INFO  hdlsim.xcm  xmvlog -sv -uvm ... pyhdl_uvm_pkg.sv top_pkg.sv top.sv
INFO  hdlsim.xcm  xmelab -access +r top ...
INFO  hdlsim.xcm  xmsim top +UVM_TESTNAME=hello_test ...
```

This is useful for debugging compilation errors, checking flag ordering, and
understanding what DFM abstracts away.

### Output location

Build artifacts and the simulation log are in `rundir/`:

```
rundir/
├── hello_world.sim-img/
│   └── ...            # compiled simulation image
└── hello_world.sim-run/
    └── sim.log        # full simulation output
```

---

## Understanding What Happened

Let's trace the execution path step by step:

1. **`dfm run sim-run`** compiles `defines.v`, the UVM library, the PyHDL-IF
   UVM package, and `top_pkg.sv + top.sv` into a simulation image. It then
   launches the simulator with `+UVM_TESTNAME=hello_test`.

2. **Elaboration:** The simulator builds `module top`. The `initial` block
   calls `run_test("hello_test")`.

3. **`build_phase` (SV):** UVM calls `hello_test::build_phase`. The test
   creates `m_pycomp` via the factory. The proxy's own `build_phase` fires:
   it parses `"hello::HelloComp"`, imports the Python module `hello`, finds
   class `HelloComp`, and instantiates it. It then calls
   `HelloComp.build_phase(phase)` → *"HelloComp: build_phase"* prints.

4. **`connect_phase` (SV):** The proxy delegates to `HelloComp.connect_phase`
   → *"HelloComp: connect_phase"* prints.

5. **`run_phase` (SV):** The proxy starts the asyncio event loop (if not
   already running), then `await`s the Python coroutine
   `HelloComp.run_phase(phase)`. Concurrently, `hello_test::run_phase` raises
   an objection and delays `#1`. The Python coroutine runs to completion →
   *"Hello, World! ..."* prints. When the test drops its objection, UVM ends
   `run_phase`.

6. **End of simulation:** UVM runs `report_phase` and prints the summary.

---

## Exercises

Try these variations to deepen your understanding:

### Exercise 1 — Add `start_of_simulation_phase`

`uvm_component_impl` also supports `start_of_simulation_phase`. Override it
in `HelloComp`:

```python
def start_of_simulation_phase(self, phase):
    print("HelloComp: start_of_simulation_phase", flush=True)
```

Run the simulation. Where does the new message appear relative to
`connect_phase` and `run_phase`?

### Exercise 2 — Print the component's full name

Inside `build_phase`, use `self.proxy.get_full_name()` to print the full
hierarchical path of the Python component:

```python
def build_phase(self, phase):
    print(f"HelloComp: full name = {self.proxy.get_full_name()}", flush=True)
```

What path does it print? How does this relate to the UVM component hierarchy
shown in Diagram 2?

### Exercise 3 — Multiple Python components

Modify `top_pkg.sv` to create a second proxy:

```systemverilog
pyhdl_uvm_component_proxy m_pycomp2;
// in build_phase:
m_pycomp2 = pyhdl_uvm_component_proxy::type_id::create("m_pycomp2", this);
m_pycomp2.pyclass = "hello::HelloComp";
```

Both proxies will point at the same Python class. Run the simulation.
What do you observe about the order of phase callbacks? Does each get its own
Python object instance?

### Exercise 4 — Inspect the simulator commands

Run with `--log-level=INFO` and find:
- The flag that links in the PyHDL-IF DPI-C shared library
- The `+UVM_TESTNAME` plusarg being passed to the simulator
- How many separate compilation invocations `dfm` issues

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `uvm_fatal: No value specified for 'pyclass'` | `pyclass` not set before `build_phase` ends | Set it in `build_phase` before `super.build_phase()` returns — or set it after `create`, as shown |
| `uvm_fatal: Failed to load Python module hello` | `PYTHONPATH` doesn't include `hello.py`'s directory | Check the `pythonpath` task in `flow.yaml`; verify `srcdir` resolves correctly |
| `uvm_fatal: Failed to find class HelloComp` | Class name mismatch | The class name in `pyclass` must exactly match the Python class name |
| `Hello` message never appears | `run_phase` coroutine not completing | Make sure `hello_test` keeps an objection alive long enough; the `#1` delay should suffice |
| Python print output appears at end of simulation | Buffering | Add `flush=True` to all `print()` calls |

---

## Key Takeaways

- **`pyhdl_uvm_component_proxy`** is a standard UVM component that delegates
  lifecycle callbacks to a Python class you specify via the `pyclass` field
  (`"module::ClassName"`).
- **`uvm_component_impl`** is the Python base class. Override only the phases
  you need; the rest are no-ops.
- **`run_phase` must be `async def`** because it is a UVM task. Synchronous
  phases (`build_phase`, `connect_phase`) are plain `def`.
- **`dfm`** abstracts simulator differences. Use `--log-level=INFO` to see
  exactly what it does.
- The Python interpreter is **embedded in the simulator process** — no separate
  process, no sockets, no co-simulation overhead beyond Python function call
  cost.

---

## Code Files Summary

All files for this tutorial are in `tutorials/01-hello-world/`:

| File | Purpose |
|---|---|
| `defines.v` | Simulator-compatibility defines (`timescale` for VCS) |
| `top_pkg.sv` | UVM test; creates `pyhdl_uvm_component_proxy`, sets `pyclass` |
| `top.sv` | Simulation top module; calls `run_test()` |
| `hello.py` | Python UVM component; implements `build_phase`, `connect_phase`, `run_phase` |
| `flow.yaml` | DFM build/run recipe; sets `PYTHONPATH`, links UVM and PyHDL-IF |

---

## Diagrams Summary

The following diagrams should be produced for the final tutorial:

| # | Title | Type | Key elements |
|---|---|---|---|
| 1 | Python / SystemVerilog bridge architecture | Block diagram | Simulator process boundary; UVM component tree; DPI-C bridge; embedded Python interpreter |
| 2 | UVM component hierarchy at runtime | Hierarchy tree | `uvm_root → hello_test → m_pycomp (proxy)`; annotation showing `pyclass` field |
| 3 | Phase execution timeline | Sequence / swim-lane | Three lanes: `hello_test`, `m_pycomp proxy`, `HelloComp (Python)`; arrows for phase calls and Python callbacks; async indicator on `run_phase` |
| 4 | File relationships | Dependency diagram | `flow.yaml` as root; arrows to each `.sv` / `.py` file; annotation showing how `pyclass` string links SV to Python; `PYTHONPATH` arrow |

*Recommended format: SVG or PNG generated from a diagram-as-code tool
(e.g., Mermaid, Excalidraw, or draw.io) so diagrams can be version-controlled
and updated alongside the code.*

---

## What's Next

**Tutorial 2 — Implementing Component and Sequence Phase Methods**

In this tutorial we used only `run_phase` in Python. Tutorial 2 introduces
the full UVM phase sequence, adds a *sequence proxy* alongside the component
proxy, and shows how the Python component can raise and drop phase objections
itself — giving Python full control over when the simulation advances and ends.
