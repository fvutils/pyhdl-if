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
        pass

    @exp
    def connect_phase(self, phase : object):
        pass

    @exp
    async def run_phase(self, phase : object):
        pass

    @imp
    def get_parent(self) -> UvmComponent: ...

    @imp
    def get_factory(self) -> UvmFactory: ...

    @imp
    def get_config_object(self, name : str) -> Tuple[bool, UvmObject]: ...

    @imp
    def info(self, msg : str): ...

