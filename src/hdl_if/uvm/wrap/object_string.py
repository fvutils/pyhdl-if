
import ctypes
from typing import Optional
from ...decorators import api, imp, exp
from .object import uvm_object

@api
class uvm_object_string(uvm_object):
    """
    UVM object string wrapper for storing a string value in a UVM object.
    
    Provides a Python interface to the SystemVerilog uvm_object_string class
    which wraps a simple string value in a uvm_object container.
    """

    def __init__(self):
        super().__init__()
        pass

    @imp
    def get_value(self) -> str:
        """
        Get the string value.
        
        Returns:
            The string value stored in this object
        """
        pass

    @imp
    def set_value(self, val: str) -> None:
        """
        Set the string value.
        
        Args:
            val: The string value to store
        """
        pass

    def __str__(self) -> str:
        """
        String representation of the uvm_object_string.
        
        Returns:
            The string value stored in this object
        """
        return self.get_value()

    def __repr__(self) -> str:
        """
        Detailed string representation of the uvm_object_string.
        
        Returns:
            A representation showing the type and value
        """
        return f"uvm_object_string('{self.get_value()}')"
