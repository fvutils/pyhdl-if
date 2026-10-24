#######################################
Records and Interfaces in SystemVerilog
#######################################

Use ``gen-from-sv`` when the types already exist in SystemVerilog: a
``uvm_sequence_item`` a monitor produces, an ``interface class`` an
environment exposes. The generator reads your sources with pyslang
(``pip install pyhdl-if[sv]``) and writes *companions* for your classes; it
never regenerates or modifies them.

Declaring
=========

Nothing in the SV code needs to change:

.. literalinclude:: ../../tests/unit/data/records_uvm/pkt_item_pkg.sv
   :language: systemverilog

- A class is a record. Its fields are its public data members that are not
  ``static`` or ``const`` (``--sv-fields=rand``: only ``rand``/``randc``
  ones). ``local`` and ``protected`` members are never mirrored, because
  code outside the class cannot reach them.
- An ``interface class`` is an interface. Its pure virtual methods,
  including those of interface classes it extends, are the methods. A task's
  leading ``output`` argument is its result; other arguments must be
  ``input``.
- A ``typedef enum`` is an enum.

Base classes: the walk up ``extends`` stops at any class in ``uvm_pkg``, so
UVM's own fields are not mirrored. Other base classes become records too.
``--stop-at PATTERN`` stops at more classes, ``--skip-base PATTERN`` passes
over one (dropping its fields), and ``--no-default-stops`` clears the
``uvm_pkg`` default.

A record class must be constructible with ``new()``: not ``virtual``, and
every constructor argument defaulted (as UVM's ``name`` is).

Type mapping
------------

Integral types keep their width and signedness (``logic`` is read as
two-state; a single unsigned bit is a ``bool``). ``real``/``shortreal``,
``string``, enum typedefs, class handles (records) and interface class
handles map as you would expect. Queues and dynamic and fixed-size arrays
map to lists; arrays of 8-bit elements (``byte``, ``byte unsigned``,
``bit [7:0]``) map to Python ``bytes``. Not supported yet: packed structs and
unions, associative arrays, arrays of arrays, parameterized classes and
anonymous enums. ``--skip-unsupported`` skips such fields with a warning
instead of failing; ``--field-exclude`` names fields to leave out.

A class-typed method parameter is a copy. Your existing ``interface class``
cannot name the generated accessor interface, so references are passed from
SV code explicitly (below).

Generating
==========

.. code-block:: bash

   pyhdl-if gen-from-sv -f files.f -I $UVM_HOME/src $UVM_HOME/src/uvm_pkg.sv \
       -i 'pkt_item_pkg::*' --sv-out pkt_gen_pkg.sv --py-out pkt_gen_api.py

Sources use slang's syntax: files, ``-f`` file lists, ``-I``/``+incdir+``,
``-D``/``+define+``. ``-i``/``-e`` take ``fnmatch`` patterns on ``pkg::name``
to choose which definitions to start from (by default, every class,
interface class and enum typedef outside ``std``, ``uvm_pkg`` and
``pyhdl_if``). Field and method filters take ``pkg::Class.field`` and
``pkg::Iface.method`` patterns.

In a dfm flow, ``pyhdl-if.GenFromSv`` reads the SV FileSets it needs, for
example UVM's from ``SimLibUVM`` and yours. Compile the generated package
after your sources.

Using it
========

A Python implementation of your ``interface class``, from SV:

.. literalinclude:: ../../tests/unit/data/records_uvm/uvm_rec_tb.sv
   :language: systemverilog
   :start-after: // A copy, through the SV interface class implemented in Python
   :end-before: state = pyhdl_if::PyGILState_Ensure();

``<rec>_wrap(obj)`` gives the accessor interface of one of your objects, and
``<rec>_ref_to_py()`` hands Python a reference to it. Python code that reads
fields works on a copy and on a reference alike:

.. literalinclude:: ../../tests/unit/data/records_uvm/uvm_rec_drv.py
   :language: python
   :pyobject: sample

.. note::

   PyHDL-IF integrates with Verilator through DPI, so it does not need
   ``--vpi``. ``hdlsim.vlt.SimLibUVM`` builds without it by default: UVM's
   DPI layer is used (regular expressions, ``+UVM_*`` plusargs) without the
   ``uvm_hdl_*`` register backdoor. Its ``backdoor: true`` option adds the
   backdoor and ``--vpi``; PyHDL-IF still starts through DPI.
