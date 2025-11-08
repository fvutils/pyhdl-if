from __future__ import annotations
from ...decorators import api, imp
from ..object import uvm_object as uvm_object_p
from .object import uvm_object

@api
class uvm_phase(uvm_object):
    """Python proxy for UVM uvm_phase.

    Provides minimal methods commonly used from Python components.
    """

    @imp
    def get_name(self) -> str: ...

    @imp
    def raise_objection(self, obj: uvm_object_p, count: int = 1) -> None: ...

    @imp
    def drop_objection(self, obj: uvm_object_p, count: int = 1) -> None: ...
