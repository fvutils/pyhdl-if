import ctypes
from typing import List
from ...decorators import api, imp, exp

@api
class UvmFactory(object):

    @imp
    def typenames(self) -> List[str]: ...

    pass