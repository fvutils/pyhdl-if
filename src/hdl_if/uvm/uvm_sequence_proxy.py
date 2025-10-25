
import ctypes
from ..decorators import api, imp, exp
from .uvm_object import UvmObject

@api
class UvmSequenceProxy(object):

    @exp
    async def body(self): ...

    @imp
    def get_userdata(self) -> UvmObject: ...

    @imp
    def create_req(self) -> UvmObject: ...

    @imp
    def create_rsp(self) -> UvmObject: ...

    @imp
    async def start_item(self, item : object): ...

    @imp
    async def finish_item(self, item : object): ...




