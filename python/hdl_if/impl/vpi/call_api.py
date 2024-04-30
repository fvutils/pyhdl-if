#****************************************************************************
#* call_api.py
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
import ctypes
import importlib
import hdl_if.impl.vpi.api as api
from .call_proxy_vpi import CallProxyVPI
from .util import vpi_get_val_int, vpi_get_val_obj, vpi_get_val_ptr, vpi_get_val_str
from .util import vpi_set_val_obj, vpi_set_val_ptr

tf_func_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))

def CallApi_ack(ud):
    print("CallApi_ack", flush=True)
    tf_h = api.vpi_handle(api.vpiSysTfCall, 0)
    args = api.vpi_iterate(api.vpiArgument, tf_h)
    req = vpi_get_val_obj(api.vpi_scan(args))
    rval = vpi_get_val_obj(api.vpi_scan(args))
    req.ev.set(rval)
    return 0;

CallApi_ack_tf = api.t_vpi_systf_data()
CallApi_ack_fp = tf_func_t(CallApi_ack)

def CallApi_init(ud):
    """
    - API-class module
    - API class
    """
    print("CallApi_init", flush=True)
    tf_h = api.vpi_handle(api.vpiSysTfCall, 0)
    args = api.vpi_iterate(api.vpiArgument, tf_h)
    mod_name = vpi_get_val_str(api.vpi_scan(args))
    cls_name = vpi_get_val_str(api.vpi_scan(args))
    ev_h = api.vpi_scan(args)

    mod = importlib.import_module(mod_name)
    cls = getattr(mod, cls_name)

    obj = cls()
    proxy = CallProxyVPI(obj, ev_h)
    setattr(obj, "_proxy", proxy)
    api.vpi_free_object(args)

    vpi_set_val_obj(tf_h, obj)
    return 0

CallApi_init_tf = api.t_vpi_systf_data()
CallApi_init_fp = tf_func_t(CallApi_init)

def CallApi_setMethodId(ud):
    tf_h = api.vpi_handle(api.vpiSysTfCall, 0)
    args = api.vpi_iterate(api.vpiArgument, tf_h)
    obj = vpi_get_val_obj(api.vpi_scan(args))
    print("obj: %s" % str(obj))
    name = vpi_get_val_str(api.vpi_scan(args))
    id = vpi_get_val_int(api.vpi_scan(args))

    proxy : CallProxyVPI = getattr(obj, "_proxy")
    proxy.setMethodId(name, id)
    return 0
CallApi_setMethodId_tf = api.t_vpi_systf_data()
CallApi_setMethodId_fp = tf_func_t(CallApi_setMethodId)

def CallApi_nextReq(ud):
    print("CallApi_next", flush=True)
    tf_h = api.vpi_handle(api.vpiSysTfCall, 0)
    args = api.vpi_iterate(api.vpiArgument, tf_h)
    obj = vpi_get_val_obj(api.vpi_scan(args))

    proxy : CallProxyVPI = getattr(obj, "_proxy")

    req = proxy.nextReq()
    print("req: %s" % str(req), flush=True)
    vpi_set_val_obj(tf_h, req)
    return 0

CallApi_nextReq_tf = api.t_vpi_systf_data()
CallApi_nextReq_fp = tf_func_t(CallApi_nextReq)

def register_vpi_tf():
    global CallApi_init_tf, CallApi_init_fp
    global CallApi_nextReq_tf, CallApi_nextReq_fp

    print("register_vpi_tf", flush=True)

    try:
        CallApi_ack_tf.tfname = "$pyhdl_if_CallApi_ack".encode()
        CallApi_ack_tf.calltf = CallApi_ack_fp
        CallApi_ack_tf.type = api.vpiSysTask
        api.vpi_register_systf(ctypes.byref(CallApi_ack_tf))

        CallApi_init_tf.tfname = "$pyhdl_if_CallApi_init".encode()
        CallApi_init_tf.calltf = CallApi_init_fp
        CallApi_init_tf.type = api.vpiSysFunc
        CallApi_init_tf.sysfunctype = api.vpiSizedFunc
        api.vpi_register_systf(ctypes.byref(CallApi_init_tf))

        CallApi_setMethodId_tf.tfname = "$pyhdl_if_CallApi_setMethodId".encode()
        CallApi_setMethodId_tf.calltf = CallApi_setMethodId_fp
        CallApi_setMethodId_tf.type = api.vpiSysTask
        api.vpi_register_systf(ctypes.byref(CallApi_setMethodId_tf))

        CallApi_nextReq_tf.tfname = "$pyhdl_if_CallApi_nextReq".encode()
        CallApi_nextReq_tf.calltf = CallApi_nextReq_fp
        CallApi_nextReq_tf.type = api.vpiSysFunc
        CallApi_nextReq_tf.sysfunctype = api.vpiSizedFunc
        api.vpi_register_systf(ctypes.byref(CallApi_nextReq_tf))


    except Exception as e:
        print("Exception: %s" % str(e))
        raise e

    pass

