
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


