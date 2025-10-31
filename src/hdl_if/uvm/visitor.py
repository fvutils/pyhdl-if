from __future__ import annotations
from typing import cast, TYPE_CHECKING

if TYPE_CHECKING:
    from .component import uvm_component
    from .object import uvm_object

class uvm_visitor(object):

    def visit_component(self, obj : uvm_component) -> None:
        self.visit_object(obj)

    def visit_object(self, obj : uvm_object) -> None:
        pass
