"""Procedural interface between Python and HDL simulators.

``hdl_if`` -- conventionally imported as ``hif`` -- is the top-level entry point.
It re-exports the decorators used to declare an interface between Python and
SystemVerilog, plus the handful of helpers a testbench needs to locate the
libraries and shared SystemVerilog sources that ship with the package.

The usual starting point is :func:`api` together with :func:`imp` and
:func:`exp`::

    import hdl_if as hif

    @hif.api
    class MyApi:
        @hif.imp
        async def from_sv(self, val: int) -> int:
            return val + 1

        @hif.exp
        async def to_sv(self, val: int) -> int: ...

See :doc:`the theory of operation </theory_of_op>` for how the two sides are
connected at elaboration time.
"""

import ctypes
import os
import platform

from .hdl_services import HdlServices
from .backend import Backend
from .impl.decl_rgy import DeclRgy, MethodDecoratorBase, ClsDecoratorBase
from .impl.typeinfo import TypeInfo
from .decorators import (
    api, exp, imp,
    tlm_if, req_fifo, rsp_fifo, reqrsp_fifo, req_mbox, rsp_mbox,
)
from .hdl_obj_rgy import HdlObjRgy

#: The public surface of the package.  Everything not listed here is an
#: implementation detail and may change without notice.
__all__ = [
    # Interface declaration
    "api", "exp", "imp",
    # TLM interface declaration
    "tlm_if", "req_fifo", "rsp_fifo", "reqrsp_fifo", "req_mbox", "rsp_mbox",
    # Registries and services
    "Backend", "HdlObjRgy", "HdlServices", "TypeInfo",
    # Package layout
    "get_backend", "get_entry", "root", "share", "libs",
]

# class s_vpi_vlog_info(ctypes.Structure):
#     _fields_ = [
#         ('argc', ctypes.c_int32),
#         ('argv', ctypes.POINTER(ctypes.c_char_p)),
#         ('product', ctypes.c_char_p),
#         ('version', ctypes.c_char_p)
#     ]


# print("hdl_if.init", flush=True)

# def init():
#     print("::init", flush=True)

# try:
#     exe = ctypes.cdll.LoadLibrary(None)

#     exe.vpi_get_vlog_info.restype = ctypes.c_int
#     exe.vpi_get_vlog_info.argtypes = [
#         ctypes.POINTER(s_vpi_vlog_info)
#     ]

#     info = s_vpi_vlog_info()
#     exe.vpi_get_vlog_info(ctypes.pointer(info))

#     print("argc: %d" % info.argc)

# except Exception as e:
#     print("Exception: %s" % str(e))

def vpi_init():
    """Initialize the VPI backend.

    Called by the simulator-side bootstrap, not by user code.
    """
    import hdl_if.vpi as vpi
    print("::vpi_init")
    vpi.vpi_init()

# def dpi_init(scope):
#     import hdl_if.dpi as dpi
#     print("::dpi_init")

#     dpi.dpi_init(scope)

def get_entry():
    """Return the path to the PyHDL-IF shared library.

    This is the library a simulator loads to obtain the DPI or VPI entry
    points, and the one to name in a simulator command line.

    Returns:
        Absolute path to ``libpyhdl_if`` with the platform's library prefix
        and extension applied.

    Raises:
        Exception: If the library is not present, which means the package was
            installed without its compiled extension.
    """
    hdl_pi_if_dir = os.path.dirname(os.path.abspath(__file__))
    libpref = "lib"
    dllext = ".so"
    if platform.system() == "Windows":
        libpref = ""
        dllext = ".dll"
    elif platform.system() == "Darwin":
        libpref = "lib"
        dllext = ".dylib"

    ext = os.path.join(hdl_pi_if_dir, "%spyhdl_if%s" % (libpref, dllext))
    if os.path.isfile(ext):
        return ext
    else:
        raise Exception("Library path %s doesn't exist" % ext)

def root():
    """Return the root directory of the installed ``hdl_if`` package."""
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pkg_dir)

def share():
    """Return the directory holding the shipped SystemVerilog sources.

    Add this to a simulator's include path to make ``pyhdl_if.sv`` and the
    UVM integration package visible.
    """
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pkg_dir, "share")

def libs(kind="dpi"):
    """Return the libraries to link or load for a given foreign interface.

    Args:
        kind: The foreign interface in use. Currently unused -- every
            supported interface is served by the same library.

    Returns:
        A list of absolute library paths.
    """
    lib_filename = get_entry()

    ret = [ lib_filename ]

    return ret

def get_backend() -> Backend:
    """Return the active :class:`~hdl_if.backend.Backend` singleton.

    The backend abstracts the event loop PyHDL-IF runs on, which differs
    between a bare simulator run and a cocotb run. It is selected
    automatically on first use.

    Note:
        This is a function, not the attribute ``hdl_if.backend`` -- that name
        belongs to the :mod:`hdl_if.backend` module. Equivalent to calling
        :meth:`Backend.inst() <hdl_if.backend.Backend.inst>`.
    """
    return Backend.inst()
