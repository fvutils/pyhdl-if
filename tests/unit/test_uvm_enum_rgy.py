#!/usr/bin/env python3

import pytest
import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hdl_if.uvm.wrap import uvm_enum_rgy
from enum import IntEnum


class TestUvmEnumRegistry:
    """Test cases for UVM enum registry functionality (standalone tests)"""
    
    def test_enum_rgy_instantiation(self):
        """Test that enum registry can be instantiated"""
        rgy = uvm_enum_rgy()
        assert rgy is not None
        assert hasattr(rgy, 'get_enum_type')
        assert hasattr(rgy, 'get_enum_types')
        assert hasattr(rgy, 'has_enum_type')
    
    def test_enum_rgy_cache_structure(self):
        """Test that enum registry has proper cache structure"""
        rgy = uvm_enum_rgy()
        assert hasattr(rgy, '_enum_types_cache')
        assert isinstance(rgy._enum_types_cache, dict)
    
    def test_enum_type_cache_direct(self):
        """Test direct manipulation of enum type cache"""
        rgy = uvm_enum_rgy()
        
        # Create a test enum
        class TestEnum(IntEnum):
            A = 1
            B = 2
        
        # Manually add to cache
        rgy._enum_types_cache["TestEnum"] = TestEnum
        
        # Verify it's cached
        assert "TestEnum" in rgy._enum_types_cache
        assert rgy._enum_types_cache["TestEnum"] is TestEnum


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
