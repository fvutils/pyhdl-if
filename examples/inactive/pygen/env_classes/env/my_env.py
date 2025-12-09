from __future__ import annotations
import dataclasses as dc
import typing
from hdl_if.uvm import uvm_component

if typing.TYPE_CHECKING:
    from .my_driver import my_driver
    from .my_sequencer import my_sequencer

@dc.dataclass(kw_only=True)
class my_env(uvm_component):
        m_drv : typing.Optional[my_driver] = dc.field(default=None)
        m_seqr : typing.Optional[my_sequencer] = dc.field(default=None)
