############################
PyHDL-IF Theory of Operation
############################

*****************************
PyHDL-IF Library Fundamentals
*****************************

PyHDL-IF implements a function- and task-based interface with the simulator
using three core components:

* Python library
* SystemVerilog library
* DPI library

These three components provide APIs that are used to create linked pairs of
Python and SystemVerilog objects. Each object in the pair is responsible for 
implementing and responding to method invocation requests from its peer
object.

Startup Behavior
================
On startup, the simulator initializes the pyhdl_if package by calling
`__pyhdl_if_init`. This method loads the DPI library, initializes the
Python interpreter, and loads the Python portion of the PyHDL-IF library.
The pyhdl_if SystemVerilog package calls `hdl_if.impl.dpi.dpi_init` as
a step in the startup process. This method returns an HdlCallEndpointDPI
object that allows the Python and SystemVerilog portions of the 
implementation to coordinate.

Connecting Peer Objects
=======================

The Python and SystemVerilog peer objects may be created in any manner. 
Before they can be used as a pair, though, they must be connected. This 
is done by passing both the SystemVerilog and Python objects to 
`pyhdl_if_connectObject`. This method allocates a unique integer 
identifier for the SystemVerilog object and calls `connectObj` on 
the endpoint (ie HdlCallEndpointDPI), passing the Python object and
the unique identifier for the SystemVerilog object.

Calling a Python Method from SystemVerilog
==========================================

Calling a Python Async Method from SystemVerilog
================================================

Calling a SystemVerilog Function from Python
============================================

Calling a SystemVerilog Task from Python
========================================

*************************
SystemVerilog API Classes
*************************

The `api-gen-sv` command generates convenience classes to enable
calling `exp` methods from SystemVerilog and to allow SystemVerilog
classes to implement `imp` methods.

.. code-block:: python3

    class 


*************************
SystemVerilog UVM Classes
*************************

PyHDL-IF provides built-in support for interacting with SystemVerilog UVM
testbench environments. The following classes exist for each UVM class:

* Python `Protocol` class in hdl_if.uvm that defines the available methods. 
  Note that these classes are not marked with @api, @imp, or @exp.
* Python implementation classes in hdl_if.uvm.wrap that implement the 
  interface to SystemVerilog. 
* SystemVerilog interface class in hdl_if/share/uvm/pyhdl_uvm_<name>.svh 
  that implements the conversion between SystemVerilog types and Python
  types when necessary.
* SystemVerilog wrapper class in hdl_if/share/uvm/pyhdl_uvm_<name>.svh
  named pyhdl_uvm_<name>_w. This class extends from the generated SV/Python
  integration 'imp' implementation class, and implements pyhdl_uvm_object_if.

In general, SystemVerilog inout method parameters are implemented as
return values of the Python method.


