
from ..decorators import api, imp

@api
class ObjectTypeIF(object):

    @imp
    def get_name(self) -> str:
        pass

#    @imp
#    def get_fields(self)

