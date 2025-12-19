#!/usr/bin/env python3

import pytest
import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hdl_if.uvm.wrap import UvmObjectType, UvmFieldType, UvmFieldKind
import dataclasses as dc


class TestUvmFieldQueueInt:
    """Test cases for UVM queue-type field registration and pack/unpack functionality"""
    
    def test_pack_unpack_queue_int_basic(self):
        """Test basic pack/unpack with a queue of integers"""
        
        @dc.dataclass
        class QueueData:
            my_queue: list = dc.field(default_factory=list)
            scalar_field: int = 0
        
        # Define object type with a queue field
        obj_type = UvmObjectType(
            type_name="QueueData",
            data_t=QueueData,
            can_pack=True,
            fields=[
                UvmFieldType(name="my_queue", kind=UvmFieldKind.QUEUE, size=8, is_signed=False),
                UvmFieldType(name="scalar_field", kind=UvmFieldKind.INT, size=16),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create data with queue and pack
        data = QueueData(my_queue=[0x12, 0x34, 0x56], scalar_field=0xABCD)
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.my_queue == [0x12, 0x34, 0x56]
        assert unpacked.scalar_field == 0xABCD
    
    def test_pack_unpack_empty_queue(self):
        """Test pack/unpack with an empty queue"""
        
        @dc.dataclass
        class QueueData:
            my_queue: list = dc.field(default_factory=list)
            marker: int = 0
        
        obj_type = UvmObjectType(
            type_name="QueueData",
            data_t=QueueData,
            can_pack=True,
            fields=[
                UvmFieldType(name="my_queue", kind=UvmFieldKind.QUEUE, size=32),
                UvmFieldType(name="marker", kind=UvmFieldKind.INT, size=8),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create data with empty queue
        data = QueueData(my_queue=[], marker=0xFF)
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.my_queue == []
        assert unpacked.marker == 0xFF
    
    def test_pack_unpack_single_element_queue(self):
        """Test pack/unpack with a single-element queue"""
        
        @dc.dataclass
        class QueueData:
            single_queue: list = dc.field(default_factory=list)
        
        obj_type = UvmObjectType(
            type_name="QueueData",
            data_t=QueueData,
            can_pack=True,
            fields=[
                UvmFieldType(name="single_queue", kind=UvmFieldKind.QUEUE, size=16),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create data with single element
        data = QueueData(single_queue=[0x5A5A])
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.single_queue == [0x5A5A]
    
    def test_pack_unpack_large_queue(self):
        """Test pack/unpack with a larger queue"""
        
        @dc.dataclass
        class QueueData:
            data_queue: list = dc.field(default_factory=list)
        
        obj_type = UvmObjectType(
            type_name="QueueData",
            data_t=QueueData,
            can_pack=True,
            fields=[
                UvmFieldType(name="data_queue", kind=UvmFieldKind.QUEUE, size=8),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create data with many elements
        original_values = list(range(20))
        data = QueueData(data_queue=original_values)
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.data_queue == original_values
    
    def test_pack_unpack_multiple_queues(self):
        """Test pack/unpack with multiple queue fields"""
        
        @dc.dataclass
        class MultiQueueData:
            queue_a: list = dc.field(default_factory=list)
            queue_b: list = dc.field(default_factory=list)
            scalar: int = 0
        
        obj_type = UvmObjectType(
            type_name="MultiQueueData",
            data_t=MultiQueueData,
            can_pack=True,
            fields=[
                UvmFieldType(name="queue_a", kind=UvmFieldKind.QUEUE, size=8),
                UvmFieldType(name="queue_b", kind=UvmFieldKind.QUEUE, size=16),
                UvmFieldType(name="scalar", kind=UvmFieldKind.INT, size=32),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create data with multiple queues
        data = MultiQueueData(
            queue_a=[1, 2, 3],
            queue_b=[0x100, 0x200, 0x300, 0x400],
            scalar=0xDEADBEEF
        )
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.queue_a == [1, 2, 3]
        assert unpacked.queue_b == [0x100, 0x200, 0x300, 0x400]
        assert unpacked.scalar == 0xDEADBEEF
    
    def test_pack_unpack_queue_with_signed_elements(self):
        """Test pack/unpack with a queue of signed integers"""
        
        @dc.dataclass
        class SignedQueueData:
            signed_queue: list = dc.field(default_factory=list)
        
        obj_type = UvmObjectType(
            type_name="SignedQueueData",
            data_t=SignedQueueData,
            can_pack=True,
            fields=[
                UvmFieldType(name="signed_queue", kind=UvmFieldKind.QUEUE, size=8, is_signed=True),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create data with signed values (including negative)
        data = SignedQueueData(signed_queue=[127, -128, 0, -1, 50])
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.signed_queue == [127, -128, 0, -1, 50]
    
    def test_pack_unpack_queue_with_value_masking(self):
        """Test that values larger than size are properly masked"""
        
        @dc.dataclass
        class QueueData:
            my_queue: list = dc.field(default_factory=list)
        
        obj_type = UvmObjectType(
            type_name="QueueData",
            data_t=QueueData,
            can_pack=True,
            fields=[
                UvmFieldType(name="my_queue", kind=UvmFieldKind.QUEUE, size=4),
            ]
        )
        obj_type.field_m = {f.name: f for f in obj_type.fields}
        
        # Create data with values that exceed 4 bits (should be masked)
        data = QueueData(my_queue=[0xFF, 0xAB, 0x05])
        packed = obj_type.pack_ints(data)
        
        # Unpack and verify - values should be masked to 4 bits
        unpacked = obj_type.unpack_ints(packed)
        assert unpacked.my_queue == [0xF, 0xB, 0x5]
    
    def test_pack_unpack_mixed_fields(self):
        """Test pack/unpack with queues, scalars, and objects mixed"""
        
        @dc.dataclass
        class InnerData:
            inner_val: int = 0
        
        @dc.dataclass
        class MixedData:
            scalar1: int = 0
            queue1: list = dc.field(default_factory=list)
            scalar2: int = 0
            queue2: list = dc.field(default_factory=list)
            nested: object = None
        
        # Define inner type
        inner_type = UvmObjectType(
            type_name="InnerData",
            data_t=InnerData,
            can_pack=True,
            fields=[
                UvmFieldType(name="inner_val", kind=UvmFieldKind.INT, size=16),
            ]
        )
        inner_type.field_m = {f.name: f for f in inner_type.fields}
        
        # Define mixed type
        mixed_type = UvmObjectType(
            type_name="MixedData",
            data_t=MixedData,
            can_pack=True,
            fields=[
                UvmFieldType(name="scalar1", kind=UvmFieldKind.INT, size=8),
                UvmFieldType(name="queue1", kind=UvmFieldKind.QUEUE, size=8),
                UvmFieldType(name="scalar2", kind=UvmFieldKind.INT, size=8),
                UvmFieldType(name="queue2", kind=UvmFieldKind.QUEUE, size=16),
                UvmFieldType(name="nested", kind=UvmFieldKind.OBJ, obj_type=inner_type),
            ]
        )
        mixed_type.field_m = {f.name: f for f in mixed_type.fields}
        
        # Create data
        inner = InnerData(inner_val=0x1234)
        data = MixedData(
            scalar1=0xAA,
            queue1=[1, 2, 3],
            scalar2=0xBB,
            queue2=[0x100, 0x200],
            nested=inner
        )
        packed = mixed_type.pack_ints(data)
        
        # Unpack and verify
        unpacked = mixed_type.unpack_ints(packed)
        assert unpacked.scalar1 == 0xAA
        assert unpacked.queue1 == [1, 2, 3]
        assert unpacked.scalar2 == 0xBB
        assert unpacked.queue2 == [0x100, 0x200]
        assert unpacked.nested is not None
        assert unpacked.nested.inner_val == 0x1234


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
