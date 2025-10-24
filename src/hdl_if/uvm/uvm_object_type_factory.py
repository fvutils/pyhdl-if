
from hdl_if import api, exp
from .uvm_object import UvmObject
from .uvm_object_type import UvmObjectType

@api
class UvmObjectTypeFactory(object):

    @exp
    def mk(self, obj) -> UvmObjectType:
        print("UvmObjectTypeFactory.mk()")
        pass

