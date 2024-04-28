#****************************************************************************
#* util.py
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
import hdl_if.impl.vpi.api as api

def vpi_get_val_int(src):
    val_s = api.t_vpi_value()
    val_s.format = api.vpiIntVal
    api.vpi_get_value(src, ctypes.byref(val_s));
    return val_s.value.integer;

def vpi_get_val_str(src):
    val_s = api.t_vpi_value()
    val_s.format = api.vpiStringVal
    api.vpi_get_value(src, ctypes.byref(val_s))
    return val_s.value.str.decode()

def vpi_get_val_obj(src):
    val_s = api.t_vpi_value()
    val_s.format = api.vpiVectorVal

    api.vpi_get_value(src, ctypes.byref(val_s));

    print("aval=0x%08x ; bval=0x%08x" % (val_s.value.vector[0].aval, val_s.value.vector[0].bval))

    ival = val_s.value.vector[0].bval
    ival <<= 32
    ival |= val_s.value.vector[0].aval

    print("ival: 0x%08x" % ival, flush=True)


    if ival != 0:
        oval = ctypes.cast(ival, ctypes.py_object).value 
    else:
        oval = None

    print("oval: %s" % str(oval), flush=True)

    return oval

def vpi_get_val_ptr(src):
    val_s = api.t_vpi_value()
    val_s.format = api.vpiVectorVal

    api.vpi_get_value(src, ctypes.byref(val_s));

    print("aval=0x%08x ; bval=0x%08x" % (val_s.value.vector[0].aval, val_s.value.vector[0].bval))

    ival = val_s.value.vector[0].bval
    ival <<= 32
    ival |= val_s.value.vector[0].aval

    print("ival: 0x%08x" % ival, flush=True)

    pval = ctypes.cast(ival, ctypes.c_void_p)
    oval = ctypes.cast(pval, ctypes.py_object).value

    print("oval: %s" % str(oval), flush=True)

    return oval

def vpi_set_val_ptr(dst, obj):
    vval = api.t_vpi_vecval()
    val_s = api.t_vpi_value()
    val_s.format = api.vpiVectorVal

    obj_py = ctypes.py_object(obj)
    obj_i = ctypes.cast(obj_py, ctypes.c_void_p).value

    vval.aval = obj_i & 0xFFFFFFFF
    obj_i >>= 32
    vval.bval = obj_i & 0xFFFFFFFF

    print("vval.aval=0x%08x vval.bval=0x%08x" % (vval.aval, vval.bval))

    val_s.value.vector = ctypes.pointer(vval)
    api.vpi_put_value(dst, ctypes.byref(val_s), None, api.vpiNoDelay)

def vpi_set_val_obj(dst, obj):
    vval = api.t_vpi_vecval()
    val_s = api.t_vpi_value()
    val_s.format = api.vpiVectorVal

    obj_py = ctypes.py_object(obj).value
    obj_i = id(obj_py)

    vval.aval = obj_i & 0xFFFFFFFF
    obj_i >>= 32
    vval.bval = obj_i & 0xFFFFFFFF

    print("vval.aval=0x%08x vval.bval=0x%08x" % (vval.aval, vval.bval))

    val_s.value.vector = ctypes.pointer(vval)
    api.vpi_put_value(dst, ctypes.byref(val_s), None, api.vpiNoDelay)
