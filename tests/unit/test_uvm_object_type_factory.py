#!/usr/bin/env python3

import pytest
import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hdl_if.uvm.wrap import UvmObjectType, UvmFieldType, UvmFieldKind, UvmObjectRgy


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


if __name__ == "__main__":
    pytest.main([__file__])
