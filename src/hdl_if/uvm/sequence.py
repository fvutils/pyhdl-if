
import abc
from typing import Optional
from .object import uvm_object
from .sequencer import uvm_sequencer

class uvm_sequence(uvm_object):

    @abc.abstractmethod
    async def start(self, 
                    seqr : Optional[uvm_sequencer]=None): ...
