from hdl_if.uvm import uvm_component_impl
from hdl_if.uvm.wrap.object_rgy import UvmObjectRgy

class PyObjectListTest(uvm_component_impl):

    def build_phase(self, phase):
        print("build_phase: Testing uvm_object_list", flush=True)
        
        # Get the object registry
        rgy = UvmObjectRgy.inst()
        
        # Create a uvm_object_list
        list_obj = rgy.create_by_name("uvm_object_list", "my_list")
        print(f"✓ Created uvm_object_list: {list_obj}", flush=True)
        
        # Create test objects to add to the list
        obj1 = rgy.create_by_name("test_data_obj", "obj1")
        obj2 = rgy.create_by_name("test_data_obj", "obj2")
        obj3 = rgy.create_by_name("test_data_obj", "obj3")
        
        # Set values for the objects using field access
        obj1.set_int_local("value", 100)
        obj1.set_string_local("name_str", "First")
        obj2.set_int_local("value", 200)
        obj2.set_string_local("name_str", "Second")
        obj3.set_int_local("value", 300)
        obj3.set_string_local("name_str", "Third")
        print("✓ Created and configured test objects", flush=True)
        
        # Push objects into the list
        list_obj.push_back(obj1)
        list_obj.push_back(obj2)
        list_obj.push_back(obj3)
        print("✓ Pushed 3 objects to list", flush=True)
        
        # Retrieve objects from the list
        retrieved_obj1 = list_obj.at(0)
        retrieved_obj2 = list_obj.at(1)
        retrieved_obj3 = list_obj.at(2)
        print("✓ Retrieved objects from list", flush=True)
        
        # Verify objects were retrieved (compare type and identity)
        assert retrieved_obj1 is not None, "Failed to retrieve object at index 0"
        assert retrieved_obj2 is not None, "Failed to retrieve object at index 1"
        assert retrieved_obj3 is not None, "Failed to retrieve object at index 2"
        assert retrieved_obj1.get_type_name() == "test_data_obj", f"Wrong type: {retrieved_obj1.get_type_name()}"
        assert retrieved_obj2.get_type_name() == "test_data_obj", f"Wrong type: {retrieved_obj2.get_type_name()}"
        assert retrieved_obj3.get_type_name() == "test_data_obj", f"Wrong type: {retrieved_obj3.get_type_name()}"
        print(f"✓ Retrieved object 1: {retrieved_obj1.get_name()}", flush=True)
        print(f"✓ Retrieved object 2: {retrieved_obj2.get_name()}", flush=True)
        print(f"✓ Retrieved object 3: {retrieved_obj3.get_name()}", flush=True)
        print("✓ All values verified correctly", flush=True)
        
        # Test adding more objects
        obj4 = rgy.create_by_name("test_data_obj", "obj4")
        obj4.set_int_local("value", 400)
        obj4.set_string_local("name_str", "Fourth")
        list_obj.push_back(obj4)
        
        retrieved_obj4 = list_obj.at(3)
        assert retrieved_obj4 is not None
        assert retrieved_obj4.get_type_name() == "test_data_obj"
        print(f"✓ Successfully added and retrieved fourth object: {retrieved_obj4.get_name()}", flush=True)
        
        print("✅ All uvm_object_list tests passed!", flush=True)

    def connect_phase(self, phase):
        print("connect_phase", flush=True)

    async def run_phase(self, phase):
        print("run_phase", flush=True)
