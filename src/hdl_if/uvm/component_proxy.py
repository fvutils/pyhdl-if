"""Handle onto the SystemVerilog side of a Python-implemented component."""

import dataclasses as dc
from .component import uvm_component

class uvm_component_proxy(uvm_component):
    """The SystemVerilog component proxy, as seen from Python.

    An instance is injected into :class:`~hdl_if.uvm.uvm_component_impl` as
    ``self.proxy``. It carries the full
    :class:`~hdl_if.uvm.uvm_component` surface -- hierarchical name, phase
    callbacks, and factory access -- for the SystemVerilog component that
    constructed the Python implementation.
    """
    pass
