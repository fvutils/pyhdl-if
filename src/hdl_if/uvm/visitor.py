"""Visitor over a UVM object hierarchy."""

from __future__ import annotations
from typing import cast, TYPE_CHECKING

if TYPE_CHECKING:
    from .component import uvm_component
    from .object import uvm_object

class uvm_visitor(object):
    """Visitor over a UVM object hierarchy.

    Subclass and override the ``visit_*`` methods you care about, then pass an
    instance to :meth:`uvm_object.accept
    <hdl_if.uvm.uvm_object.accept>`. Components dispatch to
    :meth:`visit_component`, which falls through to :meth:`visit_object` by
    default so a subclass handling only objects still sees them.
    """

    def visit_component(self, obj : uvm_component) -> None:
        """Visit a component.

        Args:
            obj: The component being visited.
        """
        self.visit_object(obj)

    def visit_object(self, obj : uvm_object) -> None:
        """Visit an object.

        Args:
            obj: The object being visited.
        """
        pass
