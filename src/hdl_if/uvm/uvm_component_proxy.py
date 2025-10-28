import ctypes
from typing import Tuple
from ..decorators import api, imp, exp
from .uvm_factory import UvmFactory
from .uvm_component import UvmComponent
from .uvm_object import UvmObject

@api
class UvmComponentProxy(object):

    @exp
    def build_phase(self, phase : object):
        """
        """
        ...

    @exp
    def connect_phase(self, phase : object):
        ...

    @exp
    async def run_phase(self, phase : object):
        """
        Implements the component run phase
        """
        ...

    @imp
    def get_parent(self) -> UvmComponent:
        """
        Gets the parent UVM Component

        :returns: Parent UVM component
        """
        ...

    @imp
    def get_factory(self) -> UvmFactory: ...

    @imp
    def get_config_object(self, name : str) -> Tuple[bool, UvmObject]:
        """
        Gets an object from the config database

        :returns: Tuple of (Found,Obect). If not found, assume object is None
        """
        ...

    @imp
    def info(self, msg : str): ...

