"""Python view of a SystemVerilog ``uvm_sequence``."""

import abc
from typing import Optional
from .object import uvm_object
from .sequencer import uvm_sequencer

class uvm_sequence(uvm_object):
    """The interface a SystemVerilog ``uvm_sequence`` presents to Python.

    To *implement* a sequence in Python, subclass
    :class:`~hdl_if.uvm.uvm_sequence_impl` instead;
    :class:`~hdl_if.uvm.uvm_sequence_proxy` extends this with the item-creation
    and handshake methods a body actually uses.
    """

    @abc.abstractmethod
    async def start(self,
                    seqr : Optional[uvm_sequencer]=None):
        """Start the sequence on a sequencer.

        Args:
            seqr: The sequencer to run on. Defaults to the sequence's current
                sequencer.
        """
