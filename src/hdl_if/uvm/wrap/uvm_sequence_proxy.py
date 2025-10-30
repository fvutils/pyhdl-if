
import ctypes
from typing import Optional
from ...decorators import api, imp, exp
from .uvm_object import UvmObject
from ..sequence_proxy import uvm_sequence_proxy
from ..sequence_impl import uvm_sequence_impl
from ..object import uvm_object

@api
class UvmSequenceProxy(object):

    def __init__(self):
        self._impl : Optional[uvm_sequence_impl] = None

    @exp
    async def body(self):
        assert self._impl is not None
        await self._impl.body()

    @imp
    def get_userdata(self) -> uvm_object: ...

    @imp
    def create_req(self) -> uvm_object: ...

    @imp
    def create_rsp(self) -> uvm_object: ...

    @imp
    async def start_item(self, item : uvm_object): ...

    @imp
    async def finish_item(self, item : uvm_object): ...




