from __future__ import annotations
from hdl_if import api, imp
from typing import List
from .uvm_object import UvmObject

@api
class UvmComponent(object):

    @imp
    def get_name(self) -> str: ...

    @imp
    def get_full_name(self) -> str: ...

    @imp
    def get_children(self) -> List['UvmComponent']: ...

