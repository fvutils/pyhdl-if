
from __future__ import annotations
import abc
from hdl_if import api, imp
from typing import List, TYPE_CHECKING
from .object import uvm_object
from ..reg import uvm_reg as uvm_reg_p
from ..reg_block import uvm_reg_block as uvm_reg_block_p

if TYPE_CHECKING:
    from .reg import uvm_reg

@api
class uvm_reg_block(uvm_object):

    def __init__(self):
        self._reg_m = None

    @imp
    def get_parent(self) -> uvm_reg_block_p:
        raise NotImplementedError()

    @imp
    def get_root_blocks(self) -> List[uvm_reg_block_p]:
        raise NotImplementedError()

    @imp
    def get_registers(self) -> List[uvm_reg_p]:
        raise NotImplementedError()
    
    def __getattr__(self, name):
        if self._reg_m is None:
            regs = self.get_registers()
            self._reg_m = {}
            for r in regs:
                self._reg_m[r.get_name()] = r
        if name in self._reg_m.keys():
            return self._reg_m[name]
        else:
            raise AttributeError("No register %s in block %s" % (
                name, self.get_name()))
