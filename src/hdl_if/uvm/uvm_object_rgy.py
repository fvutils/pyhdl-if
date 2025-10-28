from __future__ import annotations
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
                # Process field tokens: [field_name, type, size, ...]
                field_name = tokens[0]
                
                # Skip class lines (contain "-" for size)
                if tokens[2] == "-":
                    # Set can_pack to False when we encounter unknown sizes
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

    
    
    @imp
    def _get_type_dump(self) -> str: ...
