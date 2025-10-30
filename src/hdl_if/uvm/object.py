
import abc
from typing import Protocol

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


