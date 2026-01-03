#****************************************************************************
#* decorators.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
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
#* Created on:
#*     Author: 
#*
#****************************************************************************
from __future__ import annotations

import ctypes
import functools
import inspect
import sys
from typing import Any, Callable, TypeVar, overload, get_type_hints

# ParamSpec was added in Python 3.10
if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

from .impl.call.api_def import ApiDef
from .impl.call.api_def_rgy import ApiDefRgy
from .impl.call.ctor import Ctor
from .impl.call.imp_func_impl import ImpFuncImpl
from .impl.call.imp_task_impl import ImpTaskImpl
from .impl.call.method_def import MethodDef, MethodKind

P = ParamSpec("P")
R = TypeVar("R")
TClass = TypeVar("TClass", bound=type)


def _api_decorate(cls: TClass) -> TClass:
    ctor = Ctor.inst()
    rgy = ApiDefRgy.inst()

    init_params = []
    init_m = getattr(cls, "__init__")
    if hasattr(init_m, "__code__"):
        init_co = init_m.__code__
        type_hints = get_type_hints(init_m)
        for i in range(1, init_co.co_argcount):
            name = init_co.co_varnames[i]
            if name not in type_hints:
                raise Exception(f"parameter {name} is missing a type specification")
            init_params.append((name, type_hints[name]))

    fullname = cls.__module__ + "." + cls.__qualname__
    ad = ApiDef(fullname, init_params, ctor.getMethodDefs(), pycls=cls)
    rgy.addApiDef(ad)

    try:
        setattr(cls, "__pyhdl_api_def__", ad)
    except Exception:
        pass

    return cls


def _method_decorate(func: Callable[..., Any], kind: MethodKind) -> Callable[..., Any]:
    code = func.__code__
    hints = get_type_hints(func)

    rtype = hints.get("return", None)
    if rtype is type(None):
        rtype = None

    sig = inspect.signature(func)
    params = []
    defaults = []
    for i in range(1, code.co_argcount):
        pname = code.co_varnames[i]
        if pname not in hints:
            raise Exception(f"Method parameter {func.__name__}.{pname} is untyped")
        params.append((pname, hints[pname]))
        sig_param = sig.parameters.get(pname)
        if sig_param is not None and sig_param.default is not inspect.Parameter.empty:
            defaults.append(sig_param.default)
        else:
            defaults.append(inspect.Parameter.empty)

    if kind in (MethodKind.Imp, MethodKind.Exp):
        if inspect.iscoroutinefunction(func):
            kind = MethodKind.ImpTask if kind == MethodKind.Imp else MethodKind.ExpTask
        else:
            kind = MethodKind.ImpFunc if kind == MethodKind.Imp else MethodKind.ExpFunc

    md = MethodDef(kind, func, func.__name__, rtype, params, defaults)
    Ctor.inst().addMethodDef(md)

    if kind == MethodKind.ImpFunc:
        closure = ImpFuncImpl(md)

        @functools.wraps(func)
        def _wrap(self, *args, **kwargs):
            return closure(self, *args, **kwargs)

        setattr(_wrap, "__pyhdl_method_def__", md)
        return _wrap
    elif kind == MethodKind.ImpTask:
        closure = ImpTaskImpl(md)

        @functools.wraps(func)
        async def _wrap(self, *args, **kwargs):
            return await closure(self, *args, **kwargs)

        setattr(_wrap, "__pyhdl_method_def__", md)
        return _wrap
    else:
        try:
            setattr(func, "__pyhdl_method_def__", md)
        except Exception:
            pass
        return func


def _tlm_method_common(func: Callable[..., Any]):
    sig = inspect.signature(func)
    try:
        hints = get_type_hints(func)
    except Exception:
        hints = getattr(func, "__annotations__", {}) or {}

    rtype = hints.get("return", None)

    params = []
    is_method = False
    for i, (name, _p) in enumerate(sig.parameters.items()):
        if i == 0 and name == "self":
            is_method = True
            continue
        params.append((name, hints.get(name, None)))

    return is_method, rtype, params


def _tlm_if_decorate(cls: TClass) -> TClass:
    from hdl_if.impl.tlm.type_info_tlm_if import TypeInfoTlmIF
    from hdl_if.tlm.tlm_ifc_rgy import TlmIfcRgy
    from hdl_if.tlm.tlm_method import TlmMethod
    from hdl_if.impl.decl_rgy import DeclRgy
    from hdl_if.impl.typeinfo import TypeInfo

    info = TypeInfo.get(cls)
    tlm_if_ti = TypeInfoTlmIF.get(info)

    if_methods = DeclRgy.pop_decl(TlmMethod)
    tlm_if_ti._if_method_l.extend(if_methods)

    tlm_if_ti._base_init = cls.__init__
    TypeInfoTlmIF.addMethods(cls)

    TlmIfcRgy.inst().addTlmIf(tlm_if_ti)
    return cls


def _req_fifo_decorate(func: Callable[..., Any]) -> Callable[..., Any]:
    from hdl_if.tlm.tlm_method import TlmMethod, TlmMethodKind
    from hdl_if.impl.decl_rgy import DeclRgy

    _is_method, rtype, params = _tlm_method_common(func)

    if rtype is not None and rtype is not type(None):
        raise Exception("Request-FIFO method may not have a return type")
    if len(params) != 1:
        raise Exception(f"Request-FIFO method must have exactly one data parameter ({len(params)})")

    ptype = params[0][1]
    if not hasattr(ptype, "_fields_"):
        raise Exception(f"FIFO data-parameter type ({type(ptype)}) must derived from ctypes.Structure")

    proxy = TlmMethod(func.__name__, TlmMethodKind.Req, ptype, None)
    DeclRgy.add_decl(TlmMethod, proxy)

    @functools.wraps(func)
    async def closure(self, obj):
        model = self._model
        if func.__name__ not in model._if_m:
            raise Exception(f"Method {func.__name__} is unbound")
        ifc = model._if_m[func.__name__]
        await ifc.put(obj)

    return closure


def _rsp_fifo_decorate(func: Callable[..., Any]) -> Callable[..., Any]:
    from hdl_if.tlm.tlm_method import TlmMethod, TlmMethodKind
    from hdl_if.impl.decl_rgy import DeclRgy

    _is_method, rtype, params = _tlm_method_common(func)

    if rtype is None or rtype is type(None):
        raise Exception("Response FIFO must specify a return type")
    if len(params) != 0:
        raise Exception("Respoonse FIFO must not have parameters")
    if not hasattr(rtype, "_fields_"):
        raise Exception("FIFO response type must derive from ctypes.Structure")

    proxy = TlmMethod(func.__name__, TlmMethodKind.Rsp, None, rtype)
    DeclRgy.add_decl(TlmMethod, proxy)

    @functools.wraps(func)
    async def closure(self):
        model = self._model
        if func.__name__ not in model._if_m:
            raise Exception(f"Method {func.__name__} is unbound")
        ifc = model._if_m[func.__name__]
        ival = await ifc.get()
        sz = ctypes.sizeof(rtype)
        bval = bytearray(sz)
        for i in range(sz):
            bval[i] = (ival & 0xFF)
            ival >>= 8
        return rtype.from_buffer_copy(bval)

    return closure


def _reqrsp_fifo_decorate(func: Callable[..., Any]) -> Callable[..., Any]:
    from hdl_if.tlm.tlm_method import TlmMethod, TlmMethodKind
    from hdl_if.impl.decl_rgy import DeclRgy

    _is_method, rtype, params = _tlm_method_common(func)

    if rtype is None or rtype is type(None):
        raise Exception("ReqRsp-FIFO method must have a return type")
    if len(params) != 1:
        raise Exception(f"ReqRsp-FIFO method must have exactly one data parameter ({len(params)})")

    ptype = params[0][1]
    if not hasattr(ptype, "_fields_"):
        raise Exception(f"FIFO data-parameter type ({type(ptype)}) must derived from ctypes.Structure")
    if not hasattr(rtype, "_fields_"):
        raise Exception(f"FIFO data-parameter type ({type(rtype)}) must derived from ctypes.Structure")

    proxy = TlmMethod(func.__name__, TlmMethodKind.ReqRsp, ptype, rtype)
    DeclRgy.add_decl(TlmMethod, proxy)

    @functools.wraps(func)
    async def closure(self, obj):
        model = self._model
        if func.__name__ not in model._if_m:
            raise Exception(f"Method {func.__name__} is unbound")
        ifc = model._if_m[func.__name__]
        await ifc.put(obj)
        return await ifc.get()

    return closure


#********************************************************************
#* Decorators for API interfaces
#********************************************************************

@overload
def api(cls: TClass) -> TClass: ...

@overload
def api(*args: Any, **kwargs: Any) -> Callable[[TClass], TClass]: ...

def api(*args: Any, **kwargs: Any):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _api_decorate(args[0])

    def _decor(cls: TClass) -> TClass:
        return _api_decorate(cls)

    return _decor


@overload
def exp(func: Callable[P, R]) -> Callable[P, R]: ...

@overload
def exp(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

def exp(*args: Any, **kwargs: Any):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _method_decorate(args[0], MethodKind.Exp)

    def _decor(func: Callable[P, R]) -> Callable[P, R]:
        return _method_decorate(func, MethodKind.Exp)  # type: ignore

    return _decor


@overload
def imp(func: Callable[P, R]) -> Callable[P, R]: ...

@overload
def imp(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

def imp(*args: Any, **kwargs: Any):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _method_decorate(args[0], MethodKind.Imp)

    def _decor(func: Callable[P, R]) -> Callable[P, R]:
        return _method_decorate(func, MethodKind.Imp)  # type: ignore

    return _decor


#********************************************************************
#* Decorators for TLM interfaces
#********************************************************************

@overload
def tlm_if(cls: TClass) -> TClass: ...

@overload
def tlm_if(*args: Any, **kwargs: Any) -> Callable[[TClass], TClass]: ...

def tlm_if(*args: Any, **kwargs: Any):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _tlm_if_decorate(args[0])

    def _decor(cls: TClass) -> TClass:
        return _tlm_if_decorate(cls)

    return _decor


@overload
def req_fifo(func: Callable[P, R]) -> Callable[P, R]: ...

@overload
def req_fifo(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

def req_fifo(*args: Any, **kwargs: Any):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _req_fifo_decorate(args[0])

    def _decor(func: Callable[P, R]) -> Callable[P, R]:
        return _req_fifo_decorate(func)  # type: ignore

    return _decor


@overload
def rsp_fifo(func: Callable[P, R]) -> Callable[P, R]: ...

@overload
def rsp_fifo(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

def rsp_fifo(*args: Any, **kwargs: Any):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _rsp_fifo_decorate(args[0])

    def _decor(func: Callable[P, R]) -> Callable[P, R]:
        return _rsp_fifo_decorate(func)  # type: ignore

    return _decor


@overload
def reqrsp_fifo(func: Callable[P, R]) -> Callable[P, R]: ...

@overload
def reqrsp_fifo(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

def reqrsp_fifo(*args: Any, **kwargs: Any):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return _reqrsp_fifo_decorate(args[0])

    def _decor(func: Callable[P, R]) -> Callable[P, R]:
        return _reqrsp_fifo_decorate(func)  # type: ignore

    return _decor


def req_mbox(*args, **kwargs):
    pass


def rsp_mbox(*args, **kwargs):
    pass
