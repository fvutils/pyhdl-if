
import ctypes as ct
import hdl_if as hif

# Define a struct type
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
    ]

@hif.api
class StructBFM(object):

    @hif.imp
    async def set_point(self, p: Point):
        """Set a point (SV calls Python)"""
        pass

    @hif.imp
    async def get_point(self) -> Point:
        """Get a point (SV calls Python)"""
        pass

@hif.api
class StructTest(object):

    @hif.exp
    async def run(self, bfm: ct.py_object):
        """Test struct passing"""
        print("[Py] Creating test point")
        test_point = Point(x=42, y=100)
        
        print(f"[Py] Sending point: x={test_point.x}, y={test_point.y}")
        await bfm.set_point(test_point)
        
        print("[Py] Getting point back")
        result = await bfm.get_point()
        print(f"[Py] Received point: x={result.x}, y={result.y}")
        
        # Check if values match
        errors = 0
        if result.x != 42:
            print(f"[Py] ERROR: Expected x=42, got x={result.x}")
            errors += 1
        if result.y != 100:
            print(f"[Py] ERROR: Expected y=100, got y={result.y}")
            errors += 1
        
        with open("status.txt", "w") as fp:
            fp.write("%s: %d errors\n" % (("PASS" if errors==0 else "FAIL"), errors))

