"""Python view of a SystemVerilog ``uvm_phase``."""

from .object import uvm_object

class uvm_phase(uvm_object):
    """The interface a SystemVerilog ``uvm_phase`` presents to Python.

    Passed to the phase methods of
    :class:`~hdl_if.uvm.uvm_component_impl`.
    """
    pass