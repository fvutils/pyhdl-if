
from ..decorators import api, imp

@api
class FieldIF(object):

    @imp
    def get_name(self) -> str: pass

