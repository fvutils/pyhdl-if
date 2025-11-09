import abc
from .component import uvm_component
from .object import uvm_object
from .sequence import uvm_sequence

class uvm_sequence_proxy(uvm_sequence):

    @abc.abstractmethod
    def get_userdata(self) -> uvm_object: ...

    @abc.abstractmethod
    def create_req(self) -> uvm_object: ...

    @abc.abstractmethod
    def create_rsp(self) -> uvm_object: ...

    @abc.abstractmethod
    async def start_item(self, item : uvm_object): ...

    @abc.abstractmethod
    async def finish_item(self, item : uvm_object): ...

    @property
    @abc.abstractmethod
    def m_sequencer(self) -> uvm_component: ...
