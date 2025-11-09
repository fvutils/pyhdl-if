from __future__ import annotations
import abc
from typing import List, Tuple
from .object import uvm_object
from .reg_field import uvm_reg_field

class uvm_reg(uvm_object):

    @abc.abstractmethod
    def get_fields(self) -> List[uvm_reg_field]:
        ...

    @abc.abstractmethod
    def set(self, value):
        ...

    @abc.abstractmethod
    def get(self) -> int:
        ...
    
    @abc.abstractmethod
    async def write(self, value) -> bool:
        ...

    @abc.abstractmethod
    async def read(self, value) -> Tuple[bool,int]:
        ...

    @abc.abstractmethod
    async def update() -> bool:
        ...

