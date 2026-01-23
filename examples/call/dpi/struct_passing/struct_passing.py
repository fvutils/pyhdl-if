
import ctypes as ct
import hdl_if as hif

# Define struct types for graphics operations
class Point(ct.Structure):
    """2D point with integer coordinates"""
    _fields_ = [
        ("x", ct.c_int32),
        ("y", ct.c_int32),
    ]

class Color(ct.Structure):
    """RGBA color with 8-bit channels"""
    _fields_ = [
        ("r", ct.c_uint8),
        ("g", ct.c_uint8),
        ("b", ct.c_uint8),
        ("a", ct.c_uint8),
    ]

class Rectangle(ct.Structure):
    """Rectangle with position and size"""
    _fields_ = [
        ("x", ct.c_int32),
        ("y", ct.c_int32),
        ("width", ct.c_uint32),
        ("height", ct.c_uint32),
    ]

@hif.api
class GraphicsAPI(object):
    """API for graphics operations using structured data"""

    @hif.imp
    async def draw_point(self, pos: Point, color: Color):
        """Draw a colored point at the specified position"""
        pass

    @hif.imp
    async def draw_rectangle(self, rect: Rectangle, color: Color):
        """Draw a colored rectangle"""
        pass

    @hif.imp
    async def get_pixel(self, pos: Point) -> Color:
        """Get the color of a pixel at the specified position"""
        pass

    @hif.imp
    async def get_bounds(self) -> Rectangle:
        """Get the bounding rectangle of the canvas"""
        pass

@hif.api
class GraphicsTest(object):
    """Test driver for graphics API"""

    @hif.exp
    async def run(self, gfx: ct.py_object):
        """Run graphics test sequence"""
        print("\n=== Graphics API Struct Passing Test ===\n")
        
        # Test 1: Draw a red point
        print("Test 1: Drawing red point at (100, 200)")
        pos1 = Point(x=100, y=200)
        red = Color(r=255, g=0, b=0, a=255)
        await gfx.draw_point(pos1, red)
        
        # Read back the pixel
        pixel = await gfx.get_pixel(pos1)
        print(f"  Read back: RGBA({pixel.r}, {pixel.g}, {pixel.b}, {pixel.a})")
        assert pixel.r == 255 and pixel.g == 0 and pixel.b == 0 and pixel.a == 255, "Red point mismatch!"
        
        # Test 2: Draw a green point
        print("\nTest 2: Drawing green point at (50, 75)")
        pos2 = Point(x=50, y=75)
        green = Color(r=0, g=255, b=0, a=128)
        await gfx.draw_point(pos2, green)
        
        pixel = await gfx.get_pixel(pos2)
        print(f"  Read back: RGBA({pixel.r}, {pixel.g}, {pixel.b}, {pixel.a})")
        assert pixel.r == 0 and pixel.g == 255 and pixel.b == 0 and pixel.a == 128, "Green point mismatch!"
        
        # Test 3: Draw a blue rectangle
        print("\nTest 3: Drawing blue rectangle at (10, 20) size 300x400")
        rect = Rectangle(x=10, y=20, width=300, height=400)
        blue = Color(r=0, g=0, b=255, a=200)
        await gfx.draw_rectangle(rect, blue)
        
        # Test 4: Get canvas bounds
        print("\nTest 4: Getting canvas bounds")
        bounds = await gfx.get_bounds()
        print(f"  Canvas: ({bounds.x}, {bounds.y}) size {bounds.width}x{bounds.height}")
        assert bounds.width == 1920 and bounds.height == 1080, "Unexpected canvas size!"
        
        print("\n=== All Tests Passed! ===\n")
