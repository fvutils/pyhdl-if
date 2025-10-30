import ctypes
from typing import List, cast
from ...decorators import api, imp, exp

@api
class UvmCmdlineProcessor(object):

    def plusargs(self) -> List[str]:
        return cast(List[str], self._get_plusargs())
        pass

    @imp
    def _get_plusargs(self) -> object: ...

    pass