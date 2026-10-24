######################
Records and Interfaces
######################

Records and interfaces let SystemVerilog and Python share data and objects
with no DPI code and nothing for you to compile. You declare the types once,
in whichever language already has them, and a generator writes both halves:
an SV package and a Python module. Both call only the PyHDL-IF runtime, so
the generated files are ordinary source that you check in and read.

Two kinds of thing are shared:

- A **record** is data: a value type with ordered fields. It is an SV class
  and a Python dataclass. A record can be *copied* across, or the other side
  can hold a *reference* to it.
- An **interface** is a set of functions and tasks. It is an SV ``interface
  class`` and a Python ``typing.Protocol``. Either side can implement it;
  the other side calls it.

Where a type is declared only picks the generator's front end. It does not
decide which side implements an interface or which way data flows.

.. list-table::
   :header-rows: 1

   * - You have it in
     - Records
     - Interfaces
     - Command
   * - Python
     - ``@dataclass``
     - ``typing.Protocol`` (``async def`` is a task)
     - ``pyhdl-if gen-from-py`` (:doc:`records_from_py`)
   * - SystemVerilog
     - ``class`` data members
     - ``interface class``
     - ``pyhdl-if gen-from-sv`` (:doc:`records_from_sv`)
   * - Neither
     - JSON spec
     - JSON spec
     - ``pyhdl-if gen-from-spec`` (:doc:`records_from_spec`)

Enums go both ways too: an SV ``typedef enum`` and a Python ``enum.IntEnum``.

How it fits together
====================

1. Declare the types.
2. Generate: ``pyhdl-if gen-from-... --sv-out my_pkg.sv --py-out my_api.py``.
3. Check both files in. Run the same command with ``--check`` in CI: it
   writes nothing and fails, with a diff, when the files are stale.
4. Compile the SV package after ``pyhdl_if`` (and after any SV sources it
   mirrors), and put the Python module on ``PYTHONPATH``.

The ``pyhdl-if.GenFromPy``, ``GenFromSpec`` and ``GenFromSv`` dfm tasks run
the same generators inside a flow, for designs that generate at build time.
Each produces the SV package as a ``systemVerilogSource`` FileSet and a
``std.Env`` that puts the Python module on ``PYTHONPATH`` for the simulation.

Copy or reference
=================

A copy is a snapshot; a reference is a live view of the object on the other
side. The two languages differ in what that looks like:

- **Python** can intercept attribute access, so a copy and a reference look
  the same: ``p.ttl`` works on both.
- **SystemVerilog** cannot. A copy has plain fields (``p.ttl``); a reference
  goes through accessor methods (``p.get_ttl()``, ``p.set_ttl(v)``).

So each record ``pkt`` also gets an accessor interface class, ``pkt_if``. The
SV value class ``pkt`` implements it, and so does ``pkt_py_ref``, the SV
reference to a Python ``pkt``. Code written against ``pkt_if`` works on both:

.. literalinclude:: ../../tests/unit/data/spike_records/spike_tb.sv
   :language: systemverilog
   :start-after: // The same code works on a local pkt and on a reference to a Python pkt
   :end-before: task automatic test_copy

.. list-table:: What is generated for record ``pkt``
   :header-rows: 1

   * -
     - SystemVerilog
     - Python
   * - Value (copy)
     - ``class pkt`` with plain fields
     - ``@dataclass pkt``
   * - Accessors
     - ``interface class pkt_if`` (``get_*``, ``set_*``, ``dispose()``)
     - the dataclass's attributes
   * - Reference to the other side's object
     - ``pkt_py_ref`` (implements ``pkt_if``)
     - ``pkt_sv_ref`` (one property per field)
   * - Crossing
     - ``pkt_to_py()``, ``pkt_from_py()`` copy;
       ``pkt_ref_to_py()``, ``pkt_ref_from_py()`` reference
     - automatic, by type hint

In a method signature, a record type means a copy and a reference type means
a reference: ``pkt`` / ``pkt_if`` in SV, ``pkt`` / ``Ref[pkt]`` in Python
(:data:`hdl_if.rt.Ref`).

Rules:

- **Nested records.** Through a reference, ``get_hdr()`` returns a reference
  too (``hdr_if`` in SV, ``hdr_sv_ref`` in Python); a copy copies all the way
  down.
- **Lists through a reference.** Reading a list or byte field through a
  reference returns a copy of it; writing replaces it. Setting a nested
  record field through a reference copies the value in.
- **Mutation.** Changing a field of a copy does not change the source. Both
  forms have ``copy()`` for an explicit snapshot: ``r.copy()`` on a
  ``pkt_sv_ref``, ``pkt_copy(v)`` and ``pkt_from_if(r)`` in SV,
  :func:`hdl_if.rt.copy` for any record in Python.
- **Identity.** A reference passed back to the side that owns the object
  arrives as the object itself, not as a reference to a reference.

Interfaces: who implements
==========================

For interface ``svc``, either side can implement it; the other side calls it
through a generated proxy:

.. list-table::
   :header-rows: 1

   * -
     - SystemVerilog
     - Python
   * - The interface
     - ``interface class svc`` (with ``dispose()``)
     - ``class svc(Protocol)``
   * - Calls the other side's implementation
     - ``svc_py_proxy`` (implements ``svc``)
     - ``svc_sv_proxy``
   * - Lets the other side call this side's implementation
     - ``svc_sv_adapter``
     - ``svc_py_adapter``

You rarely name the proxies and adapters. In SV, ``svc_to_py(impl)`` hands a
local implementation to Python, and ``svc_from_py(obj)`` turns a Python
implementation into an ``svc`` handle. In Python, a value passed where the
type hint is ``svc`` is wrapped automatically. Interface-typed parameters
are how callbacks work: pass an implementation of a second interface the
other way.

Functions must return without consuming time; tasks may. A Python task is an
``async def``; an SV task's result is its leading ``output`` argument.

Lifetime and ``dispose()``
==========================

A reference keeps its target alive.

- **Python** releases a reference when its last Python reference goes away
  (CPython's reference counting makes that immediate, except in reference
  cycles). The release is only queued; the SV runtime frees the slot the next
  time it needs one. Nothing calls into SV from a finalizer, so it is safe
  after the simulation ends and during interpreter shutdown.
- **SystemVerilog** has no finalizers, so every generated interface class has
  ``dispose()``. On a reference or proxy it releases the Python object; on a
  local object it does nothing, so code written against ``pkt_if`` can always
  call it. A second ``dispose()`` does nothing; any other use afterwards is a
  runtime error.

A reference that an SV method receives is the method's to ``dispose()`` when
it is done with it. The generated code never disposes arguments, because a
method may keep one (a callback, say). Not disposing only costs memory.

Errors
======

A Python exception raised in code called from SV prints its traceback and
is reported by ``pyhdl_if::pyhdl_if_rt_error()``, which counts it in
``pyhdl_if::pyhdl_if_rt_errors`` and ends the simulation. Clear
``pyhdl_if::pyhdl_if_rt_error_fatal`` to keep running and count instead. A
Python task that raises delivers no result rather than hanging the caller.

Choosing copy or reference
==========================

A copy pays once, up front; a reference pays a crossing on every field
access. Measured on Verilator (``tests/unit/test_spike_records.py`` prints
these on every run; a record of 10 fields):

.. list-table::
   :header-rows: 1

   * - Operation
     - µs
   * - Copy a record SV→Python / Python→SV, no byte payload
     - 3.5 / 3
   * - Copy a record SV→Python / Python→SV, 1500-byte payload
     - 27 / 26
   * - SV reads one field of a Python object through a reference
     - 0.08
   * - Python reads one field of an SV object through a reference
     - 1.6
   * - SV calls a Python function (two ints)
     - 0.5
   * - Python calls an SV function (two ints)
     - 1.5
   * - SV calls a Python task, record copied in and out
     - 22

Pass a copy when the receiver reads most fields, or keeps the value; pass a
reference when it reads a few fields of a large object, or must modify the
original. Task calls cost more than either: most of that is scheduling
between the two event loops.

Generated code and versions
===========================

Generated files are never edited by hand: put behavior in a class that
implements an interface, or in code that uses the records. Each file records
the runtime API version it targets and checks it when loaded (the SV package
at package initialization, the Python module at import). A file generated
for a newer PyHDL-IF asks you to upgrade; one the installed PyHDL-IF no
longer supports asks you to regenerate it. The policy is in
``doc/design/neutral_api_and_records.md``.

How this relates to ``@api`` and ``ctypes`` structs
===================================================

``@api``/``@imp``/``@exp`` (:doc:`sv_api`) and ``ctypes.Structure`` arguments
(:doc:`structs`) remain supported. They fix, per method, which side
implements it, and they pass flat structs by value. Records and interfaces
are the more general form: the implementer is chosen when you bind,
records nest and can be referenced, and declarations can start in SV. Use
them for new code.

.. toctree::
   :maxdepth: 1

   records_from_py
   records_from_sv
   records_from_spec
   records_generated
