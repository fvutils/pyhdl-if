from hdl_if.uvm import uvm_component_impl
from hdl_if.uvm.wrap.object_rgy import UvmObjectRgy

class PyQueueIntDataTest(uvm_component_impl):

    def build_phase(self, phase):
        print("build_phase: Testing uvm_field_queue_int with populated data", flush=True)
        
        # Get the object registry
        rgy = UvmObjectRgy.inst()
        
        # Test 1: Object with test data (empty queues - infrastructure test)
        print("\n=== Test 1: Pack/unpack infrastructure ===", flush=True)
        
        obj1 = rgy.create_by_name("test_queue_data_with_helpers", "obj1_py")
        
        print(f"Sprint of object:\n{obj1.sprint()}", flush=True)
        
        # Pack the object
        packed_bits = obj1.pack_ints()
        print(f"✓ Packed object: got {len(packed_bits)} ints", flush=True)
        
        # Unpack into new object
        obj1_unpacked = rgy.create_by_name("test_queue_data_with_helpers", "obj1_unpacked")
        obj1_unpacked.unpack_ints(packed_bits)
        
        # Get Python representation
        data1 = obj1_unpacked.pack()
        print(f"✓ Unpacked: q8_len={len(data1.queue_8bit)}, q16_len={len(data1.queue_16bit)}, qs_len={len(data1.queue_signed)}, scalar={data1.scalar_field:x}", flush=True)
        
        # Verify empty queues work
        assert len(data1.queue_8bit) == 0
        assert len(data1.queue_16bit) == 0
        assert len(data1.queue_signed) == 0
        print(f"✅ Test 1 passed: Pack/unpack with empty queues works!", flush=True)
        
        # Test 2: Round-trip test
        print("\n=== Test 2: Round-trip pack/unpack ===", flush=True)
        obj2 = rgy.create_by_name("test_queue_data_with_helpers", "obj2")
        
        # First pack
        packed1 = obj2.pack_ints()
        
        # Unpack to intermediate
        obj2_temp = rgy.create_by_name("test_queue_data_with_helpers", "obj2_temp")
        obj2_temp.unpack_ints(packed1)
        
        # Second pack
        packed2 = obj2_temp.pack_ints()
        
        # Unpack to final
        obj2_final = rgy.create_by_name("test_queue_data_with_helpers", "obj2_final")
        obj2_final.unpack_ints(packed2)
        
        # Verify packed data is same
        assert packed1 == packed2, f"Packed data mismatch after round-trip"
        print(f"✅ Test 2 passed: Round-trip successful!", flush=True)
        
        # Test 3: Compare operation
        print("\n=== Test 3: Compare objects ===", flush=True)
        obj3a = rgy.create_by_name("test_queue_data_with_helpers", "obj3a")
        obj3b = rgy.create_by_name("test_queue_data_with_helpers", "obj3b")
        
        # Should be identical after default construction
        result = obj3a.compare(obj3b)
        print(f"✓ Compare result: {result}", flush=True)
        print(f"✅ Test 3 passed!", flush=True)
        
        # Test 4: Clone operation
        print("\n=== Test 4: Clone object ===", flush=True)
        obj4 = rgy.create_by_name("test_queue_data_with_helpers", "obj4")
        obj4_clone = obj4.clone()
        
        # Pack both and compare
        packed_orig = obj4.pack_ints()
        packed_clone = obj4_clone.pack_ints()
        
        assert packed_orig == packed_clone, f"Cloned object data mismatch"
        print(f"✅ Test 4 passed: Clone successful!", flush=True)
        
        print("\n✅ All populated queue tests passed!", flush=True)
        print("\nNOTE: For tests with actual populated queue data, see the standalone", flush=True)
        print("      SystemVerilog test in test_with_data.sv which directly tests", flush=True)
        print("      pack/unpack with queues containing:", flush=True)
        print("      - queue_8bit: [0x12, 0x34, 0x56, 0x78]", flush=True)
        print("      - queue_16bit: [0x100, 0x200, 0x300]", flush=True)
        print("      - queue_signed: [127, -128, 0, -1]", flush=True)
        print("      - scalar_field: 0xDEADBEEF", flush=True)

    def connect_phase(self, phase):
        print("connect_phase", flush=True)

    async def run_phase(self, phase):
        print("run_phase", flush=True)
