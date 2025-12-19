from __future__ import annotations
import dataclasses as dc
from ...decorators import api, exp, imp
from typing import ClassVar, List, Optional, cast
from .cmdline_processor import uvm_cmdline_processor
from .object import uvm_object
from .object_type import UvmObjectType, UvmFieldType, UvmFieldKind
from ..object import uvm_object as uvm_object_p

@api
class uvm_object_rgy(object):
    """Implements type introspection"""
    _inst : ClassVar[Optional[uvm_object_rgy]] = None

    def __init__(self):
        uvm_object_rgy._inst = self
        self._loaded_typenames = False
        self._typenames = []

    @staticmethod
    def inst() -> uvm_object_rgy:
        assert uvm_object_rgy._inst is not None
        return uvm_object_rgy._inst
    
    @property
    def typenames(self):
        if not self._loaded_typenames:
            typedump = self._get_type_dump()

#            print("typedump: %s" % typedump, flush=True)

            # Parse the factory configuration dump
            self._typenames = self._parse_typedump(typedump)
            self._loaded_typenames = True
        return self._typenames

    def _parse_typedump(self, typedump: str) -> List[str]:
        """
        Parse the factory configuration output to extract valid type names.
        
        Expected format:
        #### Factory Configuration (*)
        ...
        All types registered with the factory: XX total
          Type Name
          ---------
          type1
          type2
          ...
        (*) Types with no associated type name will be printed as <unknown>
        
        Filters:
        - Ignore types marked as <unknown>
        - Ignore types starting with pyhdl_
        """
        if not typedump:
            return []
        
        lines = typedump.split('\n')
        type_names = []
        
        # Find the "Type Name" section
        in_type_section = False
        found_header = False
        
        for line in lines:
            stripped = line.strip()
            
            # Look for "Type Name" header (case-insensitive, allow leading spaces)
            if stripped.lower().startswith("type name"):
                found_header = True
                continue

            # Look for the separator line (only dashes) after "Type Name"
            if found_header and stripped and all(c == '-' for c in stripped):
                in_type_section = True
                continue
            
            # If we're in the type section, process type names
            if in_type_section:
                # Stop if we hit the footer or empty section
                if stripped.startswith('(*)') or not stripped:
                    break
                
                # Filter out <unknown> types
                if '<unknown>' in stripped:
                    continue
                
                # Filter out types starting with pyhdl_
                if stripped.startswith('pyhdl_'):
                    continue
                
                # Add valid type name
                type_names.append(stripped)
        
        return type_names
    
    @exp
    def mk(self, obj : uvm_object) -> UvmObjectType:
#        print("--> mk %s" % obj.get_name())

        obj_t = UvmObjectType("Any")
        obj_s = obj.sprint()

        # Populate fields from the sprint output
        self.populate_fields(obj_t, obj_s)

#        print("<-- mk %s" % obj.get_name())
        return obj_t
    
    @imp
    def clp(self) -> uvm_cmdline_processor: ...

    def populate_fields(self, obj_t: UvmObjectType, layout: str, obj_type_cache: dict = None) -> None:
        """
        Parse the layout string (from obj.sprint()) and populate the fields list.
        Sets can_pack to False if any field has unknown size (for INT fields).
        For OBJ fields, attempts to resolve the nested object type.
        
        Args:
            obj_t: The UvmObjectType to populate
            layout: Sprint output string to parse
            obj_type_cache: Optional dict mapping type names to UvmObjectType instances
        """
        if obj_type_cache is None:
            obj_type_cache = {}

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
                field_type = tokens[1]

                # Check if this is an object-type field
                # Object fields in UVM sprint output typically have type "object" or a custom class name
                # and size "-"
                if tokens[2] == "-":
                    # This could be an object field - check if we can resolve its type
                    # The field_type token contains the SV class name
                    sanitized_type = self._sanitize_field_name(field_type)
                    
                    # Try to find or create the object type
                    nested_obj_type = obj_type_cache.get(sanitized_type)
                    
                    if nested_obj_type is not None:
                        # We have type info for this object field
                        field = UvmFieldType(
                            name=field_name,
                            kind=UvmFieldKind.OBJ,
                            size=-1,  # Objects don't have a fixed size in the same sense
                            is_signed=False,
                            obj_type=nested_obj_type
                        )
                        obj_t.fields.append(field)
                        obj_t.field_m[field.name] = field
                    else:
                        # Unknown object type - disable packing
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
                obj_t.field_m[field.name] = field
                
            count += 1

        # After collecting fields, synthesize a Python dataclass that mirrors them
        if obj_t.fields and obj_t.data_t is None:
            obj_t.data_t = self._make_data_dataclass(obj_t)
        
        if obj_t.data_t is None:
            fields_spec = ()
            # Provide a fallback typename when no type name was discovered
            obj_t.data_t = dc.make_dataclass(obj_t.type_name or "UvmObjectData", fields_spec)

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
        For ENUM fields, includes enum_type_name in metadata.
        """
        fields_spec = []
        for f in obj_t.fields:
            if f.kind == UvmFieldKind.INT:
                ftype = int
                default = 0
            elif f.kind == UvmFieldKind.STR:
                ftype = str
                default = ""
            elif f.kind == UvmFieldKind.ENUM:
                # Use the enum type if available, otherwise int
                ftype = f.enum_type if f.enum_type is not None else int
                default = 0
            elif f.kind == UvmFieldKind.OBJ:
                ftype = (f.obj_type.data_t if (f.obj_type and f.obj_type.data_t is not None) else object)
                default = None
            elif f.kind == UvmFieldKind.QUEUE:
                ftype = list
                default = dc.field(default_factory=list)
            else:
                ftype = object
                default = None

            fname = self._sanitize_field_name(f.name)
            ex_idx = -1
            for i,field in enumerate(fields_spec):
                if fname == field[0]:
                    ex_idx = i
                    break

            # Build metadata
            metadata = {"size": f.size, "signed": f.is_signed}
            if f.kind == UvmFieldKind.ENUM and f.enum_type_name:
                metadata["enum_type_name"] = f.enum_type_name

            if ex_idx == -1:
                # For QUEUE fields, default is already a dc.field with default_factory
                if f.kind == UvmFieldKind.QUEUE:
                    fields_spec.append((fname, ftype, default))
                else:
                    fields_spec.append((fname, ftype, dc.field(default=default, metadata=metadata)))
            else:
                if f.kind == UvmFieldKind.QUEUE:
                    fields_spec[ex_idx] = (fname, ftype, default)
                else:
                    fields_spec[ex_idx] = (fname, ftype, dc.field(default=default, metadata=metadata))

        typename = obj_t.type_name or "UvmObjectData"
        try:
            ret = dc.make_dataclass(typename, fields_spec)
        except Exception as e:
            print("Fields: %s" % str(fields_spec))
            raise e

        return ret

    @imp
    def _get_type_dump(self) -> str: ...

    @imp
    def create_by_name(self, name : str) -> uvm_object_p: ...


# Backward-compatible alias
UvmObjectRgy = uvm_object_rgy
