########
Overview
########

.. image:: _imgs/pyhdl_library_stack.png
    :alt: PyHDL-IF API Stack

PyHDL-IF enables interaction between HDL and Python at a 
variety of abstraction levels. 


Procedural-Interface API
************************
The procedural interface API is the lowest-level PyHDL-IF
API. Because of this, it is also the most HDL- and simulator-specific.

There are two halves to the API:

- Make an implementation of the Python C API available as a HDL-native API.
- Make an implementation of the HDL-provided foreign-language interface 
  available in Python.

Call-Interface API
******************
The *Call Interface* API enables users to create pairs of communicating 
objects, where one object lives in Python, the other lives in HDL.

TLM API
*******



