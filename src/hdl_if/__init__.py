
import ctypes
import os
import platform

from .hdl_services import HdlServices
from .backend import Backend
from .decorators import *
from .hdl_obj_rgy import *

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
    import hdl_if.vpi as vpi
    print("::vpi_init")
    vpi.vpi_init()

# def dpi_init(scope):
#     import hdl_if.dpi as dpi
#     print("::dpi_init")

#     dpi.dpi_init(scope)

def get_entry():
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
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pkg_dir)

def share():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pkg_dir, "share")

def libs(kind="dpi"):
    import sys
    import sysconfig

    lib_filename = get_entry()

    ret = [ lib_filename ]

    return ret

@property
def backend() -> Backend:
    return Backend.inst()
