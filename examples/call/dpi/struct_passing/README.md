# Struct Passing Example

This example demonstrates how to pass structured data between Python and SystemVerilog using `ctypes.Structure` types in PyHDL-IF.

## Overview

The example implements a simple graphics API that uses three struct types:
- **Point** - 2D coordinates (x, y)
- **Color** - RGBA color values
- **Rectangle** - Position and size

The Python test code creates struct instances and passes them to SystemVerilog functions, which can then return struct values back to Python.

## Files

- **struct_passing.py** - Python API definition with struct types and test code
- **struct_passing.sv** - SystemVerilog implementation of graphics canvas
- **flow.yaml** - Build/run configuration for DV Flow Manager

## API Methods

The `GraphicsAPI` class provides the following methods:

```python
async def draw_point(self, pos: Point, color: Color)
```
Draws a colored point at the specified position.

```python
async def draw_rectangle(self, rect: Rectangle, color: Color)
```
Draws a colored rectangle.

```python
async def get_pixel(self, pos: Point) -> Color
```
Returns the color of a pixel at the specified position.

```python
async def get_bounds(self) -> Rectangle
```
Returns the canvas dimensions as a Rectangle.

## Running the Example

### Prerequisites

You need either:
1. A PyHDL-IF development environment (see main README)
2. The example tools environment (run `examples/setup.sh`)

### Run with DV Flow Manager

From the example directory:

```bash
cd examples/call/dpi/struct_passing
dfm run -Dsim=vlt sim-run
```

Replace `vlt` with your simulator:
- `vlt` - Verilator
- `xcm` - Cadence Xcelium
- `mti` - Siemens Questa
- `vcs` - Synopsys VCS

### Expected Output

```
[SV] Starting struct_passing example
[SV] Initializing PyHDL-IF...
[SV] Graphics API created
[SV] Starting test...

=== Graphics API Struct Passing Test ===

Test 1: Drawing red point at (100, 200)
[SV] draw_point: pos=(100,200) color=RGBA(255,0,0,255)
[SV] get_pixel: pos=(100,200)
[SV]   returning: RGBA(255,0,0,255)
  Read back: RGBA(255, 0, 0, 255)

Test 2: Drawing green point at (50, 75)
[SV] draw_point: pos=(50,75) color=RGBA(0,255,0,128)
[SV] get_pixel: pos=(50,75)
[SV]   returning: RGBA(0,255,0,128)
  Read back: RGBA(0, 255, 0, 128)

Test 3: Drawing blue rectangle at (10, 20) size 300x400
[SV] draw_rectangle: pos=(10,20) size=300x400 color=RGBA(0,0,255,200)

Test 4: Getting canvas bounds
[SV] get_bounds: returning canvas dimensions
[SV]   canvas: (0,0) size 1920x1080
  Canvas: (0, 0) size 1920x1080

=== All Tests Passed! ===

[SV] Test completed successfully
```

## What Gets Generated

When you run the example, PyHDL-IF automatically generates:

1. **SystemVerilog struct typedefs** in `struct_passing_pkg.sv`:
   ```systemverilog
   typedef struct packed {
       int x;
       int y;
   } Point_t;
   
   typedef struct packed {
       byte unsigned r;
       byte unsigned g;
       byte unsigned b;
       byte unsigned a;
   } Color_t;
   
   typedef struct packed {
       int x;
       int y;
       int unsigned width;
       int unsigned height;
   } Rectangle_t;
   ```

2. **Conversion functions** for each struct type:
   - `pyhdl_if_py_to_struct_Point()` - Python → SystemVerilog
   - `pyhdl_if_struct_to_py_Point()` - SystemVerilog → Python
   - (Similar functions for Color and Rectangle)

3. **Interface classes** that use the struct types in method signatures

## Key Concepts Demonstrated

1. **Defining Structs** - Using `ctypes.Structure` with `_fields_`
2. **Type Annotations** - Using struct types in method parameters and return types
3. **Bidirectional Passing** - Structs can be passed both to and from SystemVerilog
4. **Multiple Struct Types** - Single API can use multiple different struct types
5. **Automatic Code Generation** - PyHDL-IF handles all conversion code

## Learning More

For complete documentation on struct support, see:
- [doc/struct.md](../../../../doc/struct.md) - Comprehensive struct documentation
- [tests/unit/test_struct.py](../../../../tests/unit/test_struct.py) - Unit tests with more examples

## Extending the Example

Try modifying the example to:
- Add more struct types (e.g., Circle, Line)
- Add more complex operations (e.g., fill operations)
- Store a proper framebuffer in SystemVerilog
- Add floating-point fields to structs
