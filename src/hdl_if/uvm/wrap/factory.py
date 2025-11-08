from typing import Optional
from ...decorators import api, imp

from ..component import uvm_component
from ..object import uvm_object

@api
class UvmObjectWrapper(object):

    @imp
    def create_component(self, name : str) -> Optional[uvm_component]:
        ...

    @imp
    def create_object(self, name : str) -> Optional[uvm_object]:
        ...
    pass

@api
class UvmFactory(object):
    pass