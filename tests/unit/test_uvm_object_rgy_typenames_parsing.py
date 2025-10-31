#!/usr/bin/env python3
import os
import sys

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from typing import Any
from hdl_if.uvm.wrap.uvm_object_rgy import UvmObjectRgy

def test_parse_typedump_factory_configuration():
    """Test the _parse_typedump method with the expected factory configuration format"""
    
    # Sample factory configuration output as specified in the task
    sample_typedump = """#### Factory Configuration (*)

  No instance or type overrides are registered with this factory

All types registered with the factory: 62 total
  Type Name
  ---------
  base_test
  my_driver
  my_env
  my_sequencer
  pyhdl_uvm2py
  pyhdl_uvm_component_proxy
  questa_uvm_recorder
  seq_item
  <unknown>
  another_test
  pyhdl_internal_type
(*) Types with no associated type name will be printed as <unknown>"""

    # Create registry instance
    rgy: Any = UvmObjectRgy()  # type: ignore  # Pylance: @api wrapper is generic; treat as Any
    
    # Test the parsing method
    result = rgy._parse_typedump(sample_typedump)
    
    # Expected results (filtered according to task requirements)
    expected = [
        "base_test",
        "my_driver", 
        "my_env",
        "my_sequencer",
        "questa_uvm_recorder",
        "seq_item",
        "another_test"
    ]
    
    # Verify filtering worked correctly
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Verify pyhdl_ types were filtered out
    assert "pyhdl_uvm2py" not in result
    assert "pyhdl_uvm_component_proxy" not in result
    assert "pyhdl_internal_type" not in result
    
    # Verify <unknown> was filtered out
    assert "<unknown>" not in result

def test_parse_typedump_empty_cases():
    """Test with empty or invalid typedump"""
    rgy: Any = UvmObjectRgy()  # type: ignore  # Pylance: @api wrapper is generic; treat as Any
    
    # Test empty string
    result = rgy._parse_typedump("")
    assert result == []
    
    # Test string without proper format
    result = rgy._parse_typedump("No types found")
    assert result == []
    
    # Test string with header but no types
    no_types_dump = """#### Factory Configuration (*)
  Type Name
  ---------
(*) Types with no associated type name will be printed as <unknown>"""
    
    result = rgy._parse_typedump(no_types_dump)
    assert result == []

def test_parse_typedump_all_filtered():
    """Test case where all types are filtered out"""
    filtered_dump = """#### Factory Configuration (*)
  Type Name
  ---------
  pyhdl_test1
  pyhdl_test2
  <unknown>
  pyhdl_another
(*) Types with no associated type name will be printed as <unknown>"""
    
    rgy: Any = UvmObjectRgy()  # type: ignore  # Pylance: @api wrapper is generic; treat as Any
    result = rgy._parse_typedump(filtered_dump)
    
    # All types should be filtered out
    assert result == []

if __name__ == "__main__":
    test_parse_typedump_factory_configuration()
    test_parse_typedump_empty_cases()
    test_parse_typedump_all_filtered()
    print("All typedump parsing tests passed!")
