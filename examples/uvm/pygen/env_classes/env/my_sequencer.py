from __future__ import annotations
import dataclasses as dc
import typing
from hdl_if.uvm import uvm_component

@dc.dataclass(kw_only=True)
class my_sequencer(uvm_component):
    pass
