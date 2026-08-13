"""Base class for UVM components implemented in Python."""

import dataclasses as dc

from .component_proxy import uvm_component_proxy
from .phase import uvm_phase

@dc.dataclass
class uvm_component_impl(object):
    """Base class for a UVM component whose behavior lives in Python.

    Subclass this and override the phase methods you need. Name the subclass
    from SystemVerilog and ``pyhdl_uvm_component_proxy`` will import it,
    construct it, and call through on each phase::

        # pycomp.py
        from hdl_if.uvm import uvm_component_impl

        class PyComp(uvm_component_impl):
            def build_phase(self, phase):
                print("build")

            async def run_phase(self, phase):
                await self.something()

    .. code-block:: systemverilog

       m_pycomp = pyhdl_uvm_component_proxy::type_id::create("m_pycomp", this);
       m_pycomp.pyclass = "pycomp::PyComp";

    The default implementations do nothing, so overriding only the phases you
    care about is fine.

    Attributes:
        proxy: Handle to the SystemVerilog proxy that constructed this
            object. Use it to reach the component's UVM identity and the
            factory.
    """

    proxy : uvm_component_proxy = dc.field()

    def build_phase(self, phase : uvm_phase):
        """Handle the UVM build phase. Override as needed.

        Args:
            phase: The phase object.
        """

    def connect_phase(self, phase : uvm_phase):
        """Handle the UVM connect phase. Override as needed.

        Args:
            phase: The phase object.
        """

    async def run_phase(self, phase : uvm_phase):
        """Handle the UVM run phase. Override as needed.

        This is a coroutine, so it may await simulation time. The phase is
        not complete until it returns.

        Args:
            phase: The phase object.
        """
