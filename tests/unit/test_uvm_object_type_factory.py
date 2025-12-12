#!/usr/bin/env python3

import pytest
import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hdl_if.uvm.wrap import UvmObjectType, UvmFieldType, UvmFieldKind
from hdl_if.uvm.wrap import uvm_object_rgy as UvmObjectRgy


class TestUvmObjectTypeFactory:
    """Test cases for UvmObjectTypeFactory populate_fields functionality"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.factory = UvmObjectRgy()
    
    def test_populate_fields_normal_layout(self):
        """Test parsing normal layout with valid field sizes"""
        layout = """------------------------------------------------------------------
Name          Type           Size  Value
------------------------------------------------------------------
my_data       integral       32    'h12345678
my_enable     integral       1     'h1
my_count      integral       16    'habcd
------------------------------------------------------------------
"""
        
        obj_t = UvmObjectType()
        self.factory.populate_fields(obj_t, layout)
        
        # Verify can_pack remains True (all sizes are valid)
        assert obj_t.can_pack == True
        
        # Verify correct number of fields
        assert len(obj_t.fields) == 3
        
        # Verify field details
        assert obj_t.fields[0].name == "my_data"
        assert obj_t.fields[0].size == 32
        assert obj_t.fields[0].kind == UvmFieldKind.INT
        assert obj_t.fields[0].is_signed == False
        
        assert obj_t.fields[1].name == "my_enable"
        assert obj_t.fields[1].size == 1
        assert obj_t.fields[1].kind == UvmFieldKind.INT
        
        assert obj_t.fields[2].name == "my_count"
        assert obj_t.fields[2].size == 16
        assert obj_t.fields[2].kind == UvmFieldKind.INT
    
    def test_populate_fields_unknown_size(self):
        """Test handling of fields with unknown size (should set can_pack=False)"""
        layout = """------------------------------------------------------------------
Name          Type           Size  Value
------------------------------------------------------------------
my_data       integral       32    'h12345678
my_object     object         -     <object>
my_count      integral       16    'habcd
------------------------------------------------------------------
"""
        
        obj_t = UvmObjectType()
        self.factory.populate_fields(obj_t, layout)
        
        # Verify can_pack is set to False due to unknown size
# MSB:        assert obj_t.can_pack == False
        
        # Verify we still get the fields with valid sizes
        assert len(obj_t.fields) == 2  # my_object should be skipped due to "-" size
        
        assert obj_t.fields[0].name == "my_data"
        assert obj_t.fields[0].size == 32
        
        assert obj_t.fields[1].name == "my_count"
        assert obj_t.fields[1].size == 16
    
    def test_populate_fields_invalid_size(self):
        """Test handling of fields with invalid/unparseable size"""
        layout = """------------------------------------------------------------------
Name          Type           Size  Value
------------------------------------------------------------------
my_data       integral       32    'h12345678
my_bad_field  integral       xyz   'h00
my_count      integral       16    'habcd
------------------------------------------------------------------
"""
        
        obj_t = UvmObjectType()
        self.factory.populate_fields(obj_t, layout)
        
        # Verify can_pack is set to False due to unparseable size
        assert obj_t.can_pack == False
        
        # Verify we get all fields, with bad one having size -1
        assert len(obj_t.fields) == 3
        
        assert obj_t.fields[0].name == "my_data"
        assert obj_t.fields[0].size == 32
        
        assert obj_t.fields[1].name == "my_bad_field"
        assert obj_t.fields[1].size == -1  # Should be set to -1 for unparseable
        
        assert obj_t.fields[2].name == "my_count"
        assert obj_t.fields[2].size == 16
    
    def test_populate_fields_empty_layout(self):
        """Test handling of empty layout"""
        layout = ""
        
        obj_t = UvmObjectType()
        self.factory.populate_fields(obj_t, layout)
        
        # Verify defaults are maintained
        assert obj_t.can_pack == True
        assert len(obj_t.fields) == 0
    
    def test_populate_fields_only_separators(self):
        """Test handling of layout with only separator lines"""
        layout = """------------------------------------------------------------------
------------------------------------------------------------------
"""
        
        obj_t = UvmObjectType()
        self.factory.populate_fields(obj_t, layout)
        
        # Verify defaults are maintained
        assert obj_t.can_pack == True
        assert len(obj_t.fields) == 0
    
    def test_populate_fields_header_only(self):
        """Test handling of layout with header but no fields"""
        layout = """------------------------------------------------------------------
Name          Type           Size  Value
------------------------------------------------------------------
------------------------------------------------------------------
"""
        
        obj_t = UvmObjectType()
        self.factory.populate_fields(obj_t, layout)
        
        # Verify defaults are maintained
        assert obj_t.can_pack == True
        assert len(obj_t.fields) == 0
    
    def test_populate_fields_insufficient_tokens(self):
        """Test handling of lines with insufficient tokens"""
        layout = """------------------------------------------------------------------
Name          Type           Size  Value
------------------------------------------------------------------
incomplete_line    integral
my_data       integral       32    'h12345678
------------------------------------------------------------------
"""
        
        obj_t = UvmObjectType()
        self.factory.populate_fields(obj_t, layout)
        
        # Should skip incomplete line and process valid one
        assert obj_t.can_pack == True
        assert len(obj_t.fields) == 1
        
        assert obj_t.fields[0].name == "my_data"
        assert obj_t.fields[0].size == 32


class TestUvmFieldTypes:
    """Test cases for UvmFieldType and UvmFieldKind classes"""
    
    def test_uvm_field_kind_enum(self):
        """Test UvmFieldKind enum values"""
        assert UvmFieldKind.INT.value == "int"
        assert UvmFieldKind.STR.value == "str"
        assert UvmFieldKind.OBJ.value == "obj"
    
    def test_uvm_field_type_defaults(self):
        """Test UvmFieldType default values"""
        field = UvmFieldType(name="test_field")
        
        assert field.name == "test_field"
        assert field.kind == UvmFieldKind.INT
        assert field.size == -1
        assert field.is_signed == False
        assert field.obj_type is None
    
    def test_uvm_field_type_custom_values(self):
        """Test UvmFieldType with custom values"""
        field = UvmFieldType(
            name="custom_field",
            kind=UvmFieldKind.STR,
            size=64,
            is_signed=True
        )
        
        assert field.name == "custom_field"
        assert field.kind == UvmFieldKind.STR
        assert field.size == 64
        assert field.is_signed == True
        assert field.obj_type is None


class TestUvmObjectType:
    """Test cases for UvmObjectType class"""
    
    def test_uvm_object_type_defaults(self):
        """Test UvmObjectType default values"""
        obj_type = UvmObjectType()
        
        assert obj_type.can_pack == True
        assert len(obj_type.fields) == 0
        assert isinstance(obj_type.fields, list)
    
    def test_uvm_object_type_with_fields(self):
        """Test UvmObjectType with fields"""
        field1 = UvmFieldType(name="field1", size=8)
        field2 = UvmFieldType(name="field2", size=16)
        
        obj_type = UvmObjectType(can_pack=False, fields=[field1, field2])
        
        assert obj_type.can_pack == False
        assert len(obj_type.fields) == 2
        assert obj_type.fields[0].name == "field1"
        assert obj_type.fields[1].name == "field2"


class TestUvmObjectTypePacking:
    """Test cases for UvmObjectType pack_ints/unpack_ints with nested objects"""

    def test_pack_unpack_int_fields_only(self):
        """Test basic pack/unpack with INT fields only"""
        import dataclasses as dc

        @dc.dataclass
        class SimpleData:
            field_a: int = 0
            field_b: int = 0

        obj_type = UvmObjectType(
            type_name="SimpleData",
            data_t=SimpleData,
            can_pack=True,
            fields=[
                UvmFieldType(name="field_a", kind=UvmFieldKind.INT, size=8),
                UvmFieldType(name="field_b", kind=UvmFieldKind.INT, size=16),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}

        # Create data object and pack
        data = SimpleData(field_a=0xAB, field_b=0x1234)
        packed = obj_type.pack_ints(data)

        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.field_a == 0xAB
        assert unpacked.field_b == 0x1234

    def test_pack_unpack_nested_object(self):
        """Test pack/unpack with a nested object field"""
        import dataclasses as dc

        @dc.dataclass
        class InnerData:
            inner_val: int = 0

        @dc.dataclass
        class OuterData:
            outer_val: int = 0
            nested: object = None

        # Define inner object type
        inner_type = UvmObjectType(
            type_name="InnerData",
            data_t=InnerData,
            can_pack=True,
            fields=[
                UvmFieldType(name="inner_val", kind=UvmFieldKind.INT, size=16),
            ]
        )
        inner_type.field_m = {f.name: f for f in inner_type.fields}

        # Define outer object type with nested object field
        outer_type = UvmObjectType(
            type_name="OuterData",
            data_t=OuterData,
            can_pack=True,
            fields=[
                UvmFieldType(name="outer_val", kind=UvmFieldKind.INT, size=8),
                UvmFieldType(name="nested", kind=UvmFieldKind.OBJ, obj_type=inner_type),
            ]
        )
        outer_type.field_m = {f.name: f for f in outer_type.fields}

        # Create data with nested object and pack
        inner_data = InnerData(inner_val=0xBEEF)
        outer_data = OuterData(outer_val=0x42, nested=inner_data)
        packed = outer_type.pack_ints(outer_data)

        # Unpack and verify
        unpacked = outer_type.unpack_ints(packed)
        assert unpacked.outer_val == 0x42
        assert unpacked.nested is not None
        assert unpacked.nested.inner_val == 0xBEEF

    def test_pack_unpack_null_object(self):
        """Test pack/unpack with a null nested object field"""
        import dataclasses as dc

        @dc.dataclass
        class InnerData:
            inner_val: int = 0

        @dc.dataclass
        class OuterData:
            outer_val: int = 0
            nested: object = None

        # Define inner object type
        inner_type = UvmObjectType(
            type_name="InnerData",
            data_t=InnerData,
            can_pack=True,
            fields=[
                UvmFieldType(name="inner_val", kind=UvmFieldKind.INT, size=16),
            ]
        )
        inner_type.field_m = {f.name: f for f in inner_type.fields}

        # Define outer object type with nested object field
        outer_type = UvmObjectType(
            type_name="OuterData",
            data_t=OuterData,
            can_pack=True,
            fields=[
                UvmFieldType(name="outer_val", kind=UvmFieldKind.INT, size=8),
                UvmFieldType(name="nested", kind=UvmFieldKind.OBJ, obj_type=inner_type),
            ]
        )
        outer_type.field_m = {f.name: f for f in outer_type.fields}

        # Create data with null nested object and pack
        outer_data = OuterData(outer_val=0x99, nested=None)
        packed = outer_type.pack_ints(outer_data)

        # Unpack and verify
        unpacked = outer_type.unpack_ints(packed)
        assert unpacked.outer_val == 0x99
        assert unpacked.nested is None

    def test_pack_unpack_deeply_nested_objects(self):
        """Test pack/unpack with multiple levels of nested objects"""
        import dataclasses as dc

        @dc.dataclass
        class Level3Data:
            val3: int = 0

        @dc.dataclass
        class Level2Data:
            val2: int = 0
            child: object = None

        @dc.dataclass
        class Level1Data:
            val1: int = 0
            child: object = None

        # Define level 3 type
        level3_type = UvmObjectType(
            type_name="Level3Data",
            data_t=Level3Data,
            can_pack=True,
            fields=[
                UvmFieldType(name="val3", kind=UvmFieldKind.INT, size=8),
            ]
        )
        level3_type.field_m = {f.name: f for f in level3_type.fields}

        # Define level 2 type
        level2_type = UvmObjectType(
            type_name="Level2Data",
            data_t=Level2Data,
            can_pack=True,
            fields=[
                UvmFieldType(name="val2", kind=UvmFieldKind.INT, size=8),
                UvmFieldType(name="child", kind=UvmFieldKind.OBJ, obj_type=level3_type),
            ]
        )
        level2_type.field_m = {f.name: f for f in level2_type.fields}

        # Define level 1 type
        level1_type = UvmObjectType(
            type_name="Level1Data",
            data_t=Level1Data,
            can_pack=True,
            fields=[
                UvmFieldType(name="val1", kind=UvmFieldKind.INT, size=8),
                UvmFieldType(name="child", kind=UvmFieldKind.OBJ, obj_type=level2_type),
            ]
        )
        level1_type.field_m = {f.name: f for f in level1_type.fields}

        # Create deeply nested data
        level3 = Level3Data(val3=0x33)
        level2 = Level2Data(val2=0x22, child=level3)
        level1 = Level1Data(val1=0x11, child=level2)

        packed = level1_type.pack_ints(level1)

        # Unpack and verify all levels
        unpacked = level1_type.unpack_ints(packed)
        assert unpacked.val1 == 0x11
        assert unpacked.child is not None
        assert unpacked.child.val2 == 0x22
        assert unpacked.child.child is not None
        assert unpacked.child.child.val3 == 0x33

    def test_pack_unpack_multiple_object_fields(self):
        """Test pack/unpack with multiple object fields"""
        import dataclasses as dc

        @dc.dataclass
        class ChildA:
            val_a: int = 0

        @dc.dataclass
        class ChildB:
            val_b: int = 0

        @dc.dataclass
        class Parent:
            child_a: object = None
            child_b: object = None
            scalar: int = 0

        # Define child types
        child_a_type = UvmObjectType(
            type_name="ChildA",
            data_t=ChildA,
            can_pack=True,
            fields=[UvmFieldType(name="val_a", kind=UvmFieldKind.INT, size=8)]
        )
        child_a_type.field_m = {f.name: f for f in child_a_type.fields}

        child_b_type = UvmObjectType(
            type_name="ChildB",
            data_t=ChildB,
            can_pack=True,
            fields=[UvmFieldType(name="val_b", kind=UvmFieldKind.INT, size=16)]
        )
        child_b_type.field_m = {f.name: f for f in child_b_type.fields}

        # Define parent type
        parent_type = UvmObjectType(
            type_name="Parent",
            data_t=Parent,
            can_pack=True,
            fields=[
                UvmFieldType(name="child_a", kind=UvmFieldKind.OBJ, obj_type=child_a_type),
                UvmFieldType(name="child_b", kind=UvmFieldKind.OBJ, obj_type=child_b_type),
                UvmFieldType(name="scalar", kind=UvmFieldKind.INT, size=8),
            ]
        )
        parent_type.field_m = {f.name: f for f in parent_type.fields}

        # Create data
        child_a = ChildA(val_a=0xAA)
        child_b = ChildB(val_b=0xBBBB)
        parent = Parent(child_a=child_a, child_b=child_b, scalar=0xCC)

        packed = parent_type.pack_ints(parent)

        # Unpack and verify
        unpacked = parent_type.unpack_ints(packed)
        assert unpacked.child_a is not None
        assert unpacked.child_a.val_a == 0xAA
        assert unpacked.child_b is not None
        assert unpacked.child_b.val_b == 0xBBBB
        assert unpacked.scalar == 0xCC

    def test_pack_unpack_mixed_null_nonnull(self):
        """Test pack/unpack with a mix of null and non-null object fields"""
        import dataclasses as dc

        @dc.dataclass
        class Child:
            val: int = 0

        @dc.dataclass
        class Parent:
            child_a: object = None
            child_b: object = None

        child_type = UvmObjectType(
            type_name="Child",
            data_t=Child,
            can_pack=True,
            fields=[UvmFieldType(name="val", kind=UvmFieldKind.INT, size=8)]
        )
        child_type.field_m = {f.name: f for f in child_type.fields}

        parent_type = UvmObjectType(
            type_name="Parent",
            data_t=Parent,
            can_pack=True,
            fields=[
                UvmFieldType(name="child_a", kind=UvmFieldKind.OBJ, obj_type=child_type),
                UvmFieldType(name="child_b", kind=UvmFieldKind.OBJ, obj_type=child_type),
            ]
        )
        parent_type.field_m = {f.name: f for f in parent_type.fields}

        # First child non-null, second null
        parent = Parent(child_a=Child(val=0x55), child_b=None)
        packed = parent_type.pack_ints(parent)
        unpacked = parent_type.unpack_ints(packed)
        assert unpacked.child_a is not None
        assert unpacked.child_a.val == 0x55
        assert unpacked.child_b is None

        # First child null, second non-null
        parent2 = Parent(child_a=None, child_b=Child(val=0x77))
        packed2 = parent_type.pack_ints(parent2)
        unpacked2 = parent_type.unpack_ints(packed2)
        assert unpacked2.child_a is None
        assert unpacked2.child_b is not None
        assert unpacked2.child_b.val == 0x77


class TestUvmObjectRgyObjectFields:
    """Test cases for populate_fields with object-type fields"""

    def setup_method(self):
        """Setup method called before each test"""
        self.factory = UvmObjectRgy()

    def test_populate_fields_with_object_type_cache(self):
        """Test populate_fields recognizes object fields when type cache is provided"""
        import dataclasses as dc

        # Create a nested object type
        @dc.dataclass
        class NestedData:
            inner_val: int = 0

        nested_type = UvmObjectType(
            type_name="nested_type",
            data_t=NestedData,
            can_pack=True,
            fields=[UvmFieldType(name="inner_val", kind=UvmFieldKind.INT, size=16)]
        )
        nested_type.field_m = {f.name: f for f in nested_type.fields}

        # Layout with a type declaration line first (name, type, - size), then fields including an object
        layout = """------------------------------------------------------------------
Name          Type           Size  Value
------------------------------------------------------------------
parent_obj    parent_type    -     @123
my_data       integral       32    'h12345678
my_nested     nested_type    -     <object>
my_count      integral       16    'habcd
------------------------------------------------------------------
"""

        obj_t = UvmObjectType()
        obj_type_cache = {"nested_type": nested_type}
        self.factory.populate_fields(obj_t, layout, obj_type_cache)

        # Verify type_name was captured from the first "-" line
        assert obj_t.type_name == "parent_type"

        # Verify can_pack remains True (object field has known type)
        assert obj_t.can_pack == True

        # Verify correct number of fields
        assert len(obj_t.fields) == 3

        # Verify field details
        assert obj_t.fields[0].name == "my_data"
        assert obj_t.fields[0].kind == UvmFieldKind.INT
        assert obj_t.fields[0].size == 32

        assert obj_t.fields[1].name == "my_nested"
        assert obj_t.fields[1].kind == UvmFieldKind.OBJ
        assert obj_t.fields[1].obj_type is nested_type

        assert obj_t.fields[2].name == "my_count"
        assert obj_t.fields[2].kind == UvmFieldKind.INT
        assert obj_t.fields[2].size == 16

    def test_populate_fields_object_unknown_type(self):
        """Test populate_fields sets can_pack=False when object type is not in cache"""
        layout = """------------------------------------------------------------------
Name          Type           Size  Value
------------------------------------------------------------------
parent_obj    parent_type    -     @123
my_data       integral       32    'h12345678
my_unknown    unknown_type   -     <object>
my_count      integral       16    'habcd
------------------------------------------------------------------
"""

        obj_t = UvmObjectType()
        # Empty cache - type not found
        self.factory.populate_fields(obj_t, layout, {})

        # Verify can_pack is False due to unknown object type
        assert obj_t.can_pack == False

        # INT fields should still be parsed
        assert len(obj_t.fields) == 2
        assert obj_t.fields[0].name == "my_data"
        assert obj_t.fields[1].name == "my_count"


if __name__ == "__main__":
    pytest.main([__file__])
