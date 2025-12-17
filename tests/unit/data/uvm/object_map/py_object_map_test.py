from hdl_if.uvm import uvm_component_impl
from hdl_if.uvm.wrap.object_rgy import UvmObjectRgy

class PyObjectMapTest(uvm_component_impl):

    def build_phase(self, phase):
        print("build_phase: Testing uvm_object_map", flush=True)
        
        # Get the object registry
        rgy = UvmObjectRgy.inst()
        
        # Create a uvm_object_map
        map_obj = rgy.create_by_name("uvm_object_map", "my_map")
        print(f"✓ Created uvm_object_map: {map_obj}", flush=True)
        
        # Create test objects to add to the map
        cfg1 = rgy.create_by_name("test_config_obj", "cfg1")
        cfg2 = rgy.create_by_name("test_config_obj", "cfg2")
        cfg3 = rgy.create_by_name("test_config_obj", "cfg3")
        
        # Set configuration values using field access
        cfg1.set_int_local("cfg_value", 100)
        cfg1.set_string_local("cfg_name", "Config_A")
        cfg2.set_int_local("cfg_value", 200)
        cfg2.set_string_local("cfg_name", "Config_B")
        cfg3.set_int_local("cfg_value", 300)
        cfg3.set_string_local("cfg_name", "Config_C")
        print("✓ Created and configured test objects", flush=True)
        
        # Test has_key before adding (should be False)
        assert not map_obj.has_key("key1"), "Key should not exist before adding"
        assert not map_obj.has_key("key2"), "Key should not exist before adding"
        print("✓ has_key() correctly returns False for non-existent keys", flush=True)
        
        # Add objects to the map with string keys
        map_obj.set("key1", cfg1)
        map_obj.set("key2", cfg2)
        map_obj.set("key3", cfg3)
        print("✓ Added 3 objects to map with keys", flush=True)
        
        # Test has_key after adding (should be True)
        assert map_obj.has_key("key1"), "Key1 should exist after adding"
        assert map_obj.has_key("key2"), "Key2 should exist after adding"
        assert map_obj.has_key("key3"), "Key3 should exist after adding"
        assert not map_obj.has_key("key4"), "Key4 should not exist"
        print("✓ has_key() correctly identifies existing and non-existing keys", flush=True)
        
        # Retrieve objects from the map
        retrieved_cfg1 = map_obj.get("key1")
        retrieved_cfg2 = map_obj.get("key2")
        retrieved_cfg3 = map_obj.get("key3")
        print("✓ Retrieved objects from map", flush=True)
        
        # Verify objects were retrieved (compare type and identity)
        assert retrieved_cfg1 is not None, "Failed to retrieve object for key1"
        assert retrieved_cfg2 is not None, "Failed to retrieve object for key2"
        assert retrieved_cfg3 is not None, "Failed to retrieve object for key3"
        assert retrieved_cfg1.get_type_name() == "test_config_obj", f"Wrong type: {retrieved_cfg1.get_type_name()}"
        assert retrieved_cfg2.get_type_name() == "test_config_obj", f"Wrong type: {retrieved_cfg2.get_type_name()}"
        assert retrieved_cfg3.get_type_name() == "test_config_obj", f"Wrong type: {retrieved_cfg3.get_type_name()}"
        print(f"✓ Retrieved config 1: {retrieved_cfg1.get_name()}", flush=True)
        print(f"✓ Retrieved config 2: {retrieved_cfg2.get_name()}", flush=True)
        print(f"✓ Retrieved config 3: {retrieved_cfg3.get_name()}", flush=True)
        print("✓ All objects verified correctly", flush=True)
        
        # Test updating an existing key
        cfg1_updated = rgy.create_by_name("test_config_obj", "cfg1_updated")
        cfg1_updated.set_int_local("cfg_value", 999)
        cfg1_updated.set_string_local("cfg_name", "Updated_A")
        map_obj.set("key1", cfg1_updated)
        
        retrieved_updated = map_obj.get("key1")
        assert retrieved_updated is not None
        assert retrieved_updated.get_type_name() == "test_config_obj"
        print(f"✓ Successfully updated existing key: {retrieved_updated.get_name()}", flush=True)
        
        # Test with various key names
        test_keys = ["config.addr", "config_value_123", "my-config", "CFG_UPPER"]
        for i, key in enumerate(test_keys):
            obj = rgy.create_by_name("test_config_obj", f"obj_{i}")
            obj.set_int_local("cfg_value", i * 10)
            obj.set_string_local("cfg_name", f"Value_{i}")
            map_obj.set(key, obj)
            assert map_obj.has_key(key), f"Key '{key}' should exist"
            retrieved = map_obj.get(key)
            assert retrieved is not None
            assert retrieved.get_type_name() == "test_config_obj"
        print("✓ Successfully tested various key name formats", flush=True)
        
        print("✅ All uvm_object_map tests passed!", flush=True)

    def connect_phase(self, phase):
        print("connect_phase", flush=True)

    async def run_phase(self, phase):
        print("run_phase", flush=True)
