"""
Python test script for enum registry integration test
"""
import hdl_if
from hdl_if.uvm.wrap import uvm_enum_rgy

def test_enum_registry():
    """Test enum registry from Python side"""
    print("Python: Testing enum registry")
    
    # Get the enum registry instance
    rgy = uvm_enum_rgy.inst()
    
    # Get all registered enum types
    enum_types = rgy.get_enum_types()
    print(f"Python: Found {len(enum_types)} enum types: {enum_types}")
    
    # Test each enum type
    for enum_name in ["color_e", "state_e", "operation_e"]:
        if enum_name in enum_types:
            print(f"Python: Testing {enum_name}")
            
            # Get the enum type
            enum_type = rgy.get_enum_type(enum_name)
            if enum_type:
                print(f"Python:   Got enum type: {enum_type}")
                print(f"Python:   Members: {list(enum_type.__members__.keys())}")
                print(f"Python:   Values: {[e.value for e in enum_type]}")
            else:
                print(f"Python:   FAIL: Could not get enum type for {enum_name}")
        else:
            print(f"Python: WARNING: {enum_name} not in registered types")
    
    print("Python: Enum registry tests complete")

if __name__ == "__main__":
    test_enum_registry()
