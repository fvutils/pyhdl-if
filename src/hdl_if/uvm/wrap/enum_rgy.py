from __future__ import annotations
from ...decorators import api, exp, imp
from typing import ClassVar, Dict, List, Optional, Type
from enum import IntEnum

@api
class uvm_enum_rgy(object):
    """Registry for enum types registered from SystemVerilog"""
    _inst : ClassVar[Optional[uvm_enum_rgy]] = None
    
    def __init__(self):
        uvm_enum_rgy._inst = self
        self._enum_types_cache : Dict[str, Type[IntEnum]] = {}
    
    @staticmethod
    def inst() -> uvm_enum_rgy:
        if uvm_enum_rgy._inst is None:
            uvm_enum_rgy._inst = uvm_enum_rgy()
        return uvm_enum_rgy._inst
    
    @exp
    def get_enum_type(self, type_name: str) -> Optional[Type[IntEnum]]:
        """
        Get the Python IntEnum type for a registered enum.
        
        Args:
            type_name: The name of the enum type (as registered in SystemVerilog)
            
        Returns:
            A Python IntEnum class with the enum's members, or None if not found
        """
        if type_name in self._enum_types_cache:
            return self._enum_types_cache[type_name]
        
        names = self._get_enum_names(type_name)
        values = self._get_enum_values(type_name)
        
        if not names or not values:
            return None
        
        if len(names) != len(values):
            raise ValueError(f"Enum {type_name}: names and values length mismatch")
        
        # Create a Python IntEnum from the names and values
        enum_dict = {name: value for name, value in zip(names, values)}
        enum_type = IntEnum(type_name, enum_dict)
        
        # Cache it
        self._enum_types_cache[type_name] = enum_type
        
        return enum_type
    
    @exp
    def get_enum_types(self) -> List[str]:
        """
        Get a list of all registered enum type names.
        
        Returns:
            List of enum type names
        """
        return self._get_enum_types()
    
    @exp
    def has_enum_type(self, type_name: str) -> bool:
        """
        Check if an enum type is registered.
        
        Args:
            type_name: The name of the enum type
            
        Returns:
            True if the enum type is registered, False otherwise
        """
        return type_name in self.get_enum_types()
    
    @imp
    def _get_enum_names(self, type_name: str) -> List[str]:
        """Get enumerator names from SystemVerilog"""
        ...
    
    @imp
    def _get_enum_values(self, type_name: str) -> List[int]:
        """Get enumerator values from SystemVerilog"""
        ...
    
    @imp
    def _get_enum_types(self) -> List[str]:
        """Get all registered enum type names from SystemVerilog"""
        ...


# Backward-compatible alias
UvmEnumRgy = uvm_enum_rgy
