import ctypes
from ..decorators import api, imp, exp
from .uvm_factory import UvmFactory
from .uvm_component import UvmComponent

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
    def info(self, msg : str): ...

