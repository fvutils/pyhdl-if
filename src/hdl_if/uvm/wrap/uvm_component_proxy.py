import ctypes
from typing import List, Optional, Tuple
from ...decorators import api, imp, exp
from .uvm_factory import UvmFactory
from .uvm_component import UvmComponent
from .uvm_object import UvmObject
from ..component import uvm_component
from ..component_impl import uvm_component_impl
from ..component_proxy import uvm_component_proxy

@api
class UvmComponentProxy(object):

    def __init__(self):
        self._impl : Optional[uvm_component_impl] = None
        self._child_m = None

    @exp
    def build_phase(self, phase : object):
        """
        """
        assert self._impl is not None
        self._impl.build_phase(phase)
        ...

    @exp
    def connect_phase(self, phase : object):
        assert self._impl is not None
        self._impl.connect_phase(phase)

    @exp
    async def run_phase(self, phase : object):
        """
        Implements the component run phase
        """
        assert self._impl is not None
        await self._impl.run_phase(phase)
        ...

    @imp
    def get_parent(self) -> object:
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

    @property
    def children(self) -> List[object]:
        return self.get_children()

    @imp
    def get_children(self) -> List[object]:
        """
        Returns the immediate child components of this component.

        Notes:

        - Order is implementation-defined.
        - Returned elements are component handles/proxies.
        """
        ...
    

    @imp
    def info(self, msg : str): ...

