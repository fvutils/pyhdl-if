from __future__ import annotations
import ctypes as ct
from hdl_if import api, imp
from typing import List, TYPE_CHECKING, Tuple
from .object import uvm_object

if TYPE_CHECKING:
    from .reg import uvm_reg

@api
class uvm_reg_field(uvm_object):

    @imp
    def set(self, value : ct.c_uint64):
        ...

    @imp
    def get(self) -> ct.c_uint64:
        ...
    
    @imp
    async def write(self, value : ct.c_uint64) -> bool:
        ...

    @imp
    async def read(self) -> Tuple[bool,ct.c_uint64]:
        ...

