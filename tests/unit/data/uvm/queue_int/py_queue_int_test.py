from hdl_if.uvm import uvm_component_impl
from hdl_if.uvm.wrap.object_rgy import UvmObjectRgy

class PyQueueIntTest(uvm_component_impl):

    def build_phase(self, phase):
        print("build_phase: Testing uvm_field_queue_int pack/unpack", flush=True)
        
        # Get the object registry
        rgy = UvmObjectRgy.inst()
        
        # Test 1: Basic pack/unpack (empty queues)
        print("\n=== Test 1: Basic pack/unpack (empty queues) ===", flush=True)
        obj1 = rgy.create_by_name("test_queue_data", "obj1")
        
        packed_bits = obj1.pack_ints()
        print(f"✓ Packed object, got {len(packed_bits)} ints", flush=True)
        
        obj1_unpacked = rgy.create_by_name("test_queue_data", "obj1_unpacked")
        obj1_unpacked.unpack_ints(packed_bits)
        
        unpacked_data = obj1_unpacked.pack()
        assert len(unpacked_data.queue_8bit) == 0, f"Expected empty queue_8bit"
        assert len(unpacked_data.queue_16bit) == 0, f"Expected empty queue_16bit"
        assert len(unpacked_data.queue_signed) == 0, f"Expected empty queue_signed"
        print(f"✓ Unpacked successfully: all queues empty", flush=True)
        
        # Test 2: Copy then pack/unpack
        print("\n=== Test 2: Copy then pack/unpack ===", flush=True)
        obj2 = rgy.create_by_name("test_queue_data", "obj2")
        
        obj2_copy = rgy.create_by_name("test_queue_data", "obj2_copy")
        obj2_copy.copy(obj2)
        
        packed_bits2 = obj2_copy.pack_ints()
        print(f"✓ Packed copied object, got {len(packed_bits2)} ints", flush=True)
        
        obj2_unpacked = rgy.create_by_name("test_queue_data", "obj2_unpacked")
        obj2_unpacked.unpack_ints(packed_bits2)
        
        unpacked_data2 = obj2_unpacked.pack()
        assert len(unpacked_data2.queue_8bit) == 0
        assert len(unpacked_data2.queue_16bit) == 0
        assert len(unpacked_data2.queue_signed) == 0
        print(f"✓ Unpacked successfully after copy", flush=True)
        
        # Test 3: Multiple pack/unpack cycles
        print("\n=== Test 3: Multiple pack/unpack cycles ===", flush=True)
        obj3 = rgy.create_by_name("test_queue_data", "obj3")
        
        # First cycle
        packed_bits3_1 = obj3.pack_ints()
        obj3_temp = rgy.create_by_name("test_queue_data", "obj3_temp")
        obj3_temp.unpack_ints(packed_bits3_1)
        
        # Second cycle
        packed_bits3_2 = obj3_temp.pack_ints()
        obj3_final = rgy.create_by_name("test_queue_data", "obj3_final")
        obj3_final.unpack_ints(packed_bits3_2)
        
        unpacked_data3 = obj3_final.pack()
        assert len(unpacked_data3.queue_8bit) == 0
        assert len(unpacked_data3.queue_16bit) == 0
        assert len(unpacked_data3.queue_signed) == 0
        print(f"✓ Multiple cycles successful", flush=True)
        
        # Test 4: Compare objects
        print("\n=== Test 4: Compare objects ===", flush=True)
        obj4a = rgy.create_by_name("test_queue_data", "obj4a")
        obj4b = rgy.create_by_name("test_queue_data", "obj4b")
        
        # Compare should return true for two default-constructed objects
        result = obj4a.compare(obj4b)
        assert result == True, f"Expected compare to return True for identical objects"
        print(f"✓ Compare successful: objects are identical", flush=True)
        
        # Test 5: Randomize then pack/unpack
        print("\n=== Test 5: Randomize then pack/unpack ===", flush=True)
        obj5 = rgy.create_by_name("test_queue_data", "obj5")
        obj5.randomize()
        
        data_before = obj5.pack()
        packed_bits5 = obj5.pack_ints()
        
        obj5_unpacked = rgy.create_by_name("test_queue_data", "obj5_unpacked")
        obj5_unpacked.unpack_ints(packed_bits5)
        
        data_after = obj5_unpacked.pack()
        assert data_after.scalar_field == data_before.scalar_field
        assert data_after.queue_8bit == data_before.queue_8bit
        assert data_after.queue_16bit == data_before.queue_16bit
        assert data_after.queue_signed == data_before.queue_signed
        print(f"✓ Randomized object pack/unpack successful", flush=True)
        
        print("\n✅ All uvm_field_queue_int pack/unpack tests passed!", flush=True)

    def connect_phase(self, phase):
        print("connect_phase", flush=True)

    async def run_phase(self, phase):
        print("run_phase", flush=True)
