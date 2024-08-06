
import ctypes
import os

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

    for f in os.listdir(hdl_pi_if_dir):
        if f.endswith(".so") and f.startswith("entry"):
            return os.path.join(hdl_pi_if_dir, f)

    raise Exception("Failed to find entry .so")

def root():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pkg_dir)

def share():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pkg_dir, "share")

def libs(kind="dpi"):
    import platform
    import sys
    import sysconfig
    pkg_dir = os.path.dirname(os.path.abspath(__file__))

    if platform.system() == "Windows":
        dllext = ".dll"
    elif platform.system() == "Darwin":
        dllext = ".dyld"
    else:
        dllext = ".so"

    lib = None
    for f in os.listdir(pkg_dir):
        if f.endswith(dllext) and f.startswith("entry"):
            lib = os.path.join(pkg_dir, f)
            break

    if lib is None:
        raise Exception("Failed to find pyhdl-pi-if library")

    lib_filename = lib

    ret = [ lib_filename ]
    if kind != "vpi":
        exe_dir = os.path.dirname(sys.executable)
        python_dir = os.path.dirname(exe_dir)
        python_libdir = sysconfig.get_config_var("LIBDIR")
#        python_libdir = os.path.join(python_dir, 'lib')

        ret.append(os.path.join(python_libdir, sysconfig.get_config_var("LDLIBRARY")))

    return ret
