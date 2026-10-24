## Unreleased
- Records and interfaces shared between SystemVerilog and Python, generated
  from Python (`gen-from-py`), SystemVerilog (`gen-from-sv`, needs pyslang:
  `pip install pyhdl-if[sv]`) or a JSON spec (`gen-from-spec`), with dfm
  tasks `GenFromPy`, `GenFromSv` and `GenFromSpec`. Records can be copied or
  referenced; either side can implement an interface. Generated code calls
  only the PyHDL-IF runtime and is meant to be checked in; `--check` detects
  stale files. See the "Records and Interfaces" chapter.
- Runtime API version (`hdl_if.PYHDL_IF_RT_API_VERSION`, and
  `pyhdl_if::PYHDL_IF_RT_API_VERSION` in SV), checked by generated code.
- Fix: the result of a Python task called from SV could be freed before SV
  read it (`pyhdl_if_setSem` now keeps a reference).
- Fix: on Verilator built with `--vpi`, PyHDL-IF's VPI start-up aborted the
  simulation (Verilator has no `vpi_register_systf`). It now steps aside
  and PyHDL-IF starts through DPI.
- Fix: `ifc-gen-sv` and `ifc-gen-types` had no command handler.
- Fix: the `@imp`/`@exp` docstrings described the directions backwards.
- `python_requires >= 3.9`.


## 0.2.0
- Add generation of Python classes that mirror user-defined UVM classes

## 0.1.0
- Breaking API change in generated SV classes. By default, the generator now
  produces separate <class>_imp_impl and <class>_exp_impl classes. Add 
  --deprecated when calling the generator to enable previous behavior.

## 0.0.6
- Merge in WIP UVM integration

## 0.0.5
- (#34) - Explicitly import pyhdl_if package in generated code and alter the way that
          some library types are referenced to workaround an issue with Verilator (#6549).

## 0.0.4
- (#31) - Fix issues with double/real datatypes

## 0.0.3
- (#29) - Resolve issues with tasks and Python GIL
- (#22) - Resolve return value issue
- () - Add support for AMD Xilinx Xsim simulator
- () - Move tests over to use the DV Flow Manager PyTest extension

## 0.0.2
- (#25) - Correct issue passing string-type parameters


