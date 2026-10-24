import ctypes
import dataclasses as dc
import enum
from typing import List, Optional, Protocol

from hdl_if.rt import Ref, u8, i32, uint


class Color(enum.IntEnum):
    RED = 1
    BLUE = 300


class Sign(enum.IntEnum):
    NEG = -1
    POS = 1


class Wide(enum.IntEnum):
    __pyhdl_width__ = 4
    A = 0
    B = 9


@dc.dataclass
class Inner:
    a: u8 = 0
    c: Color = Color.RED


@dc.dataclass
class Outer:
    i: Inner = dc.field(default_factory=Inner)
    items: List[Inner] = dc.field(default_factory=list)
    nums: "list[int]" = dc.field(default_factory=list)
    data: bytes = b""
    w: uint(100) = 0
    o: Optional[Inner] = None
    ct: ctypes.c_uint16 = 0
    cb: ctypes.c_bool = False
    cf: ctypes.c_float = 0.0
    f: float = 0.0
    s: str = ""
    b: bool = False


@dc.dataclass
class Derived(Outer):
    extra: i32 = 0


class Cb(Protocol):
    def notify(self, v: i32) -> None: ...


class Svc(Protocol):
    def get(self, key: str) -> Optional[Outer]: ...

    async def put(self, p: Ref[Outer], cb: Cb) -> bool: ...

    def _private(self) -> None: ...


class SvcPlus(Svc, Protocol):
    def more(self) -> i32: ...


class NotExported(object):
    pass
