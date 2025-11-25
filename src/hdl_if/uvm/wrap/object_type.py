from __future__ import annotations
import dataclasses as dc
from typing import Dict, List, Optional, Type
from enum import Enum

class UvmFieldKind(Enum):
    INT = "int"
    STR = "str"
    OBJ = "obj"

@dc.dataclass
class UvmFieldType(object):
    name: str
    kind: UvmFieldKind = UvmFieldKind.INT
    size: int = -1
    is_signed: bool = False
    obj_type: Optional['uvm_object_type'] = None

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
        Computes the total number of bits required to pack all INT fields.
        Raises if any INT field has unknown/invalid size.
        """
        total = 0
        for f in self.fields:
            if f.kind != UvmFieldKind.INT:
                raise NotImplementedError("Only INT fields are supported by pack_ints/unpack_ints")
            if f.size is None or f.size <= 0:
                raise ValueError(f"Invalid size for field '{f.name}': {f.size}")
            total += f.size
        return total

    def pack_ints(self, data_obj: object) -> List[int]:
        """
        Packs INT fields from the provided data object into a list of 32-bit ints.
        Semantics mirror UVM uvm_object::pack_ints + uvm_packer.get_ints with big_endian=1:
        - Fields are appended MSB-first into a bitstream.
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
        for f in self.fields:
            if f.kind != UvmFieldKind.INT:
                raise NotImplementedError(f"Unsupported field kind for packing: {f.kind}")
            size = f.size
            if size is None or size <= 0:
                raise ValueError(f"Invalid size for field '{f.name}': {size}")

            attr = self._sanitize_field_name(f.name)
            if not hasattr(data_obj, attr):
                raise AttributeError(f"Data object missing attribute for field '{f.name}' (attr='{attr}')")

            v = getattr(data_obj, attr)
            if not isinstance(v, int):
                raise TypeError(f"Field '{f.name}' value must be int, got {type(v)!r}")

            # Mask to width (two's complement for negative values handled by masking)
            mask = (1 << size) - 1 if size < 1024*1024 else (1 << size) - 1  # Python int is unbounded; keep simple
            v_masked = v & mask

            # Append bits MSB -> LSB
            for i in range(size - 1, -1, -1):
                bits.append((v_masked >> i) & 1)

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

    def unpack_ints(self, intstream: List[int]) -> object:
        """
        Unpacks a list of 32-bit ints (as produced by pack_ints) into a new data_t instance.
        Mirrors UVM uvm_object::unpack_ints + uvm_packer.put_ints with big_endian=1:
        - Each 32-bit word is bit-reversed before appending to the bitstream.
        - Uses the exact field sizes in order to slice values MSB-first.
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

        total = self._total_pack_bits()
        if len(bits) < total:
            raise ValueError(f"Insufficient bits in intstream: have {len(bits)}, need {total}")

        # Create target data object
        data = self.data_t()

        # Slice and assign per field
        offset = 0
        for f in self.fields:
            if f.kind != UvmFieldKind.INT:
                raise NotImplementedError(f"Unsupported field kind for unpacking: {f.kind}")
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

            attr = self._sanitize_field_name(f.name)
            setattr(data, attr, val)

        return data
