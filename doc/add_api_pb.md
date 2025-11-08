# Support a new function
Implement the <class>::<function> function in hdl_if:
- Find the original definition in packages/uvm/src/.../<class>.svh
- Add a prototype to <class> src/hdl_if/uvm. Be sure to add type hints on both 
  parameters and return.
- Add an import wrapper method to src/hdl_if/uvm/wrap
- Implement the wrapper method in src/hdl_if/share/uvm/pyhdl_<class>.svh
- Add a UVM test similar to tests/unit/test_uvm_sequence_proxy.py::test_smoke
- Copy the documentation from packages/uvm/src/... and add to Python classes.
  Convert to pydocs (restructured text) format for Python methods
- Mark completed methods with '*' in doc/uvm_api.md

Methods are import unless otherwise noted. 
SystemVerilog tasks map to Python async methods. SystemVerilog functions 
map to Python regular methods

Reference doc/doc/theory_of_op.rst for background info
Run tests like this: pytest -s tests/unit/...

src/hdl_if/share/uvm/pyhdl_uvm_apis.svh is a generated file. Re-generate whenever
a Python class in src/hdl_if/uvm/wrap is changed. Use the following command:
% python -m hdl_if api-gen-sv -m hdl_if.uvm.wrap -o src/hdl_if/share/uvm/pyhdl_uvm_apis.svh

It's important to follow the class pattern in src/hdl_if/share/uvm/pyhdl_uvm_object.svh.
Don't attempt to flatten macros. Use them as shown.





