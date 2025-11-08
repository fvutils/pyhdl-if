
# ConfigDB support on components

# Factory-method support

# Proxy associated data
- Allow a UVM object-based object to be associated with a 
sequence or component proxy. This allows the caller to 
easily pass accessible data to the implementation.
- Add convenience classes
  - object_map
  - object_list
  - string, int value wrappers
- Implement Python wrappers with convenience methods

# Cancel SV task
- Support killing asyncio tasks that represent SV task calls
  - Catch exception in Python
  - Kill process in SV

# UVM reg value
- Specialized int-based type -> encodes fields for reading
- Immutable, so must use 
  set(**kwargs):
  val = val.set(field1=1, field2=2) # Is a bit of runtime validation
-> Type is specific, so we can build a function with specific kwargs

# User-defined wrapper classes
Allows the user to define wrapper classes with custom APIs. These
methods can accept and return typed objects.
-> Challenge: Must provide a dynamically-constructed way to locate
  the proper wrapper class for a UVM-derived object
- To register, must know class type and base-class type
- Use a type-registry type to create unique handles for each
  registered type
- type_w node has a list of derived type_w nodes
- type_w node provides 'isinstance' method that checks if object isinstance
- Object factory starts at type_w #(uvm_object) and searches 
  deeper the longer 
- Can we detect an improperly-constructed type tree where multiple
  children would match? 


# Class Metadata
Define macros in SystemVerilog that attach metadata to UVM classes.
This metadata, such as docstrings, is used by the mock-class generator.
Need to support attaching to class and methods.

# Support Uvm2Py config file
- Allow filtering classes to convert
- Allow directing to specific packages
