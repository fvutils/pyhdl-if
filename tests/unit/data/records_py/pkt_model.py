"""Records and an interface declared in Python (the tutorial's 2b shape)."""
import dataclasses as dc
import enum
from typing import List, Protocol

from hdl_if.rt import u8, u16, u32


class Proto(enum.IntEnum):
    ICMP = 1
    TCP = 6
    UDP = 17


@dc.dataclass
class RefPkt:
    """A reference packet, built in Python and sent to SV."""
    src: u32 = 0
    dst: u32 = 0
    ttl: u8 = 64
    proto: Proto = Proto.UDP
    payload: bytes = b""
    opts: List[u16] = dc.field(default_factory=list)


class PktSink(Protocol):
    """Implemented in SV: drives packets into the DUT."""

    async def send(self, p: RefPkt) -> u32: ...

    def count(self) -> u32: ...
