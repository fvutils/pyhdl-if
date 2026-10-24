################################
Records and Interfaces in Python
################################

Use ``gen-from-py`` when the types already exist in Python: packets built by
a Python model, a service an SV testbench should call, a reference
generator.

Declaring
=========

- A ``@dataclass`` is a record. Its fields, from ``dataclasses.fields()``,
  are the record's fields. A dataclass base class becomes the record's base.
- An ``enum.IntEnum`` is an enum.
- A ``typing.Protocol`` is an interface. Its public methods (not starting
  with ``_``), including those of base protocols, are the methods. An
  ``async def`` is a task. A missing return annotation means no result.

.. literalinclude:: ../../tests/unit/data/records_py/pkt_model.py
   :language: python

Type hints
----------

Python's ``int`` has no width, so use the sized hints from :mod:`hdl_if.rt`
where the SV side needs one:

.. list-table::
   :header-rows: 1

   * - Hint
     - SystemVerilog
   * - ``u8``, ``u16``, ``u32``, ``u64``, ``uint(N)``
     - ``bit [N-1:0]``
   * - ``i8``, ``i16``, ``i32``, ``i64``, ``sint(N)``
     - ``byte``, ``shortint``, ``int``, ``longint``, ``bit signed [N-1:0]``
   * - ``int``
     - ``longint``
   * - ``ctypes.c_uint8`` ... ``ctypes.c_int64``
     - as the sized hints
   * - ``bool``
     - ``bit``
   * - ``float`` / ``ctypes.c_float``
     - ``real`` / ``shortreal``
   * - ``str``
     - ``string``
   * - ``bytes``
     - ``byte unsigned [$]`` (``pyhdl_if::pyhdl_if_bytes_t``)
   * - ``List[T]`` / ``list[T]``
     - a queue of ``T`` (typedef ``list_<T>_t``)
   * - ``Optional[T]``
     - ``T`` (a record may be ``None``/``null``)
   * - a dataclass, an ``IntEnum``
     - the generated class or enum
   * - ``Ref[dataclass]`` (parameters and results)
     - ``<rec>_if``: a reference, not a copy
   * - a Protocol (parameters and results)
     - the generated interface class

An enum's width is the smallest of 8, 16, 32 or 64 bits that holds its
values. Set ``__pyhdl_width__`` in the class body to choose another.

Generating
==========

.. code-block:: bash

   pyhdl-if gen-from-py -m pkt_model --sv-out pkt_pkg.sv --py-out pkt_api.py

``-m`` names a module to scan (repeatable); ``-P`` adds a directory to the
Python path first. ``-i``/``-e`` take ``fnmatch`` patterns on
``module.Class`` to choose which classes to start from; whatever they use is
always included. The Python module imports your classes rather than
redefining them, and adds the reference, proxy and adapter classes.

In a dfm flow:

.. code-block:: yaml

   - name: gen
     uses: pyhdl-if.GenFromPy
     with:
       pkgname: pkt_pkg
       pymodule: pkt_api
       modules: [pkt_model]
       pythonpath: [.]

Implementing the interface in SV
================================

Implement the generated ``interface class`` and hand the implementation to
Python with ``<iface>_to_py()``:

.. literalinclude:: ../../tests/unit/data/records_py/pkt_tb.sv
   :language: systemverilog
   :end-before: module pkt_tb;

Python calls it like any object; the records arrive in SV as copies:

.. literalinclude:: ../../tests/unit/data/records_py/pkt_drv.py
   :language: python
   :pyobject: run
