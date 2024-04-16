import ctypes
import hdl_pi_if.vpi.api as vpi

pkg_hndl = None
exp_func = None

def my_task(p):
    global pkg_hndl
    global exp_func
    print("my_task", flush=True)
    import hdl_pi_if.dpi as dpi

    if exp_func is None:
        lib = ctypes.cdll.LoadLibrary(None)
        exp_func = getattr(lib, "exp_func", None)
        print("exp_func=%s" % str(exp_func))

    print("-1- Get scope: %s" % str(dpi.svGetScope()), flush=True)
    print("  Name: %s" % dpi.svGetNameFromScope(dpi.svGetScope()).decode())
    print("-2- Set scope to %s" % str(pkg_hndl))
    dpi.svSetScope(pkg_hndl)
    print("-3- Get scope: %s" % str(dpi.svGetScope()), flush=True)
    exp_func()
    print("TODO: Invoke dpi-export function")

    return 0
my_task_t = None
my_task_h = None


def dpi_init(p):
    import hdl_pi_if.dpi as dpi
    global pkg_hndl
#    pkg_hndl = dpi.svGetScope()
    pkg_hndl = p
    print("dpi_init: %s" % str(pkg_hndl), flush=True)
    print("Name: %s" % dpi.svGetNameFromScope(pkg_hndl).decode())

def vlog_startup():
    global my_task_t, my_task_h
    print("vlog_startup")

    my_task_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))
    my_task_h = my_task_t(my_task)
    try:
        systf_i = vpi.t_vpi_systf_data()
        systf_i.tfname = "$my_task".encode()
        systf_i.type = vpi.vpiSysTask
        print("my_task_h: %s" % str(my_task_h), flush=True)
        systf_i.calltf = my_task_h
#        systf_i.compiletf = None
#        systf_i.sizetf = None
        systf_i.userdata = None
        print("vpi_register_systf=%s" % str(vpi.vpi_register_systf), flush=True)
        ret = vpi.vpi_register_systf(ctypes.pointer(systf_i))
        print("ret: %s" % str(ret), flush=True)
    except Exception as e:
        print("Exception: %s" % str(e), flush=True)
