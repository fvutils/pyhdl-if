import ctypes
from ..decorators import api, imp
from .object_if import ObjectIF

@api
class ComponentIF(object):

    @imp
    def get_name(self) -> str:
        pass

    @imp
    def get_full_name(self) -> str:
        pass

    @imp
    def create_object_by_name(self, typename : str, name : str="") -> 'ObjectIF':
        pass

    pass