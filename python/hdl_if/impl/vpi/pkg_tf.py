import hdl_if.impl.vpi.api as api
from .util import vpi_set_val_obj
import ctypes

tf_func_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))

def hdl_if_None(ud):
    print("None", flush=True)
    tf_h = api.vpi_handle(api.vpiSysTfCall, 0)
    vpi_set_val_obj(tf_h, None)

    return 0
hdl_if_None_tf = api.t_vpi_systf_data()
hdl_if_None_fp = tf_func_t(hdl_if_None)

def hdl_if_idle(ud):
    from hdl_if.backend import Backend
    print("idle", flush=True)
    be = Backend.inst()
    be.idle()
    return 0
hdl_if_idle_tf = api.t_vpi_systf_data()
hdl_if_idle_fp = tf_func_t(hdl_if_idle)



def register():
    global hdl_if_None_tf, hdl_if_None_fp
    global hdl_if_idle_tf, hdl_if_idle_fp

    hdl_if_None_tf.tfname = "$pyhdl_if_None".encode()
    hdl_if_None_tf.calltf = hdl_if_None_fp
    hdl_if_None_tf.type = api.vpiSysFunc
    hdl_if_None_tf.sysfunctype = api.vpiSizedFunc
    api.vpi_register_systf(ctypes.byref(hdl_if_None_tf))

    hdl_if_idle_tf.tfname = "$pyhdl_if_idle".encode()
    hdl_if_idle_tf.calltf = hdl_if_idle_fp
    hdl_if_idle_tf.type = api.vpiSysTask
    api.vpi_register_systf(ctypes.byref(hdl_if_idle_tf))
