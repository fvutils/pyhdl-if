
from __future__ import annotations
import abc
from typing import List, TYPE_CHECKING
from .object import uvm_object

if TYPE_CHECKING:
    from .reg import uvm_reg

class uvm_reg_block(uvm_object):


    @abc.abstractmethod
    def get_parent(self) -> uvm_reg_block: ...

    @abc.abstractmethod
    def get_root_blocks(self) -> List[uvm_reg_block]:
        ...

    @abc.abstractmethod
    def get_registers(self) -> List[uvm_reg]: 
        ...
