
import ctypes as ct
import hdl_if as hif

# Multiple different struct types
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

class Rectangle(ct.Structure):
    _fields_ = [
        ("x", ct.c_int32),
        ("y", ct.c_int32),
        ("width", ct.c_uint32),
        ("height", ct.c_uint32),
    ]

# Struct with various field types
class AllTypes(ct.Structure):
    _fields_ = [
        ("i8", ct.c_int8),
        ("u8", ct.c_uint8),
        ("i16", ct.c_int16),
        ("u16", ct.c_uint16),
        ("i32", ct.c_int32),
        ("u32", ct.c_uint32),
        ("i64", ct.c_int64),
        ("u64", ct.c_uint64),
        ("f32", ct.c_float),
        ("f64", ct.c_double),
        ("b", ct.c_bool),
    ]

# Struct with many fields
class ManyFields(ct.Structure):
    _fields_ = [
        ("f0", ct.c_int32),
        ("f1", ct.c_int32),
        ("f2", ct.c_int32),
        ("f3", ct.c_int32),
        ("f4", ct.c_int32),
        ("f5", ct.c_int32),
        ("f6", ct.c_int32),
        ("f7", ct.c_int32),
        ("f8", ct.c_int32),
        ("f9", ct.c_int32),
    ]

@hif.api
class ComprehensiveBFM(object):

    @hif.imp
    async def set_point(self, p: Point):
        """Set a point"""
        pass

    @hif.imp
    async def get_point(self) -> Point:
        """Get a point"""
        pass

    @hif.imp
    async def set_color(self, c: Color):
        """Set a color"""
        pass

    @hif.imp
    async def get_color(self) -> Color:
        """Get a color"""
        pass

    @hif.imp
    async def set_rectangle(self, r: Rectangle):
        """Set a rectangle"""
        pass

    @hif.imp
    async def get_rectangle(self) -> Rectangle:
        """Get a rectangle"""
        pass

    @hif.imp
    async def set_all_types(self, at: AllTypes):
        """Set struct with all types"""
        pass

    @hif.imp
    async def get_all_types(self) -> AllTypes:
        """Get struct with all types"""
        pass

    @hif.imp
    async def set_many_fields(self, mf: ManyFields):
        """Set struct with many fields"""
        pass

    @hif.imp
    async def get_many_fields(self) -> ManyFields:
        """Get struct with many fields"""
        pass

@hif.api
class ComprehensiveTest(object):

    @hif.exp
    async def run(self, bfm: ct.py_object):
        """Test comprehensive struct handling"""
        errors = 0
        
        # Test Point
        print("[Py] Testing Point struct...")
        test_point = Point(x=100, y=200)
        await bfm.set_point(test_point)
        result_point = await bfm.get_point()
        if result_point.x != 100 or result_point.y != 200:
            print(f"[Py] ERROR: Point mismatch - expected (100,200), got ({result_point.x},{result_point.y})")
            errors += 1
        else:
            print(f"[Py] ✓ Point OK: ({result_point.x},{result_point.y})")
        
        # Test Color
        print("[Py] Testing Color struct...")
        test_color = Color(r=255, g=128, b=64, a=32)
        await bfm.set_color(test_color)
        result_color = await bfm.get_color()
        if (result_color.r != 255 or result_color.g != 128 or 
            result_color.b != 64 or result_color.a != 32):
            print(f"[Py] ERROR: Color mismatch")
            errors += 1
        else:
            print(f"[Py] ✓ Color OK: RGBA({result_color.r},{result_color.g},{result_color.b},{result_color.a})")
        
        # Test Rectangle
        print("[Py] Testing Rectangle struct...")
        test_rect = Rectangle(x=10, y=20, width=300, height=400)
        await bfm.set_rectangle(test_rect)
        result_rect = await bfm.get_rectangle()
        if (result_rect.x != 10 or result_rect.y != 20 or 
            result_rect.width != 300 or result_rect.height != 400):
            print(f"[Py] ERROR: Rectangle mismatch")
            errors += 1
        else:
            print(f"[Py] ✓ Rectangle OK: ({result_rect.x},{result_rect.y}) {result_rect.width}x{result_rect.height}")
        
        # Test AllTypes
        print("[Py] Testing AllTypes struct...")
        test_all = AllTypes(
            i8=-128, u8=255, 
            i16=-32768, u16=65535,
            i32=-2147483648, u32=4294967295,
            i64=-9223372036854775808, u64=18446744073709551615,
            f32=3.14159, f64=2.71828,
            b=True
        )
        await bfm.set_all_types(test_all)
        result_all = await bfm.get_all_types()
        
        # Check integer fields
        if (result_all.i8 != -128 or result_all.u8 != 255 or
            result_all.i16 != -32768 or result_all.u16 != 65535 or
            result_all.i32 != -2147483648 or result_all.u32 != 4294967295 or
            result_all.i64 != -9223372036854775808 or result_all.u64 != 18446744073709551615):
            print(f"[Py] ERROR: AllTypes integer mismatch")
            print(f"  i8: {result_all.i8} (exp -128)")
            print(f"  u8: {result_all.u8} (exp 255)")
            print(f"  i16: {result_all.i16} (exp -32768)")
            print(f"  u16: {result_all.u16} (exp 65535)")
            print(f"  i32: {result_all.i32} (exp -2147483648)")
            print(f"  u32: {result_all.u32} (exp 4294967295)")
            print(f"  i64: {result_all.i64} (exp -9223372036854775808)")
            print(f"  u64: {result_all.u64} (exp 18446744073709551615)")
            errors += 1
        # Check float fields (with tolerance)
        elif (abs(result_all.f32 - 3.14159) > 0.00001 or 
              abs(result_all.f64 - 2.71828) > 0.00001):
            print(f"[Py] ERROR: AllTypes float mismatch")
            print(f"  f32: {result_all.f32} (exp 3.14159)")
            print(f"  f64: {result_all.f64} (exp 2.71828)")
            errors += 1
        # Check bool field
        elif result_all.b != True:
            print(f"[Py] ERROR: AllTypes bool mismatch: {result_all.b}")
            errors += 1
        else:
            print(f"[Py] ✓ AllTypes OK: all 11 fields verified")
        
        # Test ManyFields
        print("[Py] Testing ManyFields struct...")
        test_many = ManyFields(f0=0, f1=1, f2=2, f3=3, f4=4, f5=5, f6=6, f7=7, f8=8, f9=9)
        await bfm.set_many_fields(test_many)
        result_many = await bfm.get_many_fields()
        many_ok = all(getattr(result_many, f"f{i}") == i for i in range(10))
        if not many_ok:
            print(f"[Py] ERROR: ManyFields mismatch")
            for i in range(10):
                val = getattr(result_many, f"f{i}")
                if val != i:
                    print(f"  f{i}: {val} (expected {i})")
            errors += 1
        else:
            print(f"[Py] ✓ ManyFields OK: all 10 fields verified")
        
        print(f"\n[Py] Tests complete: {errors} errors")
        
        with open("status.txt", "w") as fp:
            fp.write("%s: %d errors\n" % (("PASS" if errors==0 else "FAIL"), errors))
