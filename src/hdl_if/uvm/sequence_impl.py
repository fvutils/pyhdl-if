import abc
import dataclasses as dc
from .sequence_proxy import uvm_sequence_proxy

@dc.dataclass
class uvm_sequence_impl(object):
    proxy : uvm_sequence_proxy = dc.field()

    @abc.abstractmethod
    async def body(self): ...