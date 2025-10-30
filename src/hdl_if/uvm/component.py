import abc
from typing import Protocol
from .object import uvm_object

class uvm_component(uvm_object):

    @abc.abstractmethod
    def get_full_name(self) -> str: ...

    @abc.abstractmethod
    def build_phase(self, phase : object): ...

    @abc.abstractmethod
    def connect_phase(self, phase : object): ...

    @abc.abstractmethod
    async def run_phase(self, phase : object): ...
