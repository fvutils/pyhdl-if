#****************************************************************************
#* types.py
#*
#* Copyright 2026 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may
#* not use this file except in compliance with the License.
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software
#* distributed under the License is distributed on an "AS IS" BASIS,
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#* See the License for the specific language governing permissions and
#* limitations under the License.
#*
#****************************************************************************
"""Type annotations for records and interfaces shared with SystemVerilog.

Python's ``int`` has no width, so a record field that must match a sized
SystemVerilog field is annotated with one of the sized aliases here
(``u8``, ``i32``, ...) or with :func:`uint`/:func:`sint` for other widths.
To a type checker each is plain ``int``.

:data:`Ref` marks a parameter or return value that passes a record by
reference instead of by copy.
"""
import dataclasses as dc
from typing import Annotated, TypeVar

__all__ = [
    "IntT", "RefMarker", "Ref",
    "u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64",
    "uint", "sint",
]


@dc.dataclass(frozen=True)
class IntT(object):
    """Width and signedness of an integer, carried in an ``Annotated`` hint.

    Args:
        width: Width in bits.
        signed: Whether the value is two's-complement signed.
    """
    width: int
    signed: bool


@dc.dataclass(frozen=True)
class RefMarker(object):
    """Marks an ``Annotated`` hint as by-reference. Use :data:`Ref` instead."""
    pass


_T = TypeVar("_T")

#: ``Ref[pkt]`` passes a ``pkt`` record by reference: the callee works on the
#: caller's object instead of a copy. A plain ``pkt`` hint passes a copy. To a
#: type checker, ``Ref[pkt]`` is ``pkt``.
Ref = Annotated[_T, RefMarker()]


def uint(width: int):
    """Return the hint for an unsigned integer of ``width`` bits."""
    return Annotated[int, IntT(width, False)]


def sint(width: int):
    """Return the hint for a signed integer of ``width`` bits."""
    return Annotated[int, IntT(width, True)]


u8 = uint(8)
u16 = uint(16)
u32 = uint(32)
u64 = uint(64)
i8 = sint(8)
i16 = sint(16)
i32 = sint(32)
i64 = sint(64)
