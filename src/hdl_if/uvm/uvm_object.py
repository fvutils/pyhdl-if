
import ctypes
from ..decorators import api, imp, exp

@api
class UvmObject(object):

#    @imp
#    def randomize(self) -> bool: ...

    @imp
    def get_name(self) -> str: ...

