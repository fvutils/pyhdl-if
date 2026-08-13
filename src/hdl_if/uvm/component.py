"""Python view of a SystemVerilog ``uvm_component``."""

import abc
from typing import Protocol
from .object import uvm_object

class uvm_component(uvm_object):
    """The interface a SystemVerilog ``uvm_component`` presents to Python.

    Extends :class:`~hdl_if.uvm.uvm_object` with the component-specific
    surface: the phase callbacks and factory access. Like ``uvm_object``, this
    describes a wrapper around a SystemVerilog object rather than something
    constructed in Python.

    To *implement* a component in Python, subclass
    :class:`~hdl_if.uvm.uvm_component_impl` instead.
    """

    @abc.abstractmethod
    def get_full_name(self) -> str:
        """Return the component's full hierarchical path."""

    @abc.abstractmethod
    def build_phase(self, phase : object):
        """Run the UVM build phase.

        Args:
            phase: The phase object.
        """

    @abc.abstractmethod
    def connect_phase(self, phase : object):
        """Run the UVM connect phase.

        Args:
            phase: The phase object.
        """

    @abc.abstractmethod
    async def run_phase(self, phase : object):
        """Run the UVM run phase.

        Args:
            phase: The phase object.
        """

    @abc.abstractmethod
    def create_object(self, requested_type_name : str, name : str = "") -> uvm_object:
        """Create an object through the UVM factory.

        Args:
            requested_type_name: The registered type name to create.
            name: Leaf name for the new object.

        Returns:
            The new object, subject to any factory overrides in effect.
        """

    @abc.abstractmethod
    def create_component(self, requested_type_name : str, name : str) -> uvm_object:
        """Create a component through the UVM factory, parented to this one.

        Args:
            requested_type_name: The registered type name to create.
            name: Leaf name for the new component.

        Returns:
            The new component, subject to any factory overrides in effect.
        """
