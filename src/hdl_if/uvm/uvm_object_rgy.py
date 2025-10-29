from __future__ import annotations
import dataclasses as dc
from hdl_if import api, exp, imp
from typing import ClassVar, Optional
from .uvm_object import UvmObject
from .uvm_object_type import UvmObjectType, UvmFieldType, UvmFieldKind

@api
class UvmObjectRgy(object):
    """Implements type introspection"""
    _inst : ClassVar[Optional[UvmObjectRgy]] = None

    def __init__(self):
        UvmObjectRgy._inst = self
        self._loaded_typenames = False
        self._typenames = []

    @staticmethod
    def inst() -> UvmObjectRgy:
        assert UvmObjectRgy._inst is not None
        return UvmObjectRgy._inst
    
    @property
    def typenames(self):
        if not self._loaded_typenames:
            typedump = self._get_type_dump()

            print("typedump: %s" % typedump, flush=True)

            self._loaded_typenames = True
        return self._typenames
    
    @exp
    def mk(self, obj : UvmObject) -> UvmObjectType:
        print("--> mk %s" % obj.get_name())
        obj_t = UvmObjectType()
        obj_s = obj.sprint()
        
        # Populate fields from the sprint output
        self.populate_fields(obj_t, obj_s)

        print("<-- mk %s" % obj.get_name())
        return obj_t

    def populate_fields(self, obj_t: UvmObjectType, layout: str) -> None:
        """
        Parse the layout string (from obj.sprint()) and populate the fields list.
        Sets can_pack to False if any field has unknown size.
        """
        if not layout:
            return
            
        lines = layout.split('\n')
        count = 0
        
        for line in lines:
            # Skip separator lines and empty lines
            if not line.strip() or line.strip().startswith('-'):
                continue
                
            # Split line into tokens, handling multiple spaces
            tokens = line.split()
            if not tokens:
                continue
                
            if count == 0:
                # Ignore header line (Name Type Size Value)
                pass
            elif len(tokens) >= 3:
                # First data line is the object/class line: [name, type, '-', ...]
                if obj_t.type_name is None and tokens[2] == "-":
                    # Capture the SV type name from the Type column
                    obj_t.type_name = self._sanitize_field_name(tokens[1])
                    count += 1
                    continue

                # Process field tokens: [field_name, type, size, ...]
                field_name = tokens[0]

                # Unknown/unsupported size on field line disables packing
                if tokens[2] == "-":
                    obj_t.can_pack = False
                    count += 1
                    continue

                try:
                    # Try to parse size as integer
                    size = int(tokens[2])
                except (ValueError, IndexError):
                    # If size is unknown or unparseable, mark can_pack as False
                    obj_t.can_pack = False
                    size = -1

                # Create field (currently assuming all fields are INT type like SystemVerilog)
                field = UvmFieldType(
                    name=field_name,
                    kind=UvmFieldKind.INT,
                    size=size,
                    is_signed=False  # Assuming unsigned for now
                )

                obj_t.fields.append(field)
                
            count += 1

        # After collecting fields, synthesize a Python dataclass that mirrors them
        if obj_t.fields and obj_t.data_t is None:
            obj_t.data_t = self._make_data_dataclass(obj_t)

    def _sanitize_field_name(self, name: str) -> str:
        # Ensure valid Python identifier
        s = ''.join((c if (c.isalnum() or c == '_') else '_') for c in name)
        if not s or s[0].isdigit():
            s = f"f_{s}"
        return s

    def _make_data_dataclass(self, obj_t: UvmObjectType):
        """
        Builds a Python dataclass type with one field per entry in obj_t.fields.
        Returns the created type.
        Each field includes metadata: {"size": f.size, "signed": f.is_signed}.
        """
        fields_spec = []
        for f in obj_t.fields:
            if f.kind == UvmFieldKind.INT:
                ftype = int
                default = 0
            elif f.kind == UvmFieldKind.STR:
                ftype = str
                default = ""
            elif f.kind == UvmFieldKind.OBJ:
                ftype = (f.obj_type.data_t if (f.obj_type and f.obj_type.data_t is not None) else object)
                default = None
            else:
                ftype = object
                default = None

            fname = self._sanitize_field_name(f.name)
            fields_spec.append((fname, ftype, dc.field(default=default, metadata={"size": f.size, "signed": f.is_signed})))

        typename = obj_t.type_name or "UvmObjectData"
        return dc.make_dataclass(typename, fields_spec)

    
    
    @imp
    def _get_type_dump(self) -> str: ...
