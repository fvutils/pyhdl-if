#################
SystemVerilog API
#################

The SystemVerilog API provides three levels of Python API access:

- Generated wrapper classes that mirror a Python-defined API
- An abstracted class-based convenience API
- Direct access to the Python C API

Generated wrappers

The SystemVerilog API generator creates wrapper classes that enable 
bidirectional communication between Python and SystemVerilog code. This system 
allows you to define APIs in Python and automatically generate corresponding 
SystemVerilog interfaces and implementations.

Command Usage
-------------

The ``api-gen-sv`` command generates SystemVerilog wrapper code from Python 
API definitions:

.. code-block:: bash

   python -m hdl_if api-gen-sv -m my_module -o my_api.svh

**Required Parameters:**

* ``-m, --module``: Python module(s) containing ``@api`` decorated classes 
  (can be specified multiple times)

**Optional Parameters:**

* ``-o, --output``: Output file name (default: ``hdl_call_if_api.svh``)
* ``-p, --package``: Wrap generated code in a SystemVerilog package
* ``-uvm``: Generate UVM-friendly interface classes
* ``--deprecated``: Include legacy class formats

**Example:**

.. code-block:: bash

   python -m hdl_if api-gen-sv \
     -m my_project.interfaces \
     -m my_project.components \
     -p my_api_pkg \
     -o generated_api.svh

Python API Definition
---------------------

APIs are defined in Python using decorators to mark classes and methods for 
SystemVerilog generation.

API Class Decorator
~~~~~~~~~~~~~~~~~~~

Use the ``@api`` decorator to mark a class for SystemVerilog generation:

.. code-block:: python

   from hdl_if.decorators import api, imp, exp
   
   @api
   class memory_interface:
       """Custom memory interface API"""
       pass

Method Decorators
~~~~~~~~~~~~~~~~~

Two decorators control the direction of method calls:

* ``@imp``: **Implementation methods** - Implemented in SystemVerilog, 
  called from Python
* ``@exp``: **Export methods** - Implemented in Python, called from 
  SystemVerilog

.. code-block:: python

   @api
   class memory_interface:
       @imp
       def write(self, addr: int, data: int) -> bool:
           """Write data to memory (implemented in SV)"""
           pass
           
       @imp  
       def read(self, addr: int) -> int:
           """Read data from memory (implemented in SV)"""
           pass
           
       @exp
       def on_write_complete(self, addr: int, success: bool) -> None:
           """Callback when write completes (implemented in Python)"""
           print(f"Write to {addr}: {'success' if success else 'failed'}")

Type Translation
----------------

Python type annotations are automatically translated to SystemVerilog types:

.. list-table:: Type Translation Table
   :header-rows: 1
   :widths: 30 30 40

   * - Python Type
     - SystemVerilog Type  
     - Notes
   * - ``int``
     - ``longint``
     - 64-bit signed integer
   * - ``bool``
     - ``bit``
     - Single bit
   * - ``str``
     - ``string``
     - SystemVerilog string type
   * - ``float``
     - ``real``
     - Floating point number
   * - ``List[T]``
     - ``pyhdl_if::PyObject``
     - Python list object
   * - Custom objects
     - ``pyhdl_if::PyObject``
     - Python object reference
   * - ``ctypes.c_uint32``
     - ``int unsigned``
     - Specific width integers
   * - ``ctypes.c_int8``
     - ``byte``
     - 8-bit signed integer

**Parameter Directions:**

* Method parameters become ``input`` parameters in SystemVerilog
* Return values become function return types or ``output`` parameters for tasks
* Tasks (methods that may block) use ``output`` parameters for return values

Generated Class Structure
-------------------------

For each ``@api`` class, four SystemVerilog components are generated:

1. **``<class>_exp_if``**: Interface for SystemVerilog calling Python methods 
   (``@exp`` methods)
2. **``<class>_imp_if``**: Interface for Python calling SystemVerilog methods 
   (``@imp`` methods)  
3. **``<class>_exp_impl``**: Implementation class for SystemVerilog to call 
   Python
4. **``<class>_imp_impl``**: Implementation class for Python to call 
   SystemVerilog

Interface Classes
~~~~~~~~~~~~~~~~~

The interface classes define the method signatures:

.. code-block:: systemverilog

   // Generated for @exp methods
   interface class memory_interface_exp_if;
       pure virtual function void on_write_complete(
           input int addr,
           input bit success
       );
   endclass

   // Generated for @imp methods  
   interface class memory_interface_imp_if;
       pure virtual function bit write(
           input longint addr,
           input longint data
       );
       pure virtual function longint read(input longint addr);
   endclass

Implementation Classes
~~~~~~~~~~~~~~~~~~~~~~

The implementation classes handle the Python/SystemVerilog communication:

**``<class>_exp_impl``**: For calling Python from SystemVerilog
   
.. code-block:: systemverilog

   class memory_interface_exp_impl implements memory_interface_exp_if;
       pyhdl_if::PyObject m_obj;
       
       function new(pyhdl_if::PyObject obj=null, bit create=1, string clsname="memory_interface");
           // Constructor logic
       endfunction
       
       virtual function void on_write_complete(input int addr, input bit success);
           // Calls Python method through PyObject
       endfunction
   endclass

**``<class>_imp_impl``**: For calling SystemVerilog from Python

.. code-block:: systemverilog

   class memory_interface_imp_impl #(type ImpT=memory_interface_imp_if) 
           implements pyhdl_if::ICallApi;
       ImpT m_impl;
       
       function new(ImpT impl, pyhdl_if::PyObject obj=null, bit create=1);
           // Constructor logic  
       endfunction
       
       virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);
           // Dispatches to SystemVerilog implementation
       endfunction
   endclass

SystemVerilog Implementation Example
------------------------------------

To use the generated API, implement the ``_imp_if`` interface in SystemVerilog:

.. code-block:: systemverilog

   class my_memory implements memory_interface_imp_if;
       logic [31:0] mem[1024];
       
       virtual function bit write(input longint addr, input longint data);
           if (addr < 1024) begin
               mem[addr] = data[31:0];
               return 1'b1;  // Success
           end
           return 1'b0;  // Failure
       endfunction
       
       virtual function longint read(input longint addr);
           if (addr < 1024) begin
               return longint'(mem[addr]);
           end
           return 0;
       endfunction
   endclass

SystemVerilog Usage Example  
---------------------------

Create and connect the API implementations:

.. code-block:: systemverilog

   module testbench;
       // Create SystemVerilog implementation
       my_memory mem_impl;
       
       // Create Python-to-SV bridge
       memory_interface_imp_impl #(my_memory) mem_bridge;
       
       // Create SV-to-Python caller  
       memory_interface_exp_impl py_caller;
       
       initial begin
           // Initialize implementations
           mem_impl = new();
           mem_bridge = new(mem_impl);
           py_caller = new();
           
           // Use the API
           automatic bit success = mem_bridge.invokeFunc("write", args);
           py_caller.on_write_complete(32'h100, success);
       end
   endmodule

Best Practices
--------------

**Object Lifecycle:**
   * Always properly initialize implementation objects before creating bridges
   * Use the provided constructors to establish Python/SystemVerilog 
     connections
   * Handle Python GIL (Global Interpreter Lock) properly in custom 
     implementations

**Error Handling:**
   * Check return values from API calls
   * Handle Python exceptions that may propagate through the interface
   * Use appropriate SystemVerilog error handling for failed API calls

**Performance:**
   * Minimize frequent calls across the Python/SystemVerilog boundary
   * Batch operations when possible to reduce overhead
   * Be aware that each cross-language call has performance implications

Complete Working Example
------------------------

**1. Python API Definition (``my_api.py``):**

.. code-block:: python

   from hdl_if.decorators import api, imp, exp
   
   @api  
   class counter_api:
       @imp
       def increment(self) -> int:
           """Increment counter, return new value"""
           pass
           
       @imp
       def get_value(self) -> int:
           """Get current counter value"""
           pass
           
       @exp
       def on_overflow(self, value: int) -> None:
           """Called when counter overflows"""
           print(f"Counter overflow at value: {value}")

**2. Generate SystemVerilog:**

.. code-block:: bash

   python -m hdl_if api-gen-sv -m my_api -o counter_api.svh

**3. SystemVerilog Implementation:**

.. code-block:: systemverilog

   `include "counter_api.svh"
   
   class counter_impl implements counter_api_imp_if;
       int counter = 0;
       counter_api_exp_impl py_notifier;
       
       function new(counter_api_exp_impl notifier);
           py_notifier = notifier;
       endfunction
       
       virtual function longint increment();
           counter++;
           if (counter > 1000) begin
               py_notifier.on_overflow(counter);
               counter = 0;
           end
           return longint'(counter);
       endfunction
       
       virtual function longint get_value();
           return longint'(counter);
       endfunction
   endclass

**4. SystemVerilog Usage:**

.. code-block:: systemverilog

   module test;
       counter_impl impl;
       counter_api_imp_impl #(counter_impl) bridge;
       counter_api_exp_impl py_caller;
       
       initial begin
           py_caller = new();
           impl = new(py_caller);  
           bridge = new(impl);
           
           // Test the API
           for (int i = 0; i < 1005; i++) begin
               automatic longint val = bridge.invokeFunc("increment", null);
               $display("Counter: %0d", val);
           end
       end
   endmodule

This example demonstrates the complete flow from Python API definition to 
SystemVerilog implementation and usage, showing both directions of 
tcommunication between Python and SystemVerilog.
==================

Class-Based API
===============
.. doxygenclass:: py_object
    :members:

.. doxygenclass:: py_dict
    :members:

.. doxygenclass:: py_list
    :members:

.. doxygenclass:: py_tuple
    :members:

Utility Methods
---------------

.. doxygenfunction:: py_from_int

.. doxygenfunction:: py_from_uint

.. doxygenfunction:: py_from_long

.. doxygenfunction:: py_from_ulong

.. doxygenfunction:: py_from_str

.. doxygenfunction:: py_import

.. doxygenfunction:: py_call_builtin

.. doxygenfunction:: py_gil_enter

.. doxygenfunction:: py_gil_leave



Direct API
==========
