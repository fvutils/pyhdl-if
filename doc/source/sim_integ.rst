#####################
Simulator Integration
#####################

SystemVerilog (DPI)
===================

Source
******
The PyHDL-IF SystemVerilog package must be compiled prior to 
compilation of code that uses PyHDL-IF artifacts. If you use
a FuseSoC-based build system, simply place a dependency on
`fvutils::pyhdl-if`. 

If you directly specify sources:

- Obtain the `share` directory by calling: 

  .. code:: shell

    % python3 -c 'import hdl_if; print(hdl_if.share())'
    # OR
    % python3 -m hdl_if share

- Specify `${share}/dpi` as an include directory
- Specify `${share}/dpi/pyhdl_if.sv` as a source file

DPI Shared Library
******************
Two shared libraries must be specified as DPI libraries to the simulator:

- PyHDL-IF entrypoint
- Python 

Obtain the paths to these libraries by running:

.. code:: shell

    % python3 -c 'import hdl_if; print(" ".join(hdl_if.libs("dpi")))'
    # OR
    % python3 -m hdl_if libs --type dpi

Specify these as DPI libraries to your simulator using its preferred mechanism.

Verilog (VPI)
=============
TBD

VHDL (VHPI)
===========
TBD

VHDL (FLI)
==========
TBD

Loading the Python Library
**************************

When the PyHDL-IF library is initialized, it will try to load the Python
shared library and locate symbols for simulator-provided APIs.

By default, the following process is followed:

* If ${LIBPYTHON_LOC} is set, this shared library is loaded and Python symbols
  are obtained from it.
* Python symbols will be obtained from the simulator's global namespace 
  if Python symbols are available in the simulator's global namespace.
* Next, shared libraries loaded by the simulator process are checked to specified
  if they provide Python symbols. 
* Next, the available Python interpreter is used to discover where its shared 
  library is installed.

LIBPYTHON_LOC
=============
The environment variable `LIBPYTHON_LOC` can be set to specify the location of the
Python shared library. Note that a full path must be specified.

PYHDL_IF_PYTHON
===============
The environment variable `PYHDL_IF_PYTHON` can be set to specify the Python
interpreter to probe for configuration information. 