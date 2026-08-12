"""Handle onto the SystemVerilog side of a Python-implemented sequence."""

import abc
from .component import uvm_component
from .object import uvm_object
from .sequence import uvm_sequence

class uvm_sequence_proxy(uvm_sequence):
    """The SystemVerilog sequence proxy, as seen from Python.

    An instance is injected into :class:`~hdl_if.uvm.uvm_sequence_impl` as
    ``self.proxy``. It is how a Python sequence body creates items and runs
    the UVM item handshake -- the items themselves are SystemVerilog objects,
    so they are created on that side and returned as
    :class:`~hdl_if.uvm.uvm_object` wrappers.

    The usual shape is create, randomize, start, finish::

        req = self.proxy.create_req()
        req.randomize()
        await self.proxy.start_item(req)
        await self.proxy.finish_item(req)
    """

    @abc.abstractmethod
    def get_userdata(self) -> uvm_object:
        """Return the user data object attached to the sequence, if any."""

    @abc.abstractmethod
    def create_req(self) -> uvm_object:
        """Create a request item of the sequence's ``REQ`` type.

        Returns:
            The new item, with fields at their defaults.
        """

    @abc.abstractmethod
    def create_rsp(self) -> uvm_object:
        """Create a response item of the sequence's ``RSP`` type.

        Returns:
            The new item, with fields at their defaults.
        """

    @abc.abstractmethod
    async def start_item(self, item : uvm_object):
        """Begin the UVM handshake for an item.

        Blocks until the sequencer grants access to the driver. Randomize or
        assign the item's fields after this returns and before
        :meth:`finish_item`.

        Args:
            item: The item to send.
        """

    @abc.abstractmethod
    async def finish_item(self, item : uvm_object):
        """Complete the UVM handshake for an item.

        Blocks until the driver signals it is done with the item.

        Args:
            item: The item passed to the matching :meth:`start_item`.
        """

    @property
    @abc.abstractmethod
    def m_sequencer(self) -> uvm_component:
        """The sequencer this sequence is running on."""
