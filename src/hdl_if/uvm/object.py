
import abc
from typing import Protocol
from .visitor import uvm_visitor

class uvm_object(Protocol):

    @abc.abstractmethod
    def get_name(self) -> str: ...

    @abc.abstractmethod
    def sprint(self) -> str: ...

    @abc.abstractmethod
    def pack(self) -> object: ...

    @abc.abstractmethod
    def unpack(self, val : object): ...

    @abc.abstractmethod
    def randomize(self): ...

    @abc.abstractmethod
    def accept(self, v : uvm_visitor): ...


