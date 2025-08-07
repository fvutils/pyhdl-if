from ..decorators import api, imp

@api
class ObjectIF(object):

    @imp
    def get_name(self) -> str:
        pass


