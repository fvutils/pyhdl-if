from __future__ import annotations

import weakref
from typing import Any


class TypeInfo:
    _info_m: "weakref.WeakKeyDictionary[type[Any], TypeInfo]" = weakref.WeakKeyDictionary()

    def __init__(self, T: type[Any]):
        self.T = T

    @classmethod
    def get(cls, T: type[Any]) -> "TypeInfo":
        ti = cls._info_m.get(T)
        if ti is None:
            ti = TypeInfo(T)
            cls._info_m[T] = ti
        return ti
