
from typing import cast
from uvm_component import UvmComponent
from .uvm_object import UvmObject

class Visitor(object):

    def visitComponet(self, obj : UvmComponent) -> None:
        self.visitObject(cast(UvmObject, obj))

    def visitObject(self, obj : UvmObject) -> None:
        pass
