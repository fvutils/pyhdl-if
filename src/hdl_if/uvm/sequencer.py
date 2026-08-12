"""Python view of a SystemVerilog ``uvm_sequencer``."""

import abc
from .object import uvm_object

class uvm_sequencer(uvm_object):
    """The interface a SystemVerilog ``uvm_sequencer`` presents to Python.

    Reached as :attr:`uvm_sequence_proxy.m_sequencer
    <hdl_if.uvm.uvm_sequence_proxy.m_sequencer>`. It carries the
    :class:`~hdl_if.uvm.uvm_object` surface; sequences are started on it
    from the SystemVerilog side.
    """
    pass
