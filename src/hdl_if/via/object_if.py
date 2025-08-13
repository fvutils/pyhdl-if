from ..decorators import api, imp
from .object_type_if import ObjectTypeIF

@api
class ObjectIF(object):

    def __del__(self):
        print("ObjectIF::__del__")

    @imp
    def get_name(self) -> str: pass

    @imp
    def get_object_type(self) -> ObjectTypeIF: pass


