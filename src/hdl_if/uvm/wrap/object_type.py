from __future__ import annotations
import dataclasses as dc
from typing import Dict, List, Optional, Type
from enum import Enum

class UvmFieldKind(Enum):
    INT = "int"
    STR = "str"
    OBJ = "obj"
    QUEUE = "queue"
    ENUM = "enum"

@dc.dataclass
class UvmFieldType(object):
    name: str
    kind: UvmFieldKind = UvmFieldKind.INT
    size: int = -1
    is_signed: bool = False
    obj_type: Optional['uvm_object_type'] = None
    enum_type_name: Optional[str] = None  # For ENUM fields, the name of the enum type
    enum_type: Optional[Type] = None  # For ENUM fields, the Python IntEnum type
    size_unknown: bool = False  # For QUEUE fields, True if element size needs to be determined from data

@dc.dataclass
class UvmObjectType(object):
    super_t : Optional[str] = dc.field(default=None)  # Make optional to allow zero-arg construction in tests
    can_pack : bool = dc.field(default=True)
    data_t : Optional[Type] = dc.field(default=None)
    fields : List[UvmFieldType] = dc.field(default_factory=list)
    field_m : Dict[str,UvmFieldType] = dc.field(default_factory=dict)
    type_name : Optional[str] = dc.field(default=None)

    def _sanitize_field_name(self, name: str) -> str:
        """
        Matches the sanitize logic used when building data_t in UvmObjectRgy.
        Ensures we can map field names from SV sprint output to Python dataclass attributes.
        """
        s = ''.join((c if (c.isalnum() or c == '_') else '_') for c in name)
        if not s or s[0].isdigit():
            s = f"f_{s}"
        return s

    def _total_pack_bits(self) -> int:
        """
        Computes the total number of bits required to pack all fields.
        For OBJ fields, includes 4-bit header plus recursively computed object bits.
        For QUEUE fields, includes 32-bit size header plus maximum possible element bits.
        For ENUM fields, uses the field size.
        Raises if any INT/ENUM field has unknown/invalid size.
        """
        total = 0
        for f in self.fields:
            if f.kind == UvmFieldKind.INT or f.kind == UvmFieldKind.ENUM:
                if f.size is None or f.size <= 0:
                    raise ValueError(f"Invalid size for field '{f.name}': {f.size}")
                total += f.size
            elif f.kind == UvmFieldKind.OBJ:
                # 4-bit null/non-null header
                total += 4
                # If object type is known, add its total bits (non-null case)
                if f.obj_type is not None:
                    total += f.obj_type._total_pack_bits()
            elif f.kind == UvmFieldKind.QUEUE:
                # 32-bit size header + variable number of elements
                # Note: This is an upper bound; actual may be smaller
                total += 32
                # We can't compute exact size without knowing queue length at runtime
                # This is only used for estimation
            else:
                raise NotImplementedError(f"Unsupported field kind: {f.kind}")
        return total

    def _pack_bits(self, data_obj: object, bits: List[int]) -> None:
        """
        Internal helper: packs fields from data_obj into the bits list (MSB-first).
        Handles INT, ENUM, OBJ, and QUEUE fields recursively.
        """
        for f in self.fields:
            attr = self._sanitize_field_name(f.name)
            if not hasattr(data_obj, attr):
                raise AttributeError(f"Data object missing attribute for field '{f.name}' (attr='{attr}')")

            v = getattr(data_obj, attr)

            if f.kind == UvmFieldKind.INT:
                size = f.size
                if size is None or size <= 0:
                    raise ValueError(f"Invalid size for field '{f.name}': {size}")
                if not isinstance(v, int):
                    raise TypeError(f"Field '{f.name}' value must be int, got {type(v)!r}")

                # Mask to width (two's complement for negative values handled by masking)
                mask = (1 << size) - 1
                v_masked = v & mask

                # Append bits MSB -> LSB
                for i in range(size - 1, -1, -1):
                    bits.append((v_masked >> i) & 1)

            elif f.kind == UvmFieldKind.ENUM:
                size = f.size
                if size is None or size <= 0:
                    raise ValueError(f"Invalid size for field '{f.name}': {size}")
                
                # Extract integer value from enum (supports both IntEnum instances and plain ints)
                if hasattr(v, 'value'):
                    int_val = v.value
                elif isinstance(v, int):
                    int_val = v
                else:
                    raise TypeError(f"Enum field '{f.name}' value must be IntEnum or int, got {type(v)!r}")

                # Mask to width
                mask = (1 << size) - 1
                v_masked = int_val & mask

                # Append bits MSB -> LSB
                for i in range(size - 1, -1, -1):
                    bits.append((v_masked >> i) & 1)

            elif f.kind == UvmFieldKind.OBJ:
                # Pack 4-bit header: 0 for null, 0xF for non-null
                if v is None:
                    # null object: pack 4 zero bits
                    bits.extend([0, 0, 0, 0])
                else:
                    # non-null object: pack 0xF (4 one bits), then recursively pack object
                    bits.extend([1, 1, 1, 1])
                    if f.obj_type is None:
                        raise ValueError(f"Object field '{f.name}' has no obj_type defined")
                    f.obj_type._pack_bits(v, bits)

            elif f.kind == UvmFieldKind.QUEUE:
                # Pack queue: 32-bit size header, then elements
                if not isinstance(v, list):
                    raise TypeError(f"Queue field '{f.name}' value must be list, got {type(v)!r}")
                
                size = f.size
                
                # If element size is unknown, try to infer it from the packed bits
                # This happens when the queue was empty during initial introspection
                if f.size_unknown or size is None or size <= 0:
                    # We need to infer the size from SystemVerilog's packed data
                    # For now, if we're packing from Python, we can't determine this
                    # So we'll need to get it from an actual pack operation first
                    if len(v) == 0:
                        # Empty queue - just pack the length as 0
                        queue_len = 0
                        for i in range(31, -1, -1):
                            bits.append((queue_len >> i) & 1)
                        continue
                    else:
                        # Non-empty queue but size unknown - this shouldn't happen
                        # when packing from Python to SV, only when unpacking
                        raise ValueError(f"Cannot pack queue field '{f.name}' with unknown element size and non-empty data")
                
                # Pack queue length as 32-bit unsigned integer
                queue_len = len(v)
                for i in range(31, -1, -1):
                    bits.append((queue_len >> i) & 1)
                
                # Pack each element
                mask = (1 << size) - 1
                for elem in v:
                    if not isinstance(elem, int):
                        raise TypeError(f"Queue field '{f.name}' element must be int, got {type(elem)!r}")
                    elem_masked = elem & mask
                    for i in range(size - 1, -1, -1):
                        bits.append((elem_masked >> i) & 1)

            else:
                raise NotImplementedError(f"Unsupported field kind for packing: {f.kind}")

    def pack_ints(self, data_obj: object) -> List[int]:
        """
        Packs fields from the provided data object into a list of 32-bit ints.
        Semantics mirror UVM uvm_object::pack_ints + uvm_packer.get_ints with big_endian=1:
        - Fields are appended MSB-first into a bitstream.
        - For OBJ fields, a 4-bit header (0=null, 0xF=non-null) is packed, then object fields recursively.
        - The bitstream is chunked into 32-bit words.
        - Each 32-bit word is bit-reversed before being emitted (matching get_ints big_endian behavior).
        - The last partial word is zero-padded; significant bits end up in the MSB positions of the returned int.
        Returns:
            List[int]: 32-bit words representing the packed bitstream.
        """
        if not self.can_pack:
            raise ValueError("Packing disabled due to unknown field sizes or unsupported kinds (can_pack=False)")
        if self.data_t is None:
            raise ValueError("data_t is not defined for this UvmObjectType (%s)" % self.type_name)

        # Build MSB-first bitstream from fields
        bits: List[int] = []
        self._pack_bits(data_obj, bits)

        if not bits:
            return []

        # Convert to 32-bit ints per UVM get_ints with big_endian=1 (reverse bits within each 32-bit word)
        n = len(bits)
        words = (n + 31) // 32
        out: List[int] = []
        for wi in range(words):
            # Collect 32 source bits (MSB-first slice of m_bits)
            word_bits = [0] * 32
            base = wi * 32
            for k in range(32):
                idx = base + k
                word_bits[k] = bits[idx] if idx < n else 0

            # Reverse bit order within the 32-bit word (big_endian behavior)
            v = 0
            for j in range(32):
                b = word_bits[31 - j]
                if b:
                    v |= (1 << j)

            # Do NOT mask after reversal; UVM get_ints masks before reversal so resulting ints'
            # significant bits in the last word reside in MSB positions.
            out.append(v)

        return out

    def _unpack_bits(self, bits: List[int], offset: int, data: object) -> int:
        """
        Internal helper: unpacks fields from bits starting at offset into data object.
        Handles INT, ENUM, OBJ, and QUEUE fields recursively.
        Returns the new offset after unpacking all fields.
        """
        for f in self.fields:
            attr = self._sanitize_field_name(f.name)

            if f.kind == UvmFieldKind.INT:
                size = f.size
                if size is None or size <= 0:
                    raise ValueError(f"Invalid size for field '{f.name}': {size}")

                seg = bits[offset:offset + size]
                offset += size

                # Convert MSB-first segment to integer
                val = 0
                for b in seg:
                    val = (val << 1) | (1 if b else 0)

                # Interpret signed if requested (two's complement)
                if f.is_signed and size > 0:
                    sign_bit = 1 << (size - 1)
                    if val & sign_bit:
                        val -= (1 << size)

                setattr(data, attr, val)

            elif f.kind == UvmFieldKind.ENUM:
                size = f.size
                if size is None or size <= 0:
                    raise ValueError(f"Invalid size for field '{f.name}': {size}")

                seg = bits[offset:offset + size]
                offset += size

                # Convert MSB-first segment to integer
                val = 0
                for b in seg:
                    val = (val << 1) | (1 if b else 0)

                # Interpret signed if requested (two's complement)
                if f.is_signed and size > 0:
                    sign_bit = 1 << (size - 1)
                    if val & sign_bit:
                        val -= (1 << size)

                # Convert to enum type if available
                if f.enum_type is not None:
                    try:
                        val = f.enum_type(val)
                    except ValueError:
                        # Value not in enum, keep as int
                        pass

                setattr(data, attr, val)

            elif f.kind == UvmFieldKind.OBJ:
                # Read 4-bit header
                header_bits = bits[offset:offset + 4]
                offset += 4
                header_val = 0
                for b in header_bits:
                    header_val = (header_val << 1) | (1 if b else 0)

                if header_val == 0:
                    # null object
                    setattr(data, attr, None)
                else:
                    # non-null object: recursively unpack
                    if f.obj_type is None:
                        raise ValueError(f"Object field '{f.name}' has no obj_type defined")
                    if f.obj_type.data_t is None:
                        raise ValueError(f"Object field '{f.name}' obj_type has no data_t defined")
                    child_data = f.obj_type.data_t()
                    offset = f.obj_type._unpack_bits(bits, offset, child_data)
                    setattr(data, attr, child_data)

            elif f.kind == UvmFieldKind.QUEUE:
                # Unpack queue: 32-bit size header, then elements
                size = f.size
                
                # Unpack queue length (32-bit)
                len_bits = bits[offset:offset + 32]
                offset += 32
                queue_len = 0
                for b in len_bits:
                    queue_len = (queue_len << 1) | (1 if b else 0)
                
                # If element size is unknown and queue has elements, we need to infer it
                if (f.size_unknown or size is None or size <= 0) and queue_len > 0:
                    # Calculate total bits remaining for all fields after this one
                    remaining_fields_bits = 0
                    found_current = False
                    for remaining_f in self.fields:
                        if found_current:
                            if remaining_f.kind == UvmFieldKind.INT or remaining_f.kind == UvmFieldKind.ENUM:
                                if remaining_f.size and remaining_f.size > 0:
                                    remaining_fields_bits += remaining_f.size
                            elif remaining_f.kind == UvmFieldKind.OBJ:
                                remaining_fields_bits += 4  # header
                                if remaining_f.obj_type:
                                    remaining_fields_bits += remaining_f.obj_type._total_pack_bits()
                            elif remaining_f.kind == UvmFieldKind.QUEUE:
                                remaining_fields_bits += 32  # size header, elements unknown
                        if remaining_f.name == f.name:
                            found_current = True
                    
                    # Calculate element size from available bits
                    bits_available = len(bits) - offset - remaining_fields_bits
                    if bits_available > 0 and queue_len > 0:
                        size = bits_available // queue_len
                        # Update the field's size now that we know it
                        f.size = size
                        f.size_unknown = False
                    else:
                        raise ValueError(f"Cannot determine element size for queue field '{f.name}': queue_len={queue_len}, bits_available={bits_available}")
                
                if size is None or size <= 0:
                    if queue_len == 0:
                        # Empty queue is OK
                        setattr(data, attr, [])
                        continue
                    else:
                        raise ValueError(f"Invalid element size for queue field '{f.name}': {size}")
                
                # Unpack each element
                queue = []
                for _ in range(queue_len):
                    elem_bits = bits[offset:offset + size]
                    offset += size
                    
                    elem_val = 0
                    for b in elem_bits:
                        elem_val = (elem_val << 1) | (1 if b else 0)
                    
                    # Interpret signed if requested (two's complement)
                    if f.is_signed and size > 0:
                        sign_bit = 1 << (size - 1)
                        if elem_val & sign_bit:
                            elem_val -= (1 << size)
                    
                    queue.append(elem_val)
                
                setattr(data, attr, queue)

            else:
                raise NotImplementedError(f"Unsupported field kind for unpacking: {f.kind}")

        return offset

    def unpack_ints(self, intstream: List[int]) -> object:
        """
        Unpacks a list of 32-bit ints (as produced by pack_ints) into a new data_t instance.
        Mirrors UVM uvm_object::unpack_ints + uvm_packer.put_ints with big_endian=1:
        - Each 32-bit word is bit-reversed before appending to the bitstream.
        - Uses the exact field sizes in order to slice values MSB-first.
        - For OBJ fields, reads 4-bit header (0=null, else non-null) then recursively unpacks.
        - Signed fields are interpreted in two's complement.
        Returns:
            data_t instance populated with unpacked field values.
        """
        if self.data_t is None:
            raise ValueError("data_t is not defined for this UvmObjectType (%s)" % self.type_name)
        if not isinstance(intstream, list):
            raise TypeError("intstream must be a List[int]")

        # Reconstruct m_bits by reversing each 32-bit word (undo big_endian get_ints)
        bits: List[int] = []
        for v in intstream:
            if not isinstance(v, int):
                raise TypeError(f"intstream contains non-int element: {type(v)!r}")
            # Reverse 32 bits of v
            word_bits = [0] * 32
            for j in range(32):
                bj = (v >> j) & 1
                word_bits[31 - j] = bj
            bits.extend(word_bits)

        # Create target data object
        data = self.data_t()

        # Unpack fields recursively
        self._unpack_bits(bits, 0, data)

        return data
