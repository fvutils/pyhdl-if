
- py_object
  - as_<> converters
  - to_<> terminal converters


- py_dict
  - mk
  - mk_new
  - clear
  - contains
  - contains_str
  - copy
  - set_item
  - set_item_str
  - del_item
  - del_item_str
  - get_item
  - get_item_ref
  - get_item_str
  - get_item_str_ref
  - pop
  - pop_str
  - size

- py_list
  - mk
  - mk_new
  - size
  - get_item
  - get_item_ref
  - set_item
  - insert
  - append
  - extend
  - clear
  - get_slice
  - set_slice
  - sort
  - reverse
  - as_tuple
  - to_tuple

- py_tuple
  - mk
  - mk_new
  - size
  - get_item
  - set_item
  - get_slice
  - set_slice

Use Cases
- Develop a symmetric API in Python and SystemVerilog
  - Call Python from SystemVerilog
  - Call SystemVerilog from Python
- Call an existing Python API using the Python API (abstracted or not)
- Implement a SystemVerilog convenience wrapper for an existing Python class
