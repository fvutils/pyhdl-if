import ctypes
from typing import List, cast
from ...decorators import api, imp, exp
from .object import uvm_object

@api
class uvm_cmdline_processor(uvm_object):

    def __init__(self):
        super().__init__()

    def plusargs(self) -> List[str]:
        return cast(List[str], self.get_plusargs())

    @imp
    def get_plusargs(self) -> List[str]: ...
