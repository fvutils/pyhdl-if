"""Python side of the UVM integration.

SystemVerilog proxy classes construct and drive Python implementations at
runtime. There are two halves to this API:

* The ``*_impl`` classes -- :class:`uvm_component_impl` and
  :class:`uvm_sequence_impl` -- are what you subclass. You name the subclass
  from SystemVerilog (via a ``pyclass`` field or ``PyClass`` parameter) and
  the proxy imports it, constructs it, and calls its phase or ``body``
  methods.
* The ``*_proxy`` classes are handles onto the SystemVerilog side, injected
  into your implementation as ``self.proxy``. You call through them to create
  and drive sequence items.

:class:`uvm_object` and :class:`uvm_component` wrap SystemVerilog objects
handed to Python -- sequence items, for example.

See :doc:`the UVM guide </uvm>` for worked examples.
"""

#from .uvm_cmdline_processor import UvmCmdlineProcessor
from .component import uvm_component
from .component_impl import uvm_component_impl
from .component_proxy import uvm_component_proxy
from .object import uvm_object
from .sequence_impl import uvm_sequence_impl
from .sequence_proxy import uvm_sequence_proxy

__all__ = [
    "uvm_component_impl",
    "uvm_sequence_impl",
    "uvm_component_proxy",
    "uvm_sequence_proxy",
    "uvm_object",
    "uvm_component",
]
