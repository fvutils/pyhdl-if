
import ctypes
from typing import Optional
from ...decorators import api, imp, exp
from .object import uvm_object

@api
class uvm_object_map(uvm_object):
    """
    UVM object map wrapper for storing key-value pairs of UVM objects.
    
    Provides a Python interface to the SystemVerilog uvm_object_map class
    which uses an associative array [string] to store uvm_object instances.
    """

    def __init__(self):
        super().__init__()
        pass

    @imp
    def has_key(self, key: str) -> bool:
        """
        Check if a key exists in the map.
        
        Args:
            key: The string key to check
            
        Returns:
            True if the key exists, False otherwise
        """
        pass

    @imp
    def get(self, key: str) -> ctypes.c_void_p:
        """
        Get the object associated with the specified key.
        
        Args:
            key: The string key to look up
            
        Returns:
            PyObject representing the UVM object for that key
        """
        pass

    @imp
    def insert(self, key: str, obj: ctypes.c_void_p) -> None:
        """
        Insert/update the object associated with the specified key.
        
        Args:
            key: The string key
            obj: PyObject representing the UVM object to store
        """
        pass
