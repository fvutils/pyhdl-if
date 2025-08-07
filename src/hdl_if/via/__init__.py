
import importlib
import sys

from .component_if import ComponentIF
from .object_if import ObjectIF
from .object_type_if import ObjectTypeIF
from .root import Root

print("load(0)", flush=True)

def load(clsname):

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


