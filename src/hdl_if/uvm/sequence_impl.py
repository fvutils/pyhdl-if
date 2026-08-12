"""Base class for UVM sequences implemented in Python."""

import abc
import dataclasses as dc
from .sequence_proxy import uvm_sequence_proxy

@dc.dataclass
class uvm_sequence_impl(object):
    """Base class for a UVM sequence whose body is written in Python.

    Subclass this and implement :meth:`body`. Name the subclass from
    SystemVerilog and ``pyhdl_uvm_sequence_proxy`` runs it when the sequence
    is started on a sequencer::

        # pyseq.py
        from hdl_if.uvm import uvm_sequence_impl

        class PyRandSeq(uvm_sequence_impl):
            async def body(self):
                for _ in range(8):
                    req = self.proxy.create_req()
                    req.randomize()
                    await self.proxy.start_item(req)
                    await self.proxy.finish_item(req)

    .. code-block:: systemverilog

       typedef pyhdl_uvm_sequence_proxy #(
         .REQ(seq_item), .PyClass("pyseq:PyRandSeq")) py_seq_t;

    Attributes:
        proxy: Handle to the SystemVerilog sequence proxy. Items are created
            and driven through it -- see
            :class:`~hdl_if.uvm.uvm_sequence_proxy`.
    """

    proxy : uvm_sequence_proxy = dc.field()

    @abc.abstractmethod
    async def body(self):
        """Generate the sequence's stimulus.

        Called when the sequence is started on a sequencer, and awaited to
        completion before the sequence finishes.
        """
