########################
Generated Code Reference
########################

What the generators write, for one record and one interface. The excerpts
are from ``tests/unit/data/spike_records``, which the test suite generates
from ``tests/unit/gen/data/spike.json`` and simulates.

Names starting with ``__`` are internal to the generated code. Functions
marked "GIL held" in comments expect the caller to hold the Python GIL; the
public ones take it themselves.

A record
========

SystemVerilog
-------------

The accessor interface. Code written against it works on a local object and
on a reference to a Python one:

.. literalinclude:: ../../tests/unit/data/spike_records/spike_pkg.sv
   :language: systemverilog
   :start-after: //* Record hdr
   :end-before: /** Record hdr, as a value. */

The value class, when the record was not declared in SV (for a class that
already exists in SV, ``hdr_sv_wrap`` implements ``hdr_if`` around your
object instead):

.. literalinclude:: ../../tests/unit/data/spike_records/spike_pkg.sv
   :language: systemverilog
   :start-after: /** Record hdr, as a value. */
   :end-before: /** Reference to a hdr in Python.

Also generated, for record ``r``:

.. list-table::
   :header-rows: 1

   * - Name
     - Purpose
   * - ``r_py_ref``
     - Reference to a Python ``r``; implements ``r_if``. Call ``dispose()``
       when done.
   * - ``r_sv_adapter``
     - Receives Python's calls on a reference to an SV ``r``.
   * - ``r_to_py(v)`` / ``r_from_py(o)``
     - Copy into a new Python ``r`` / into a new SV ``r``.
   * - ``r_ref_to_py(r_if)`` / ``r_ref_from_py(o)``
     - A Python reference to an SV object / an SV reference to a Python
       object. A reference passed back to its owner arrives as the object.
   * - ``r_copy(v)``
     - Deep copy.
   * - ``r_from_if(r_if)``
     - Snapshot of the current value behind an accessor interface.
   * - ``r_wrap(v)``
     - The accessor interface of a value.
   * - ``list_<T>_t``
     - Typedef for a list field or parameter of element type ``T``.

Python
------

The dataclass (imported instead of generated when it was declared in
Python):

.. literalinclude:: ../../tests/unit/data/spike_records/spike_api.py
   :language: python
   :pyobject: hdr

The reference to an SV object; every property access calls SV:

.. literalinclude:: ../../tests/unit/data/spike_records/spike_api.py
   :language: python
   :pyobject: hdr_sv_ref

An interface
============

SystemVerilog
-------------

.. literalinclude:: ../../tests/unit/data/spike_records/spike_pkg.sv
   :language: systemverilog
   :start-after: //* Interface cb_if
   :end-before: // Receives calls from Python on an SV implementation of cb_if.

Also generated, for interface ``i``: ``i_sv_adapter`` (receives Python's
calls on an SV implementation), ``i_py_proxy`` (calls a Python
implementation; implements ``i``; call ``dispose()`` when done),
``i_to_py(impl)`` and ``i_from_py(obj)``.

Python
------

The Protocol (imported instead of generated when it was declared in Python),
the proxy that calls an SV implementation, and the adapter that lets SV call
a Python one:

.. literalinclude:: ../../tests/unit/data/spike_records/spike_api.py
   :language: python
   :pyobject: cb_if

.. literalinclude:: ../../tests/unit/data/spike_records/spike_api.py
   :language: python
   :pyobject: cb_if_sv_proxy

.. literalinclude:: ../../tests/unit/data/spike_records/spike_api.py
   :language: python
   :pyobject: cb_if_py_adapter

The module ends by registering each interface and building the converters
the classes use:

.. literalinclude:: ../../tests/unit/data/spike_records/spike_api.py
   :language: python
   :start-at: _rt.register_interface(cb_if
