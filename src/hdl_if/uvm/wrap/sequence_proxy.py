
import ctypes
from typing import Optional
from ..component import uvm_component as uvm_component_p
from ...decorators import api, imp, exp
from .object import uvm_object
from ..sequence_proxy import uvm_sequence_proxy
from ..sequence_impl import uvm_sequence_impl
from ..object import uvm_object as uvm_object_p

@api
class uvm_sequence_proxy(object):

    def __init__(self):
        self._impl : Optional[uvm_sequence_impl] = None

    @exp
    async def body(self):
        assert self._impl is not None
        await self._impl.body()

    @imp
    def get_userdata(self) -> uvm_object_p: ...

    @imp
    def create_req(self) -> uvm_object_p: ...

    @imp
    def create_rsp(self) -> uvm_object_p: ...

    @imp
    async def start_item(self, item : uvm_object_p): ...

    @imp
    async def finish_item(self, item : uvm_object_p): ...

    @imp
    def get_type_name(self) -> str:
        raise NotImplementedError()

    @imp
    def create(self) -> Optional[uvm_object_p]:
        if self._impl is not None:
            return self._impl.create()
        return None

    @imp
    def clone(self) -> Optional[uvm_object_p]:
        if self._impl is not None:
            return self._impl.clone()
        return None

    @imp
    def print(self) -> None:
        if self._impl is not None:
            return self._impl.print()
        return None

    @imp
    def convert2string(self) -> str:
        assert self._impl is not None
        return self._impl.convert2string()

    @imp
    def record(self):
        if self._impl is not None:
            return self._impl.record()
        return None

    @imp
    def copy(self, rhs : uvm_object_p) -> None:
        assert self._impl is not None
        return self._impl.copy(rhs)

    @property
    def m_sequencer(self) -> uvm_component_p: 
        return self._get_sequencer()

    @imp
    def _get_sequencer(self) -> uvm_component_p:
        raise NotImplementedError()

