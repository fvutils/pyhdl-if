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

*************************
SystemVerilog UVM Classes
*************************

