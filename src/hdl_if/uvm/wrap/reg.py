from __future__ import annotations
import abc
import ctypes as ct
from hdl_if import api, imp, exp
from typing import List, Tuple
from .object import uvm_object
from ..object import uvm_object as uvm_object_p
from ..reg_field import uvm_reg_field as uvm_reg_field_p

@api
class uvm_reg(uvm_object):

    def __init__(self):
        self._field_m = None

    @imp
    def get_fields(self) -> List[uvm_reg_field_p]:
        raise NotImplementedError()

    @imp
    def set(self, value : ct.c_uint64):
        raise NotImplementedError()

    @imp
    def get(self) -> ct.c_uint64:
        raise NotImplementedError()
    
    @imp
    async def write(self, value : ct.c_uint64) -> bool:
        raise NotImplementedError()

    @imp
    async def read(self) -> Tuple[bool,ct.c_uint64]:
        raise NotImplementedError()

    def __getattr__(self, name):
        if self._field_m is None:
            self._field_m = {}
            fields = self.get_fields()
            for f in fields:
                self._field_m[f.get_name()] = f
        if name in self._field_m.keys():
            return self._field_m[name]
        else:
            raise AttributeError("No field %s in register %s" % (
                name, self.get_full_name()))

    @imp
    async def update() -> bool:
        ...
