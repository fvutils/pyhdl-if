"""Python view of the UVM factory."""

import abc
from typing import Optional, Protocol
from .component import uvm_component
from .object import uvm_object

class uvm_object_wrapper(Protocol):
    """A factory registration for one registered type.

    Obtained from :meth:`uvm_factory.find_wrapper_by_name`. Creating through
    the wrapper honors any factory overrides in effect.
    """

    @abc.abstractmethod
    def create_component(self,
                         name : str,
                         parent : Optional[uvm_component]) -> Optional[uvm_component]:
        """Create a component of the wrapped type.

        Args:
            name: Leaf name for the new component.
            parent: The parent component, or None for a root.

        Returns:
            The new component, or None if the type is not a component.
        """

    @abc.abstractmethod
    def create_object(self, name : str) -> Optional[uvm_object]:
        """Create an object of the wrapped type.

        Args:
            name: Leaf name for the new object.

        Returns:
            The new object, or None if the type is not an object.
        """

class uvm_factory(Protocol):
    """The interface the UVM factory presents to Python."""

    @abc.abstractmethod
    def find_wrapper_by_name(self, name : str) -> Optional[uvm_object_wrapper]:
        """Look up a registered type by name.

        Args:
            name: The registered type name.

        Returns:
            The type's wrapper, or None if no such type is registered.
        """
