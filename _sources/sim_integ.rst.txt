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

    python3 -c 'import hdl_if; print(hdl_if.share())'

- Specify `${share}/dpi` as an include directory
- Specify `${share}/dpi/pyhdl_if.sv` as a source file

DPI Shared Library
******************
Two shared libraries must be specified as DPI libraries to the simulator:

- PyHDL-IF entrypoint
- Python 

Obtain the paths to these libraries by running:

.. code:: shell

    python3 -c 'import hdl_if; print(" ".join(hdl_if.libs("dpi")))'

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

