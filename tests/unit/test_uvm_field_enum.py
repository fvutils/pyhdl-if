#!/usr/bin/env python3

import pytest
import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hdl_if.uvm.wrap import UvmObjectType, UvmFieldType, UvmFieldKind
from enum import IntEnum
import dataclasses as dc


class TestUvmFieldEnum:
    """Test cases for UVM enum-type field registration and pack/unpack functionality"""
    
    def test_pack_unpack_enum_basic(self):
        """Test basic pack/unpack with an enum field"""
        
        # Define an enum type
        class ColorEnum(IntEnum):
            RED = 0
            GREEN = 1
            BLUE = 2
        
        @dc.dataclass
        class EnumData:
            color: int = 0
            value: int = 0
        
        # Define object type with an enum field
        obj_type = UvmObjectType(
            type_name="EnumData",
            data_t=EnumData,
            can_pack=True,
            fields=[
                UvmFieldType(name="color", kind=UvmFieldKind.ENUM, size=2, 
                           enum_type_name="ColorEnum", enum_type=ColorEnum),
                UvmFieldType(name="value", kind=UvmFieldKind.INT, size=8),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create data with enum value and pack
        data = EnumData(color=ColorEnum.GREEN, value=0x42)
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.color == ColorEnum.GREEN
        assert unpacked.value == 0x42
    
    def test_pack_unpack_enum_as_int(self):
        """Test pack/unpack when enum is passed as plain int"""
        
        class StateEnum(IntEnum):
            IDLE = 0
            ACTIVE = 1
            DONE = 2
        
        @dc.dataclass
        class StateData:
            state: int = 0
        
        obj_type = UvmObjectType(
            type_name="StateData",
            data_t=StateData,
            can_pack=True,
            fields=[
                UvmFieldType(name="state", kind=UvmFieldKind.ENUM, size=2,
                           enum_type_name="StateEnum", enum_type=StateEnum),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Pack with plain int value (should work)
        data = StateData(state=1)
        packed = obj_type.pack_ints(data)
        
        # Unpack - should convert to enum
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.state == StateEnum.ACTIVE
        assert isinstance(unpacked.state, StateEnum)
    
    def test_pack_unpack_multiple_enums(self):
        """Test pack/unpack with multiple enum fields"""
        
        class OpEnum(IntEnum):
            ADD = 0
            SUB = 1
            MUL = 2
            DIV = 3
        
        class StatusEnum(IntEnum):
            OK = 0
            ERROR = 1
        
        @dc.dataclass
        class MultiEnumData:
            operation: int = 0
            status: int = 0
            result: int = 0
        
        obj_type = UvmObjectType(
            type_name="MultiEnumData",
            data_t=MultiEnumData,
            can_pack=True,
            fields=[
                UvmFieldType(name="operation", kind=UvmFieldKind.ENUM, size=2,
                           enum_type_name="OpEnum", enum_type=OpEnum),
                UvmFieldType(name="status", kind=UvmFieldKind.ENUM, size=1,
                           enum_type_name="StatusEnum", enum_type=StatusEnum),
                UvmFieldType(name="result", kind=UvmFieldKind.INT, size=16),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create and pack data
        data = MultiEnumData(operation=OpEnum.MUL, status=StatusEnum.OK, result=42)
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.operation == OpEnum.MUL
        assert unpacked.status == StatusEnum.OK
        assert unpacked.result == 42
    
    def test_pack_unpack_enum_without_type(self):
        """Test pack/unpack with enum field but no enum_type specified"""
        
        @dc.dataclass
        class SimpleData:
            state: int = 0
        
        obj_type = UvmObjectType(
            type_name="SimpleData",
            data_t=SimpleData,
            can_pack=True,
            fields=[
                UvmFieldType(name="state", kind=UvmFieldKind.ENUM, size=3,
                           enum_type_name="state_e", enum_type=None),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Should work with plain int when no enum_type provided
        data = SimpleData(state=5)
        packed = obj_type.pack_ints(data)
        
        # Unpack - should return as int
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.state == 5
        assert isinstance(unpacked.state, int)
    
    def test_pack_unpack_enum_with_masking(self):
        """Test that enum values are properly masked to field size"""
        
        class BigEnum(IntEnum):
            SMALL = 1
            MEDIUM = 2
            LARGE = 0xFF  # Larger than 2 bits
        
        @dc.dataclass
        class MaskData:
            size: int = 0
        
        obj_type = UvmObjectType(
            type_name="MaskData",
            data_t=MaskData,
            can_pack=True,
            fields=[
                UvmFieldType(name="size", kind=UvmFieldKind.ENUM, size=2,
                           enum_type_name="BigEnum", enum_type=BigEnum),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Pack value that will be masked
        data = MaskData(size=BigEnum.LARGE)  # 0xFF -> 0x3 (2 bits)
        packed = obj_type.pack_ints(data)
        
        # Unpack - should be masked to 2 bits
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.size == 3  # 0xFF & 0x3 = 3
    
    def test_pack_unpack_mixed_enum_and_int(self):
        """Test pack/unpack with mix of enum and int fields"""
        
        class ModeEnum(IntEnum):
            READ = 0
            WRITE = 1
        
        @dc.dataclass
        class MixedData:
            addr: int = 0
            mode: int = 0
            data: int = 0
        
        obj_type = UvmObjectType(
            type_name="MixedData",
            data_t=MixedData,
            can_pack=True,
            fields=[
                UvmFieldType(name="addr", kind=UvmFieldKind.INT, size=16),
                UvmFieldType(name="mode", kind=UvmFieldKind.ENUM, size=1,
                           enum_type_name="ModeEnum", enum_type=ModeEnum),
                UvmFieldType(name="data", kind=UvmFieldKind.INT, size=32),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create and pack data
        data = MixedData(addr=0x1000, mode=ModeEnum.WRITE, data=0xDEADBEEF)
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.addr == 0x1000
        assert unpacked.mode == ModeEnum.WRITE
        assert unpacked.data == 0xDEADBEEF
    
    def test_pack_unpack_enum_invalid_value(self):
        """Test unpacking an invalid enum value (not in enum definition)"""
        
        class SmallEnum(IntEnum):
            A = 0
            B = 1
        
        @dc.dataclass
        class EnumData:
            val: int = 0
        
        obj_type = UvmObjectType(
            type_name="EnumData",
            data_t=EnumData,
            can_pack=True,
            fields=[
                UvmFieldType(name="val", kind=UvmFieldKind.ENUM, size=2,
                           enum_type_name="SmallEnum", enum_type=SmallEnum),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Pack value not in enum (2 is not defined in SmallEnum)
        data = EnumData(val=2)
        packed = obj_type.pack_ints(data)
        
        # Unpack - should handle gracefully by keeping as int
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.val == 2
        assert isinstance(unpacked.val, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
