from __future__ import annotations

import functools
import inspect
import threading
from typing import Any, Dict, List, Tuple, get_type_hints

from .typeinfo import TypeInfo


class DeclRgy:
    _tls = threading.local()

    @classmethod
    def _decl_m(cls) -> Dict[type, List[Any]]:
        if not hasattr(cls._tls, "decl_m"):
            cls._tls.decl_m = {}
        return cls._tls.decl_m

    @classmethod
    def add_decl(cls, category: type, decl: Any) -> None:
        m = cls._decl_m()
        m.setdefault(category, []).append(decl)

    @classmethod
    def pop_decl(cls, category: type) -> List[Any]:
        m = cls._decl_m()
        return m.pop(category, [])


class MethodDecoratorBase:
    def __init__(self, args, kwargs):
        self._args = list(args) if args is not None else []
        self._kwargs = dict(kwargs) if kwargs is not None else {}

    def get_category(self):  # pragma: no cover
        raise NotImplementedError()

    def get_signature(self, func=None):
        if func is None:
            raise Exception("func must be provided")

        sig = inspect.signature(func)
        try:
            hints = get_type_hints(func, include_extras=True)
        except Exception:
            hints = getattr(func, "__annotations__", {}) or {}

        rtype = hints.get("return", None)

        params: List[Tuple[str, Any]] = []
        is_method = False
        for i, (name, _p) in enumerate(sig.parameters.items()):
            if i == 0 and name == "self":
                is_method = True
                continue
            params.append((name, hints.get(name, None)))

        return is_method, rtype, params

    def decorate(self, T):
        return T

    def register(self, T, Tp):
        DeclRgy.add_decl(self.get_category(), Tp)

    def __call__(self, T):
        Tp = self.decorate(T)
        if callable(Tp) and Tp is not T:
            Tp = functools.wraps(T)(Tp)
        self.register(T, Tp)
        return Tp


class ClsDecoratorBase:
    def __init__(self, args, kwargs):
        self._args = list(args) if args is not None else []
        self._kwargs = dict(kwargs) if kwargs is not None else {}
        self._typeinfo = None

    def get_typeinfo(self) -> TypeInfo:
        return self._typeinfo

    def get_type_category(self):
        return None

    def pre_decorate(self, T):
        pass

    def post_decorate(self, T, Tp):
        pass

    def pre_register(self):
        pass

    def __call__(self, T):
        self._typeinfo = TypeInfo.get(T)
        self.pre_decorate(T)
        self.post_decorate(T, T)
        self.pre_register()
        return T


__all__ = [
    "DeclRgy",
    "TypeInfo",
    "MethodDecoratorBase",
    "ClsDecoratorBase",
]
