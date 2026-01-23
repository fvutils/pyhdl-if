######################
Struct Type Support
######################

PyHDL-IF supports using Python ``ctypes.Structure`` types as function parameters 
and return types in API methods. This enables efficient passing of structured data 
between Python and SystemVerilog.

Overview
========

When you define an API method that uses a struct type, PyHDL-IF automatically:

1. Generates a SystemVerilog ``typedef struct`` definition
2. Creates bidirectional conversion functions between Python and SystemVerilog
3. Handles the struct in method calls transparently

Defining Struct Types
======================

Struct types are defined as Python classes inheriting from ``ctypes.Structure``:

.. code-block:: python

    import ctypes as ct
    import hdl_if as hif

    class Point(ct.Structure):
        _fields_ = [
            ("x", ct.c_int32),
            ("y", ct.c_int32),
        ]

    class Color(ct.Structure):
        _fields_ = [
            ("r", ct.c_uint8),
            ("g", ct.c_uint8),
            ("b", ct.c_uint8),
            ("a", ct.c_uint8),
        ]

Using Structs in APIs
=====================

Once defined, structs can be used as parameters and return types in API methods:

.. code-block:: python

    @hif.api
    class GraphicsAPI(object):
        
        @hif.imp
        async def set_point(self, p: Point):
            """Called from SV to set a point"""
            pass
        
        @hif.imp
        async def get_point(self) -> Point:
            """Called from SV to get a point"""
            pass
        
        @hif.imp
        async def set_color(self, c: Color):
            """Called from SV to set a color"""
            pass

Supported Field Types
=====================

PyHDL-IF supports all standard ctypes in struct fields:

.. list-table:: Type Mapping
    :header-rows: 1
    :widths: 30 30 40

    * - Python Type
      - SystemVerilog Type
      - Description
    * - ``ctypes.c_int8``
      - ``byte``
      - Signed 8-bit integer
    * - ``ctypes.c_uint8``
      - ``byte unsigned``
      - Unsigned 8-bit integer
    * - ``ctypes.c_int16``
      - ``shortint``
      - Signed 16-bit integer
    * - ``ctypes.c_uint16``
      - ``shortint unsigned``
      - Unsigned 16-bit integer
    * - ``ctypes.c_int32``
      - ``int``
      - Signed 32-bit integer
    * - ``ctypes.c_uint32``
      - ``int unsigned``
      - Unsigned 32-bit integer
    * - ``ctypes.c_int64``
      - ``longint``
      - Signed 64-bit integer
    * - ``ctypes.c_uint64``
      - ``longint unsigned``
      - Unsigned 64-bit integer
    * - ``ctypes.c_float``
      - ``shortreal``
      - 32-bit floating point
    * - ``ctypes.c_double``
      - ``real``
      - 64-bit floating point
    * - ``ctypes.c_bool``
      - ``bit``
      - Boolean
    * - ``str``
      - ``string``
      - String type

Generated SystemVerilog Code
=============================

For the ``Point`` example above, PyHDL-IF generates:

Typedef
-------

.. code-block:: systemverilog

    typedef struct packed {
        int x;
        int y;
    } Point_t;

Conversion Functions
--------------------

**Python to SystemVerilog:**

.. code-block:: systemverilog

    function Point_t pyhdl_if_py_to_struct_Point(pyhdl_if::PyObject py_obj);
        Point_t result;
        pyhdl_if::PyObject __field_x, __field_y;
        __field_x = pyhdl_if::PyObject_GetAttrString(py_obj, "x");
        result.x = int'(pyhdl_if::PyLong_AsLong(__field_x));
        pyhdl_if::Py_DecRef(__field_x);
        __field_y = pyhdl_if::PyObject_GetAttrString(py_obj, "y");
        result.y = int'(pyhdl_if::PyLong_AsLong(__field_y));
        pyhdl_if::Py_DecRef(__field_y);
        return result;
    endfunction

**SystemVerilog to Python:**

.. code-block:: systemverilog

    function pyhdl_if::PyObject pyhdl_if_struct_to_py_Point(Point_t sv_struct);
        pyhdl_if::PyObject __module, __class, __args, result;
        __module = pyhdl_if::PyImport_ImportModule("your_module");
        __class = pyhdl_if::PyObject_GetAttrString(__module, "Point");
        __args = pyhdl_if::PyTuple_New(2);
        void'(pyhdl_if::PyTuple_SetItem(__args, 0, 
              pyhdl_if::PyLong_FromLong(longint'(sv_struct.x))));
        void'(pyhdl_if::PyTuple_SetItem(__args, 1, 
              pyhdl_if::PyLong_FromLong(longint'(sv_struct.y))));
        result = pyhdl_if::PyObject_Call(__class, __args, null);
        pyhdl_if::Py_DecRef(__args);
        pyhdl_if::Py_DecRef(__class);
        pyhdl_if::Py_DecRef(__module);
        return result;
    endfunction

Using Structs from SystemVerilog
=================================

In your SystemVerilog testbench, implement the interface methods using the 
generated struct types:

.. code-block:: systemverilog

    class GraphicsAPI_Impl implements graphics_api_pkg::GraphicsAPI_imp_if;
        graphics_api_pkg::Point_t m_point;

        virtual task set_point(input graphics_api_pkg::Point_t p);
            $display("Received point: x=%0d, y=%0d", p.x, p.y);
            m_point = p;
        endtask

        virtual task get_point(output graphics_api_pkg::Point_t retval);
            $display("Returning point: x=%0d, y=%0d", m_point.x, m_point.y);
            retval = m_point;
        endtask
    endclass

Packed vs Unpacked Structs
===========================

PyHDL-IF automatically determines whether to use ``packed`` or unpacked structs:

- **Packed structs**: Used when all fields are synthesizable types (integers, bits)
- **Unpacked structs**: Used when any field is a floating-point type (``real``, ``shortreal``)

This is necessary because SystemVerilog does not allow real types in packed structs.

Complete Example
================

A complete working example is available at ``examples/call/dpi/struct_passing/``. 
The example demonstrates:

- Defining multiple struct types (Point, Color, Rectangle)
- Using structs as both parameters and return values
- Bidirectional struct passing between Python and SystemVerilog
- A simple graphics API implementation

Run the example:

.. code-block:: bash

    cd examples/call/dpi/struct_passing
    dfm run -Dsim=vlt sim-run

Limitations
===========

1. **Nested Structs**: Structs containing other structs as fields are not currently tested
2. **Arrays in Structs**: Array fields (using ctypes array types) are not currently supported
3. **Module Name**: The SV-to-Python conversion function needs to import the Python module 
   containing the struct definition. Ensure the module is in the Python path.

See Also
========

- :doc:`quickstart` - Getting started guide
- :doc:`py_api` - Python API reference
- :doc:`sv_api` - SystemVerilog API reference
- Full struct documentation: `doc/struct.md <https://github.com/fvutils/pyhdl-if/blob/main/doc/struct.md>`_
