from __future__ import annotations
from hdl_if import api, imp
from typing import List, Tuple
from .uvm_object import UvmObject

@api
class UvmComponent(object):

    def __del__(self):
        print("__del__", flush=True)

    @imp
    def get_name(self) -> str: ...

    @imp
    def get_full_name(self) -> str: ...

    @imp
    def sprint(self) -> str: ...

    @imp
    def get_children(self) -> List[object]: ...

    @imp
    def get_config_object(self, name : str) -> Tuple[bool, UvmObject]: ...

