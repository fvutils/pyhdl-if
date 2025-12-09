from __future__ import annotations
import dataclasses as dc
import typing
from hdl_if.uvm import uvm_object


@dc.dataclass(kw_only=True)
class seq_item_fields(object):
    ctrl_addr_page : int = dc.field(default=0)
    addr_page : int = dc.field(default=0)
    addr : int = dc.field(default=0)
    write : int = dc.field(default=0)
    data : int = dc.field(default=0)
    tid : int = dc.field(default=0)

@dc.dataclass
class seq_item(uvm_object, seq_item_fields):
    pass
