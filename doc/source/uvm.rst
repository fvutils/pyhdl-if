###########
UVM Support
###########

Environment Integration
***********************

Initiating Python Behavior
**************************

Overview
--------
SystemVerilog proxy classes construct and drive Python implementations at
runtime. You supply the Python implementation class via a string (``pyclass``
field or ``PyClass`` parameter) and the proxy:
1. Parses the string into module and class names
2. Imports the Python module
3. Instantiates the class
4. Attaches the Python object to the SV proxy wrapper
5. Invokes phase or sequence body callbacks (starting the Python task
   scheduler when needed)

Component Proxy (SystemVerilog)
-------------------------------
Use ``pyhdl_uvm_component_proxy`` to host a Python UVM component implementation.

.. code-block:: systemverilog

   class my_env extends uvm_env;
     `uvm_component_utils(my_env)

     pyhdl_uvm_component_proxy m_pycomp;

     function new(string name, uvm_component parent);
       super.new(name, parent);
     endfunction

     function void build_phase(uvm_phase phase);
       super.build_phase(phase);
       m_pycomp = pyhdl_uvm_component_proxy::type_id::create("m_pycomp", this);
       // Format: module::Class or module:Class
       m_pycomp.pyclass = "pycomp::PyComp";
     endfunction
   endclass

Example: ``examples/uvm/component_proxy_smoke/top_pkg.sv`` with Python
implementation in ``examples/uvm/component_proxy_smoke/pycomp.py``.

Python Component Implementation
-------------------------------
Subclass ``uvm_component_impl`` and implement phase methods. A ``proxy``
dataclass field is injected to reference the SV proxy.

.. code-block:: python

   from hdl_if.uvm import uvm_component_impl

   class PyComp(uvm_component_impl):
       def build_phase(self, phase):
           print("-- build_phase", flush=True)

       def connect_phase(self, phase):
           print("-- connect_phase", flush=True)

       async def run_phase(self, phase):
           print("Hello from PyComp run_phase", flush=True)

Sequence Proxy (SystemVerilog)
------------------------------
Use ``pyhdl_uvm_sequence_proxy`` to host a Python sequence body and drive SV
sequence items.

Two ways to specify the Python class:

1. As a parameter at typedef:

   .. code-block:: systemverilog

      typedef pyhdl_uvm_sequence_proxy #(
        .REQ(seq_item),
        .PyClass("pyseq:PyRandSeq")
      ) py_seq_t;

      initial begin
        py_seq_t seq = py_seq_t::type_id::create("seq");
        seq.start(m_env.m_seqr);
      end

2. By assigning the ``pyclass`` field after construction:

   .. code-block:: systemverilog

      typedef pyhdl_uvm_sequence_proxy #(.REQ(seq_item)) py_seq_t;

      initial begin
        py_seq_t seq = py_seq_t::type_id::create("seq");
        seq.pyclass = "pyseq::PyRandSeq";
        seq.start(m_env.m_seqr);
      end

Examples:
- ``examples/uvm/sequence_rand_item/top_pkg.sv``
- ``examples/uvm/sequence_item_knobs/top_pkg.sv``
- ``examples/uvm/multi_comp_hierarchy/top_pkg.sv``
- ``examples/uvm/spi_reg_seq/top_pkg.sv``

Python Sequence Implementation
------------------------------
Subclass ``uvm_sequence_impl`` and implement ``async def body(self)`` using
the injected ``self.proxy`` helpers.

.. code-block:: python

   from hdl_if.uvm import uvm_sequence_impl

   class PyRandSeq(uvm_sequence_impl):
       async def body(self):
           for i in range(8):
               req = self.proxy.create_req()
               req.randomize()
               await self.proxy.start_item(req)
               await self.proxy.finish_item(req)

           # Additional pattern (knobs / unpack/pack) shown in other examples

Advanced Item Manipulation
--------------------------
Typical flow inside the Python sequence:
- Create item: ``req = self.proxy.create_req()``
- Randomize SV-side: ``req.randomize()``
- Access packed view: ``vals = req.pack()``
- Modify fields: assign to ``vals`` then ``req.unpack(vals)``
- Handshake: ``await self.proxy.start_item(req)`` / ``await self.proxy.finish_item(req)``

See:
- ``examples/uvm/sequence_item_knobs/pyseq.py`` (control knobs + field
  mutation)
- ``examples/uvm/spi_reg_seq/pyseq.py`` (register access sequencing)

PyClass String Format
---------------------
Accepted forms: ``module::ClassName`` (recommended) or ``module:ClassName``.

Parsing steps (SV side):
- Scan from end for first ``:`` (possibly part of a ``::`` pair)
- Class name = substring after the last colon(s)
- Module name = substring before the preceding colons
- Import: ``PyImport_ImportModule(module)``
- Lookup: ``PyObject_GetAttrString(module, ClassName)``

Errors:
- Empty string -> fatal
- Missing ``::`` / ``:`` delimiter -> fatal
- Module or class not found -> fatal (prints Python error stack)

Starting a Sequence Proxy
-------------------------
After creating and setting the Python class reference, start on a sequencer:

.. code-block:: systemverilog

   py_seq_t seq = py_seq_t::type_id::create("seq");
   seq.pyclass = "pyseq::PyRandSeq";
   seq.start(m_env.m_seqr);

Internals:
- Scheduler startup via ``pyhdl_if_start()``
- Python ``body()`` coroutine awaited within SV ``task body()``
- ``create_req()`` / ``create_rsp()`` provide typed SV items
- ``start_item()`` / ``finish_item()`` delegate to UVM item handshake

Lifecycle Summary
-----------------
Component:
1. Set ``pyclass`` before or during build.
2. SV build_phase loads module/class, constructs helper + Python impl.
3. Phases call through to Python implementation.

Sequence:
1. Set ``PyClass`` parameter or ``pyclass`` field.
2. On ``start()``, SV ``body()`` loads Python class, constructs helper.
3. Python ``body()`` drives items using proxy methods.

Troubleshooting
---------------
- Ensure module is on PYTHONPATH or relative to invocation directory.
- Verify delimiter usage (``module::Class``).
- Use sprint/print inside Python phases to confirm activation.
- Fatal errors are raised via UVM macros after Python traceback printing.

Class API Reference
*******************

.. autoclass:: hdl_if.uvm.UvmComponent

.. autoclass:: hdl_if.uvm.UvmObject

.. autoclass:: hdl_if.uvm.UvmSequence
