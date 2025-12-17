
import ctypes
from typing import Optional
from ...decorators import api, imp, exp
from .object import uvm_object

@api
class uvm_object_list(uvm_object):
    """
    UVM object list wrapper for storing collections of UVM objects.
    
    Provides a Python interface to the SystemVerilog uvm_object_list class
    which uses a dynamic array ($) to store uvm_object instances.
    """

    def __init__(self):
        super().__init__()
        pass

    @imp
    def at(self, index: ctypes.c_int) -> ctypes.c_void_p:
        """
        Get the object at the specified index.
        
        Args:
            index: The index of the object to retrieve
            
        Returns:
            PyObject representing the UVM object at that index
        """
        pass

    @imp
    def push_back(self, obj: ctypes.c_void_p) -> None:
        """
        Add an object to the end of the list.
        
        Args:
            obj: PyObject representing the UVM object to add
        """
        pass
