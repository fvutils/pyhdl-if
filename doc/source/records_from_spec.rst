#####################################
Records and Interfaces from a Spec
#####################################

Use ``gen-from-spec`` when neither language owns the types, or to keep the
definition in a language-neutral file. The spec is JSON; its schema is
``doc/pyhdl-if-v2.schema.json``.

.. code-block:: bash

   pyhdl-if gen-from-spec pkt.json --sv-out pkt_pkg.sv --py-out pkt_api.py

The other front ends can write a spec too: give them ``--spec-out``.

Format
======

.. literalinclude:: ../../tests/unit/gen/data/spike.json
   :language: json

- ``"pyhdl-if-spec": 2`` marks the format.
- ``enums``: ``name``, ``width`` (1-64), optional ``signed``, and ``values``
  (``name``/``value`` pairs, in order).
- ``records``: ``name``, optional ``base`` (another record), and ``fields``
  (``name``/``type``, in order).
- ``interfaces``: ``name`` and ``methods``. A method has ``name``, ``kind``
  (``func``, the default, or ``task``), ``params`` (``name``/``type``) and an
  optional ``returns``.
- Definitions may refer to each other in any order.

Types
-----

.. list-table::
   :header-rows: 1

   * - Spelling
     - Meaning
   * - ``u<N>``, ``i<N>``
     - unsigned / signed integer of N bits
   * - ``bool``, ``f32``, ``f64``, ``str``, ``bytes``
     - as named
   * - ``list<T>``
     - a list of ``T`` (not of references or interfaces)
   * - the name of an enum, record or interface
     - that type (a record by copy)
   * - ``ref<record>``
     - a record by reference (parameters and results only)

Names must be valid in both languages: not a keyword of either, not
starting with ``__``. A few are reserved for generated code (``copy`` as a
field, ``dispose`` as a method, ``retval`` as a parameter), and a name may
not collide with a generated one (record ``pkt`` and record ``pkt_if``). Two
records may not contain each other by value.

The generators report problems with the element at fault, for example
``record pkt field kind: Undefined type 'proto'``.
