import ctypes
from typing import List, Optional, Tuple
from ...decorators import api, imp, exp
from .component import uvm_component as uvm_component_w
from .object import uvm_object
from ..object import uvm_object as uvm_object_p
from ..component import uvm_component
from ..component_impl import uvm_component_impl
from ..component_proxy import uvm_component_proxy
from ..visitor import uvm_visitor

@api
class uvm_component_proxy(uvm_component_w):

    def __init__(self):
        super().__init__()
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



#    @imp
#    def get_factory(self) -> uvm_factory: ...

    @imp
    def get_config_object(self, name : str, clone : bool=False) -> Tuple[bool, uvm_object]:
        """
        Gets an object from the config database

        :returns: Tuple of (Found,Obect). If not found, assume object is None
        """
        ...

    @imp
    def reseed(self): ...

    @imp
    def set_name(self, name: str):
        if self._impl is not None:
            self._impl.set_name(name)

    @imp
    def get_inst_id(self) -> int :
        assert self._impl is not None
        return self._impl.get_inst_id()

    @imp
    def get_inst_count(self) -> int:
        assert self._impl is not None
        return self._impl.get_inst_count()

    # @property
    # def children(self) -> List[object]:
    #     return self.get_children()

    # @imp
    # def get_children(self) -> List[object]:
    #     """
    #     Returns the immediate child components of this component.

    #     Notes:

    #     - Order is implementation-defined.
    #     - Returned elements are component handles/proxies.
    #     """
    #     ...
    

    @imp
    def info(self, msg : str): ...

    @imp
    def get_type_name(self) -> str:
        if self._impl is not None:
            return self._impl.get_type_name()
        return None

    @imp
    def create(self) -> uvm_object_p:
        assert self._impl is not None
        return self._impl.create()

    @imp
    def clone(self) -> uvm_object_p:
        assert self._impl is not None
        return self._impl.clone()

    @imp
    def print(self):
        if self._impl is not None:
            return self._impl.print()
        return None

    @imp
    def convert2string(self) -> str:
        assert self._impl is not None
        return self._impl.convert2string()

    @imp
    def record(self) -> None:
        assert self._impl is not None
        self._impl.record()

    @imp
    def copy(self, rhs : uvm_object_p):
        if self._impl is not None:
            return self._impl.copy(rhs)
        return None

    @imp
    def create_object(self, requested_type_name : str, name : str = "") -> uvm_object: 
        ...

    @imp
    def create_component(self, requested_type_name : str, name : str) -> uvm_object: 
        ...

    def accept(self, v : uvm_visitor):
        pass
