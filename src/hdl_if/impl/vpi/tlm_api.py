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
from hdl_if.tlm.stream_rgy import StreamRgy
from hdl_if.impl.tlm.stream_req import StreamReq
from hdl_if.impl.tlm.stream_rsp import StreamRsp
from hdl_if.impl.tlm.stream_req_rsp import StreamReqRsp
from hdl_if.impl.vpi.call_proxy_vpi import CallProxyVPI
from .call_proxy_vpi import CallProxyVPI
from .util import vpi_get_val_int, vpi_get_val_obj, vpi_get_val_ptr, vpi_get_val_str
from .util import vpi_set_val_obj, vpi_set_val_ptr

tf_func_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))

def TlmApi_registerStream(ud):
    tf_h = api.vpi_handle(api.vpiSysTfCall, 0)
    args = api.vpi_iterate(api.vpiArgument, tf_h)
    kind = vpi_get_val_str(api.vpi_scan(args))
    ev_h = api.vpi_scan(args)

    tf_s = api.vpi_handle(api.vpiScope, tf_h)
    print("tf_s=%s" % str(tf_s), flush=True)
    path = api.vpi_get_str(api.vpiFullName, tf_s).decode()
    print("path=%s" % path, flush=True)
    path = path[0:-len(".fifo_reg")]

    stream = None
    if kind == "req":
        stream = StreamReq(path)
    elif kind == "rsp":
        stream = StreamRsp(path)
    elif kind == "reqrsp":
        stream = StreamReqRsp(path)
    else:
        raise Exception("unknown FiFO kind %s" % kind, flush=True)
    print("path: %s" % path, flush=True)

    setattr(stream, "_proxy", CallProxyVPI(stream, ev_h))

    rgy = StreamRgy.inst()
    rgy.register_stream(stream)

    vpi_set_val_obj(tf_h, stream)

    return 0

TlmApi_registerStream_tf = api.t_vpi_systf_data()
TlmApi_registerStream_fp = tf_func_t(TlmApi_registerStream)

def TlmApi_reqGet(ud):
    """This method gets the Req object"""
    print("TlmApi_reqGet", flush=True)
    tf_h = api.vpi_handle(api.vpiSysTfCall, 0)
    args = api.vpi_iterate(api.vpiArgument, tf_h)
    req_h = vpi_get_val_obj(api.vpi_scan(args))
    dat_h = api.vpi_scan(args)

    req_v = req_h.args[0]
    print("req_v: 0x%08x" % req_v, flush=True)

    val_s = api.t_vpi_value()
    val_s.format = api.vpiVectorVal
    vval = api.t_vpi_vecval()
    val_s.value.vector = ctypes.pointer(vval)

    vval.aval = req_v

    api.vpi_put_value(dat_h, ctypes.byref(val_s), None, api.vpiNoDelay)

    return 0
TlmApi_reqGet_tf = api.t_vpi_systf_data()
TlmApi_reqGet_fp = tf_func_t(TlmApi_reqGet)

def TlmApi_rspAck(ud):
    """Wrapper around the regular 'ack' method to roll-up result"""
    print("rspAck", flush=True)
    tf_h = api.vpi_handle(api.vpiSysTfCall, 0)
    args = api.vpi_iterate(api.vpiArgument, tf_h)
    req_h = vpi_get_val_obj(api.vpi_scan(args))
    dat_h = api.vpi_scan(args)


    val_s = api.t_vpi_value()
    val_s.format = api.vpiVectorVal

    api.vpi_get_value(dat_h, ctypes.byref(val_s))

    req_h.ev.set(val_s.value.vector[0].aval)


    return 0
TlmApi_rspAck_tf = api.t_vpi_systf_data()
TlmApi_rspAck_fp = tf_func_t(TlmApi_rspAck)


def register_vpi_tf():
    global TlmApi_registerStream_tf, TlmApi_registerStream_fp
    global TlmApi_reqGet_tf, TlmApi_reqGet_fp
    global TlmApi_rspAck_tf, TlmApi_rspAck_fp

    TlmApi_registerStream_tf.tfname = "$pyhdl_if_TlmApi_registerStream".encode()
    TlmApi_registerStream_tf.calltf = TlmApi_registerStream_fp
    TlmApi_registerStream_tf.type = api.vpiSysFunc
    TlmApi_registerStream_tf.sysfunctype = api.vpiSizedFunc
    api.vpi_register_systf(ctypes.byref(TlmApi_registerStream_tf))

    TlmApi_reqGet_tf.tfname = "$pyhdl_if_TlmApi_reqGet".encode()
    TlmApi_reqGet_tf.calltf = TlmApi_reqGet_fp
    TlmApi_reqGet_tf.type = api.vpiSysTask
    api.vpi_register_systf(ctypes.byref(TlmApi_reqGet_tf))

    TlmApi_rspAck_tf.tfname = "$pyhdl_if_TlmApi_rspAck".encode()
    TlmApi_rspAck_tf.calltf = TlmApi_rspAck_fp
    TlmApi_rspAck_tf.type = api.vpiSysTask
    api.vpi_register_systf(ctypes.byref(TlmApi_rspAck_tf))

    pass
