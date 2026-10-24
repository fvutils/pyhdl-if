"""The interchange types: what crosses between Python and SV.

gen-from-py generates the SV side of these. They are plain, sized and
flat; the pydantic model (ref_schema.py) stays on the Python side.
"""
import dataclasses as dc
import enum
from typing import Optional, Protocol

from hdl_if.rt import u8, u32


class Fate(enum.IntEnum):
    """Same values as pkt_fate_e in ipv4_pkt_pkg.sv."""
    FORWARD = 0
    BAD_HEADER = 1
    BAD_CHECKSUM = 2
    TTL = 3
    NO_ROUTE = 4


@dc.dataclass
class RefPkt:
    name: str = ""
    src: u32 = 0
    dst: u32 = 0
    ttl: u8 = 64
    protocol: u8 = 17
    dont_fragment: bool = False
    options: bytes = b""
    payload: bytes = b""
    ihl: u8 = 0                     # 0: from the options
    corrupt_checksum: bool = False
    expected: Fate = Fate.FORWARD


class RefSource(Protocol):
    """Implemented in Python; an SV sequence pulls packets from it."""

    def get_next(self) -> Optional[RefPkt]:
        """The next packet, or None at the end."""
        ...
