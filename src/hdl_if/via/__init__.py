
import importlib
import sys

from .component_if import ComponentIF
from .object_if import ObjectIF
from .object_type_if import ObjectTypeIF
from .root import Root
from .root_if import RootIF

print("load(0)", flush=True)

_root_if = None

def load(clsname, root_if):
    global _root_if

    _root_if = root_if

    cls = None
    try:
        print("load(1) %s path=%s" % (clsname, sys.path), flush=True)
        if clsname.find("::"):
            # Have a filepath with 
            pass

        print("load(2) %s" % clsname, flush=True)
        cls_name = clsname[clsname.rfind(".")+1:]
        mod_name = clsname[:clsname.rfind("."):]

        print("load(3) %s" % clsname, flush=True)
        mod = importlib.import_module(mod_name)
        cls = getattr(mod, cls_name)


        print("load %s" % clsname)
    except Exception as e:
        print("Failed to load %s: %s" % (clsname, str(e)), flush=True)
        raise e
    
    return cls()

def info(level : int, msg : str):
    if _root_if is not None:
        _root_if.info(level, msg)
    else:
        print("Warning: calling via.info without a connected testbench")
        print("VIA Info: %s" % msg)

def info_low(msg : str):
    info(1, msg)

def info_med(msg : str):
    info(2, msg)

def info_high(msg : str):
    info(3, msg)

def error(msg : str):
    if _root_if is not None:
        _root_if.error(msg)
    else:
        print("Warning: calling via.error without a connected testbench")
        print("VIA Error: %s" % msg)

def fatal(msg : str):
    if _root_if is not None:
        _root_if.fatal(msg)
    else:
        print("Warning: calling via.fatal without a connected testbench")
        print("VIA Fatal: %s" % msg)


