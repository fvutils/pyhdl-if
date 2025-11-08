import abc
from typing import Optional, Protocol
from .component import uvm_component
from .object import uvm_object

class uvm_object_wrapper(Protocol):

    @abc.abstractmethod
    def create_component(self, 
                         name : str, 
                         parent : Optional[uvm_component]) -> Optional[uvm_component]: ...

    @abc.abstractmethod
    def create_object(self, name : str) -> Optional[uvm_object]: ...

class uvm_factory(Protocol):

    @abc.abstractmethod
    def find_wrapper_by_name(self, name : str) -> Optional[uvm_object_wrapper]: ...
    

