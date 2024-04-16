
import ctypes
import importlib

try:
    import hdl_if.vpi.api as api
    from hdl_if.vpi.api import *
except Exception as e:
    print("Exception(vpi::init::1): %s" % str(e), flush=True)


func_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))
def my_task(cb):
    print("my_task", flush=True)
    sys = api.vpi_handle(api.vpiSysTfCall, 0)
    print("sys: %s" % str(sys))
    return 0

my_task_h = func_t(my_task)

def vpi_init():
    import ctypes
    print("::vpi_init")

    exe = ctypes.cdll.LoadLibrary(None)

    if hasattr(exe, "vpi_get"):
        print("Found VPI")
        try:
            api.load(exe)
        except Exception as e:
            print("Exception: %s" % str(e), flush=True)
    else:
        print("Failed to find VPI")

#     try:

#         systf_i = api.t_vpi_systf_data()
#         systf_i.tfname = "$my_task".encode()
#         systf_i.type = api.vpiSysTask
#         systf_i.subtype = 0
#         systf_i.calltf = my_task_h
# #        systf_i.compiletf = None
# #        systf_i.sizetf = None
#         systf_i.userdata = None
#         ret = api.vpi_register_systf(ctypes.pointer(systf_i))
#         print("ret: %s" % str(ret), flush=True)
#     except Exception as e:
#         print("Exception: %s" % str(e), flush=True)

    try:
        import hdl_pi_if.vpi.pytf as pytf
        pytf.register_tf()
    except Exception as e:
        print("Exception(vpi::init::2): %s" % str(e), flush=True)

    info = api.t_vpi_vlog_info()
    api.vpi_get_vlog_info(ctypes.pointer(info))
    print("product: %s %s" % (info.product.decode(), info.version.decode()))

    for i in range(info.argc):
        arg = info.argv[i]
        arg = arg.decode()
        print("arg: %s" % arg, flush=True)
        if arg.startswith("+pyhdl-pi-if.mod="):
            mod = arg[len("+pyhdl-pi-if.mod="):]

            try:
                imp = importlib.import_module(mod, None)
                if hasattr(imp, "vlog_startup"):
                    try:
                        imp.vlog_startup()
                    except Exception as e:
                        print("Error: vlog_startup in module %s failed: %s" % (
                            mod,
                            str(e)))
                else:
                    print("Error: module %s doesn't have 'vlog_startup' method" % mod)
            except Exception as e:
                print("Failed to load module %s" % mod)

    
