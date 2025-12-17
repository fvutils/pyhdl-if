from hdl_if.uvm import uvm_component_impl
from hdl_if.uvm.wrap.object_rgy import UvmObjectRgy

class PyObjectStringTest(uvm_component_impl):

    def build_phase(self, phase):
        print("build_phase: Testing uvm_object_string", flush=True)
        
        # Get the object registry
        rgy = UvmObjectRgy.inst()
        
        # Create a uvm_object_string
        str_obj1 = rgy.create_by_name("uvm_object_string", "str_obj1")
        print(f"✓ Created uvm_object_string: {str_obj1}", flush=True)
        
        # Test setting and getting string values
        str_obj1.set_value("Hello, World!")
        value1 = str_obj1.get_value()
        assert value1 == "Hello, World!", f"Expected 'Hello, World!', got '{value1}'"
        print(f"✓ Set and retrieved value: '{value1}'", flush=True)
        
        # Test updating the value
        str_obj1.set_value("Updated value")
        value2 = str_obj1.get_value()
        assert value2 == "Updated value", f"Expected 'Updated value', got '{value2}'"
        print(f"✓ Updated and retrieved value: '{value2}'", flush=True)
        
        # Test empty string
        str_obj2 = rgy.create_by_name("uvm_object_string", "str_obj2")
        empty_val = str_obj2.get_value()
        assert empty_val == "", f"Expected empty string, got '{empty_val}'"
        print("✓ Verified empty string default", flush=True)
        
        # Test various string values
        test_strings = [
            "Simple text",
            "Text with spaces and punctuation!",
            "12345",
            "Special chars: @#$%^&*()",
            "Multi\nLine\nString"
        ]
        
        for i, test_str in enumerate(test_strings):
            str_obj = rgy.create_by_name("uvm_object_string", f"test_str_{i}")
            str_obj.set_value(test_str)
            retrieved = str_obj.get_value()
            assert retrieved == test_str, f"String mismatch: expected '{test_str}', got '{retrieved}'"
        print(f"✓ Successfully tested {len(test_strings)} different string values", flush=True)
        
        # Test using uvm_object_string in a list
        list_obj = rgy.create_by_name("uvm_object_list", "string_list")
        str_a = rgy.create_by_name("uvm_object_string", "str_a")
        str_b = rgy.create_by_name("uvm_object_string", "str_b")
        str_c = rgy.create_by_name("uvm_object_string", "str_c")
        
        str_a.set_value("First")
        str_b.set_value("Second")
        str_c.set_value("Third")
        
        list_obj.push_back(str_a)
        list_obj.push_back(str_b)
        list_obj.push_back(str_c)
        
        retrieved_a = list_obj.at(0)
        retrieved_b = list_obj.at(1)
        retrieved_c = list_obj.at(2)
        
        assert retrieved_a.get_value() == "First"
        assert retrieved_b.get_value() == "Second"
        assert retrieved_c.get_value() == "Third"
        print("✓ Successfully used uvm_object_string in a list", flush=True)
        
        # Test using uvm_object_string in a map
        map_obj = rgy.create_by_name("uvm_object_map", "string_map")
        str_x = rgy.create_by_name("uvm_object_string", "str_x")
        str_y = rgy.create_by_name("uvm_object_string", "str_y")
        str_z = rgy.create_by_name("uvm_object_string", "str_z")
        
        str_x.set_value("Value X")
        str_y.set_value("Value Y")
        str_z.set_value("Value Z")
        
        map_obj.set("key_x", str_x)
        map_obj.set("key_y", str_y)
        map_obj.set("key_z", str_z)
        
        assert map_obj.has_key("key_x")
        assert map_obj.has_key("key_y")
        assert map_obj.has_key("key_z")
        
        retrieved_x = map_obj.get("key_x")
        retrieved_y = map_obj.get("key_y")
        retrieved_z = map_obj.get("key_z")
        
        assert retrieved_x.get_value() == "Value X"
        assert retrieved_y.get_value() == "Value Y"
        assert retrieved_z.get_value() == "Value Z"
        print("✓ Successfully used uvm_object_string in a map", flush=True)
        
        print("✅ All uvm_object_string tests passed!", flush=True)

    def connect_phase(self, phase):
        print("connect_phase", flush=True)

    async def run_phase(self, phase):
        print("run_phase", flush=True)
