from typing import List
from ..decorators import api, imp
from .field_if import FieldIF

@api
class ObjectTypeIF(object):

    @imp
    def get_name(self) -> str: pass

    @imp
    def get_fields(self) -> List[FieldIF]: pass
#    @imp
#    def get_fields(self)

