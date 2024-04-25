
#****************************************************************************
#* py_tf.py
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
import os
import sysconfig
from .api import t_vpi_systf_data, t_vpi_value, t_vpi_vecval
from .api import vpi_free_object, vpi_handle, vpi_iterate, vpi_scan
from .api import vpi_get_value, vpi_put_value
from .api import vpiArgument, vpiIntVal, vpiStringVal, vpiVectorVal, vpiSysFuncSized, vpiSysTfCall, vpiNoDelay

sizetf_f = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))

def sizetf32(p):
    return 32
sizetf32_fp = sizetf_f(sizetf32)

def sizetf64(p):
    return 64
sizetf64_fp = sizetf_f(sizetf64)

tmp_vecval = (t_vpi_vecval * 4)()

def vpi_get_pval_int(arg_it):
    pval = vpi_scan(arg_it)
    val_s = t_vpi_value()
    val_s.format = vpiIntVal
    vpi_get_value(pval, ctypes.byref(val_s))
    return val_s.value.integer

def vpi_get_pval_ptr(arg_it):
    pval = vpi_scan(arg_it)
    val_s = t_vpi_value()
    val_s.format = vpiVectorVal
    val_s.value.vector = ctypes.cast(ctypes.byref(tmp_vecval), ctypes.POINTER(t_vpi_vecval))
    vpi_get_value(pval, ctypes.byref(val_s))
    ptr_ival = tmp_vecval[1].aval
    ptr_ival <<= 32
    ptr_ival |= tmp_vecval[0].aval
    print("ptr_ival: 0x%08x" % ptr_ival)
    return ctypes.cast(ptr_ival, ctypes.c_void_p)

def vpi_get_pval_str(arg_it):
    pval = vpi_scan(arg_it)
    val_s = t_vpi_value()
    val_s.format = vpiStringVal
    vpi_get_value(pval, ctypes.byref(val_s))
    return val_s.value.str.decode()

def vpi_set_val_int(val_h, val):
    val_s = t_vpi_value()
    val_s.format = vpiIntVal
    val_s.value.integer = val
    vpi_put_value(val_h, ctypes.byref(val_s), None, vpiNoDelay)

def vpi_set_val_ptr(val_h, val):
    val_s = t_vpi_value()
    val_s.format = vpiVectorVal
    val_s.value.vector = ctypes.cast(ctypes.byref(tmp_vecval), ctypes.POINTER(t_vpi_vecval))
    pval = ctypes.pointer(val)
    print("pval: %s" % str(pval))
    ival = id(pval.contents.value)
    print("ival: %08x" % ival)
    tmp_vecval[0].aval = ival
    ival >>= 32
    tmp_vecval[1].aval = ival
    vpi_put_value(val_h, ctypes.byref(val_s), None, vpiNoDelay)

def vpi_set_val_str(val_h, val):
    val_s = t_vpi_value()
    val_s.format = vpiStringVal
    val_s.value.str = val.encode()
    vpi_put_value(val_h, ctypes.byref(val_s), None, vpiNoDelay)

__PyErr_BadArgument_fp = None
__PyErr_BadArgument_f = None
__PyErr_BadArgument_tf = t_vpi_systf_data()
def __PyErr_BadArgument(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyErr_BadArgument_f()
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyErr_CheckSignals_fp = None
__PyErr_CheckSignals_f = None
__PyErr_CheckSignals_tf = t_vpi_systf_data()
def __PyErr_CheckSignals(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyErr_CheckSignals_f()
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyErr_Clear_fp = None
__PyErr_Clear_f = None
__PyErr_Clear_tf = t_vpi_systf_data()
def __PyErr_Clear(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyErr_Clear_f()
    return 0

__PyErr_Display_fp = None
__PyErr_Display_f = None
__PyErr_Display_tf = t_vpi_systf_data()
def __PyErr_Display(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_Display_f(__p0, __p1, __p2)
    return 0

__PyErr_ExceptionMatches_fp = None
__PyErr_ExceptionMatches_f = None
__PyErr_ExceptionMatches_tf = t_vpi_systf_data()
def __PyErr_ExceptionMatches(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_ExceptionMatches_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyErr_GivenExceptionMatches_fp = None
__PyErr_GivenExceptionMatches_f = None
__PyErr_GivenExceptionMatches_tf = t_vpi_systf_data()
def __PyErr_GivenExceptionMatches(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_GivenExceptionMatches_f(__p0, __p1)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyErr_NewException_fp = None
__PyErr_NewException_f = None
__PyErr_NewException_tf = t_vpi_systf_data()
def __PyErr_NewException(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    __base = vpi_get_pval_ptr(__arg_h)
    __dict = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_NewException_f(__name.encode(), __base, __dict)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_NewExceptionWithDoc_fp = None
__PyErr_NewExceptionWithDoc_f = None
__PyErr_NewExceptionWithDoc_tf = t_vpi_systf_data()
def __PyErr_NewExceptionWithDoc(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    __doc = vpi_get_pval_str(__arg_h)
    __base = vpi_get_pval_ptr(__arg_h)
    __dict = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_NewExceptionWithDoc_f(__name.encode(), __doc.encode(), __base, __dict)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_NoMemory_fp = None
__PyErr_NoMemory_f = None
__PyErr_NoMemory_tf = t_vpi_systf_data()
def __PyErr_NoMemory(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyErr_NoMemory_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_Occurred_fp = None
__PyErr_Occurred_f = None
__PyErr_Occurred_tf = t_vpi_systf_data()
def __PyErr_Occurred(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyErr_Occurred_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_Print_fp = None
__PyErr_Print_f = None
__PyErr_Print_tf = t_vpi_systf_data()
def __PyErr_Print(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyErr_Print_f()
    return 0

__PyErr_PrintEx_fp = None
__PyErr_PrintEx_f = None
__PyErr_PrintEx_tf = t_vpi_systf_data()
def __PyErr_PrintEx(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_PrintEx_f(__p0)
    return 0

__PyErr_ProgramText_fp = None
__PyErr_ProgramText_f = None
__PyErr_ProgramText_tf = t_vpi_systf_data()
def __PyErr_ProgramText(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __filename = vpi_get_pval_str(__arg_h)
    __lineno = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_ProgramText_f(__filename.encode(), __lineno)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_ProgramTextObject_fp = None
__PyErr_ProgramTextObject_f = None
__PyErr_ProgramTextObject_tf = t_vpi_systf_data()
def __PyErr_ProgramTextObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __filename = vpi_get_pval_ptr(__arg_h)
    __lineno = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_ProgramTextObject_f(__filename, __lineno)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_RangedSyntaxLocationObject_fp = None
__PyErr_RangedSyntaxLocationObject_f = None
__PyErr_RangedSyntaxLocationObject_tf = t_vpi_systf_data()
def __PyErr_RangedSyntaxLocationObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __filename = vpi_get_pval_ptr(__arg_h)
    __lineno = vpi_get_pval_int(__arg_h)
    __col_offset = vpi_get_pval_int(__arg_h)
    __end_lineno = vpi_get_pval_int(__arg_h)
    __end_col_offset = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_RangedSyntaxLocationObject_f(__filename, __lineno, __col_offset, __end_lineno, __end_col_offset)
    return 0

__PyErr_Restore_fp = None
__PyErr_Restore_f = None
__PyErr_Restore_tf = t_vpi_systf_data()
def __PyErr_Restore(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_Restore_f(__p0, __p1, __p2)
    return 0

__PyErr_SetExcInfo_fp = None
__PyErr_SetExcInfo_f = None
__PyErr_SetExcInfo_tf = t_vpi_systf_data()
def __PyErr_SetExcInfo(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetExcInfo_f(__p0, __p1, __p2)
    return 0

__PyErr_SetFromErrno_fp = None
__PyErr_SetFromErrno_f = None
__PyErr_SetFromErrno_tf = t_vpi_systf_data()
def __PyErr_SetFromErrno(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetFromErrno_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_SetFromErrnoWithFilename_fp = None
__PyErr_SetFromErrnoWithFilename_f = None
__PyErr_SetFromErrnoWithFilename_tf = t_vpi_systf_data()
def __PyErr_SetFromErrnoWithFilename(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __exc = vpi_get_pval_ptr(__arg_h)
    __filename = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetFromErrnoWithFilename_f(__exc, __filename.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_SetFromErrnoWithFilenameObject_fp = None
__PyErr_SetFromErrnoWithFilenameObject_f = None
__PyErr_SetFromErrnoWithFilenameObject_tf = t_vpi_systf_data()
def __PyErr_SetFromErrnoWithFilenameObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetFromErrnoWithFilenameObject_f(__p0, __p1)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_SetFromErrnoWithFilenameObjects_fp = None
__PyErr_SetFromErrnoWithFilenameObjects_f = None
__PyErr_SetFromErrnoWithFilenameObjects_tf = t_vpi_systf_data()
def __PyErr_SetFromErrnoWithFilenameObjects(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetFromErrnoWithFilenameObjects_f(__p0, __p1, __p2)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_SetImportError_fp = None
__PyErr_SetImportError_f = None
__PyErr_SetImportError_tf = t_vpi_systf_data()
def __PyErr_SetImportError(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetImportError_f(__p0, __p1, __p2)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_SetImportErrorSubclass_fp = None
__PyErr_SetImportErrorSubclass_f = None
__PyErr_SetImportErrorSubclass_tf = t_vpi_systf_data()
def __PyErr_SetImportErrorSubclass(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    __p3 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetImportErrorSubclass_f(__p0, __p1, __p2, __p3)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyErr_SetInterrupt_fp = None
__PyErr_SetInterrupt_f = None
__PyErr_SetInterrupt_tf = t_vpi_systf_data()
def __PyErr_SetInterrupt(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyErr_SetInterrupt_f()
    return 0

__PyErr_SetInterruptEx_fp = None
__PyErr_SetInterruptEx_f = None
__PyErr_SetInterruptEx_tf = t_vpi_systf_data()
def __PyErr_SetInterruptEx(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __signum = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetInterruptEx_f(__signum)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyErr_SetNone_fp = None
__PyErr_SetNone_f = None
__PyErr_SetNone_tf = t_vpi_systf_data()
def __PyErr_SetNone(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetNone_f(__p0)
    return 0

__PyErr_SetObject_fp = None
__PyErr_SetObject_f = None
__PyErr_SetObject_tf = t_vpi_systf_data()
def __PyErr_SetObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetObject_f(__p0, __p1)
    return 0

__PyErr_SetString_fp = None
__PyErr_SetString_f = None
__PyErr_SetString_tf = t_vpi_systf_data()
def __PyErr_SetString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __exception = vpi_get_pval_ptr(__arg_h)
    ___string = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SetString_f(__exception, ___string.encode())
    return 0

__PyErr_SyntaxLocation_fp = None
__PyErr_SyntaxLocation_f = None
__PyErr_SyntaxLocation_tf = t_vpi_systf_data()
def __PyErr_SyntaxLocation(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __filename = vpi_get_pval_str(__arg_h)
    __lineno = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SyntaxLocation_f(__filename.encode(), __lineno)
    return 0

__PyErr_SyntaxLocationEx_fp = None
__PyErr_SyntaxLocationEx_f = None
__PyErr_SyntaxLocationEx_tf = t_vpi_systf_data()
def __PyErr_SyntaxLocationEx(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __filename = vpi_get_pval_str(__arg_h)
    __lineno = vpi_get_pval_int(__arg_h)
    __col_offset = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SyntaxLocationEx_f(__filename.encode(), __lineno, __col_offset)
    return 0

__PyErr_SyntaxLocationObject_fp = None
__PyErr_SyntaxLocationObject_f = None
__PyErr_SyntaxLocationObject_tf = t_vpi_systf_data()
def __PyErr_SyntaxLocationObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __filename = vpi_get_pval_ptr(__arg_h)
    __lineno = vpi_get_pval_int(__arg_h)
    __col_offset = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_SyntaxLocationObject_f(__filename, __lineno, __col_offset)
    return 0

__PyErr_WarnEx_fp = None
__PyErr_WarnEx_f = None
__PyErr_WarnEx_tf = t_vpi_systf_data()
def __PyErr_WarnEx(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __category = vpi_get_pval_ptr(__arg_h)
    __message = vpi_get_pval_str(__arg_h)
    __stack_level = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_WarnEx_f(__category, __message.encode(), __stack_level)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyErr_WarnExplicit_fp = None
__PyErr_WarnExplicit_f = None
__PyErr_WarnExplicit_tf = t_vpi_systf_data()
def __PyErr_WarnExplicit(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __category = vpi_get_pval_ptr(__arg_h)
    __message = vpi_get_pval_str(__arg_h)
    __filename = vpi_get_pval_str(__arg_h)
    __lineno = vpi_get_pval_int(__arg_h)
    ___module = vpi_get_pval_str(__arg_h)
    __registry = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_WarnExplicit_f(__category, __message.encode(), __filename.encode(), __lineno, ___module.encode(), __registry)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyErr_WarnExplicitObject_fp = None
__PyErr_WarnExplicitObject_f = None
__PyErr_WarnExplicitObject_tf = t_vpi_systf_data()
def __PyErr_WarnExplicitObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __category = vpi_get_pval_ptr(__arg_h)
    __message = vpi_get_pval_ptr(__arg_h)
    __filename = vpi_get_pval_ptr(__arg_h)
    __lineno = vpi_get_pval_int(__arg_h)
    ___module = vpi_get_pval_ptr(__arg_h)
    __registry = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_WarnExplicitObject_f(__category, __message, __filename, __lineno, ___module, __registry)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyErr_WriteUnraisable_fp = None
__PyErr_WriteUnraisable_f = None
__PyErr_WriteUnraisable_tf = t_vpi_systf_data()
def __PyErr_WriteUnraisable(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyErr_WriteUnraisable_f(__p0)
    return 0

__PyEval_EvalCode_fp = None
__PyEval_EvalCode_f = None
__PyEval_EvalCode_tf = t_vpi_systf_data()
def __PyEval_EvalCode(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyEval_EvalCode_f(__p0, __p1, __p2)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyEval_GetBuiltins_fp = None
__PyEval_GetBuiltins_f = None
__PyEval_GetBuiltins_tf = t_vpi_systf_data()
def __PyEval_GetBuiltins(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyEval_GetBuiltins_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyEval_GetFuncDesc_fp = None
__PyEval_GetFuncDesc_f = None
__PyEval_GetFuncDesc_tf = t_vpi_systf_data()
def __PyEval_GetFuncDesc(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyEval_GetFuncDesc_f(__p0)
    vpi_set_val_str(__tf_h, __rval)
    return 0

__PyEval_GetFuncName_fp = None
__PyEval_GetFuncName_f = None
__PyEval_GetFuncName_tf = t_vpi_systf_data()
def __PyEval_GetFuncName(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyEval_GetFuncName_f(__p0)
    vpi_set_val_str(__tf_h, __rval)
    return 0

__PyEval_GetGlobals_fp = None
__PyEval_GetGlobals_f = None
__PyEval_GetGlobals_tf = t_vpi_systf_data()
def __PyEval_GetGlobals(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyEval_GetGlobals_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyEval_GetLocals_fp = None
__PyEval_GetLocals_f = None
__PyEval_GetLocals_tf = t_vpi_systf_data()
def __PyEval_GetLocals(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyEval_GetLocals_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_AddModule_fp = None
__PyImport_AddModule_f = None
__PyImport_AddModule_tf = t_vpi_systf_data()
def __PyImport_AddModule(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_AddModule_f(__name.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_AddModuleObject_fp = None
__PyImport_AddModuleObject_f = None
__PyImport_AddModuleObject_tf = t_vpi_systf_data()
def __PyImport_AddModuleObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_AddModuleObject_f(__name)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_ExecCodeModule_fp = None
__PyImport_ExecCodeModule_f = None
__PyImport_ExecCodeModule_tf = t_vpi_systf_data()
def __PyImport_ExecCodeModule(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    __co = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ExecCodeModule_f(__name.encode(), __co)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_ExecCodeModuleEx_fp = None
__PyImport_ExecCodeModuleEx_f = None
__PyImport_ExecCodeModuleEx_tf = t_vpi_systf_data()
def __PyImport_ExecCodeModuleEx(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    __co = vpi_get_pval_ptr(__arg_h)
    __pathname = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ExecCodeModuleEx_f(__name.encode(), __co, __pathname.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_ExecCodeModuleObject_fp = None
__PyImport_ExecCodeModuleObject_f = None
__PyImport_ExecCodeModuleObject_tf = t_vpi_systf_data()
def __PyImport_ExecCodeModuleObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_ptr(__arg_h)
    __co = vpi_get_pval_ptr(__arg_h)
    __pathname = vpi_get_pval_ptr(__arg_h)
    __cpathname = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ExecCodeModuleObject_f(__name, __co, __pathname, __cpathname)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_ExecCodeModuleWithPathnames_fp = None
__PyImport_ExecCodeModuleWithPathnames_f = None
__PyImport_ExecCodeModuleWithPathnames_tf = t_vpi_systf_data()
def __PyImport_ExecCodeModuleWithPathnames(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    __co = vpi_get_pval_ptr(__arg_h)
    __pathname = vpi_get_pval_str(__arg_h)
    __cpathname = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ExecCodeModuleWithPathnames_f(__name.encode(), __co, __pathname.encode(), __cpathname.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_GetImporter_fp = None
__PyImport_GetImporter_f = None
__PyImport_GetImporter_tf = t_vpi_systf_data()
def __PyImport_GetImporter(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __path = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_GetImporter_f(__path)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_GetMagicNumber_fp = None
__PyImport_GetMagicNumber_f = None
__PyImport_GetMagicNumber_tf = t_vpi_systf_data()
def __PyImport_GetMagicNumber(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyImport_GetMagicNumber_f()
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyImport_GetMagicTag_fp = None
__PyImport_GetMagicTag_f = None
__PyImport_GetMagicTag_tf = t_vpi_systf_data()
def __PyImport_GetMagicTag(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyImport_GetMagicTag_f()
    vpi_set_val_str(__tf_h, __rval)
    return 0

__PyImport_GetModule_fp = None
__PyImport_GetModule_f = None
__PyImport_GetModule_tf = t_vpi_systf_data()
def __PyImport_GetModule(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_GetModule_f(__name)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_GetModuleDict_fp = None
__PyImport_GetModuleDict_f = None
__PyImport_GetModuleDict_tf = t_vpi_systf_data()
def __PyImport_GetModuleDict(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyImport_GetModuleDict_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_Import_fp = None
__PyImport_Import_f = None
__PyImport_Import_tf = t_vpi_systf_data()
def __PyImport_Import(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_Import_f(__name)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_ImportFrozenModule_fp = None
__PyImport_ImportFrozenModule_f = None
__PyImport_ImportFrozenModule_tf = t_vpi_systf_data()
def __PyImport_ImportFrozenModule(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ImportFrozenModule_f(__name.encode())
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyImport_ImportFrozenModuleObject_fp = None
__PyImport_ImportFrozenModuleObject_f = None
__PyImport_ImportFrozenModuleObject_tf = t_vpi_systf_data()
def __PyImport_ImportFrozenModuleObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ImportFrozenModuleObject_f(__name)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyImport_ImportModule_fp = None
__PyImport_ImportModule_f = None
__PyImport_ImportModule_tf = t_vpi_systf_data()
def __PyImport_ImportModule(ud):
    import importlib
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    print("--> ImportModule_f", flush=True)
    val = "call_python"
    val_b = val.encode()
    print("val: %s ; val_b: %s" % (str(val), str(val_b)))
#    __rval = __PyImport_ImportModule_f(val_b)
    __rval = importlib.import_module(val)
    print("<-- ImportModule_f", flush=True)
    print("__rval=%s" % str(__rval), flush=True)
    vpi_set_val_ptr(__tf_h, ctypes.py_object(__rval))
    return 0

__PyImport_ImportModuleLevel_fp = None
__PyImport_ImportModuleLevel_f = None
__PyImport_ImportModuleLevel_tf = t_vpi_systf_data()
def __PyImport_ImportModuleLevel(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    __globals = vpi_get_pval_ptr(__arg_h)
    __locals = vpi_get_pval_ptr(__arg_h)
    __fromlist = vpi_get_pval_ptr(__arg_h)
    __level = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ImportModuleLevel_f(__name.encode(), __globals, __locals, __fromlist, __level)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_ImportModuleLevelObject_fp = None
__PyImport_ImportModuleLevelObject_f = None
__PyImport_ImportModuleLevelObject_tf = t_vpi_systf_data()
def __PyImport_ImportModuleLevelObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_ptr(__arg_h)
    __globals = vpi_get_pval_ptr(__arg_h)
    __locals = vpi_get_pval_ptr(__arg_h)
    __fromlist = vpi_get_pval_ptr(__arg_h)
    __level = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ImportModuleLevelObject_f(__name, __globals, __locals, __fromlist, __level)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_ImportModuleNoBlock_fp = None
__PyImport_ImportModuleNoBlock_f = None
__PyImport_ImportModuleNoBlock_tf = t_vpi_systf_data()
def __PyImport_ImportModuleNoBlock(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __name = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ImportModuleNoBlock_f(__name.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyImport_ReloadModule_fp = None
__PyImport_ReloadModule_f = None
__PyImport_ReloadModule_tf = t_vpi_systf_data()
def __PyImport_ReloadModule(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __m = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyImport_ReloadModule_f(__m)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_AsDouble_fp = None
__PyLong_AsDouble_f = None
__PyLong_AsDouble_tf = t_vpi_systf_data()
def __PyLong_AsDouble(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsDouble_f(__p0)
    vpi_set_val_double(__tf_h, __rval)
    return 0

__PyLong_AsLong_fp = None
__PyLong_AsLong_f = None
__PyLong_AsLong_tf = t_vpi_systf_data()
def __PyLong_AsLong(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = ctypes.cast(vpi_get_pval_ptr(__arg_h), ctypes.py_object)
    vpi_free_object(__arg_h)
    __rval = int(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyLong_AsLongAndOverflow_fp = None
__PyLong_AsLongAndOverflow_f = None
__PyLong_AsLongAndOverflow_tf = t_vpi_systf_data()
def __PyLong_AsLongAndOverflow(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsLongAndOverflow_f(__p0, __p1)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyLong_AsLongLong_fp = None
__PyLong_AsLongLong_f = None
__PyLong_AsLongLong_tf = t_vpi_systf_data()
def __PyLong_AsLongLong(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsLongLong_f(__p0)
    vpi_set_val_int64(__tf_h, __rval)
    return 0

__PyLong_AsLongLongAndOverflow_fp = None
__PyLong_AsLongLongAndOverflow_f = None
__PyLong_AsLongLongAndOverflow_tf = t_vpi_systf_data()
def __PyLong_AsLongLongAndOverflow(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsLongLongAndOverflow_f(__p0, __p1)
    vpi_set_val_int64(__tf_h, __rval)
    return 0

__PyLong_AsSize_t_fp = None
__PyLong_AsSize_t_f = None
__PyLong_AsSize_t_tf = t_vpi_systf_data()
def __PyLong_AsSize_t(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsSize_t_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyLong_AsSsize_t_fp = None
__PyLong_AsSsize_t_f = None
__PyLong_AsSsize_t_tf = t_vpi_systf_data()
def __PyLong_AsSsize_t(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsSsize_t_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyLong_AsUnsignedLong_fp = None
__PyLong_AsUnsignedLong_f = None
__PyLong_AsUnsignedLong_tf = t_vpi_systf_data()
def __PyLong_AsUnsignedLong(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsUnsignedLong_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyLong_AsUnsignedLongLong_fp = None
__PyLong_AsUnsignedLongLong_f = None
__PyLong_AsUnsignedLongLong_tf = t_vpi_systf_data()
def __PyLong_AsUnsignedLongLong(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsUnsignedLongLong_f(__p0)
    vpi_set_val_int64(__tf_h, __rval)
    return 0

__PyLong_AsUnsignedLongLongMask_fp = None
__PyLong_AsUnsignedLongLongMask_f = None
__PyLong_AsUnsignedLongLongMask_tf = t_vpi_systf_data()
def __PyLong_AsUnsignedLongLongMask(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsUnsignedLongLongMask_f(__p0)
    vpi_set_val_int64(__tf_h, __rval)
    return 0

__PyLong_AsUnsignedLongMask_fp = None
__PyLong_AsUnsignedLongMask_f = None
__PyLong_AsUnsignedLongMask_tf = t_vpi_systf_data()
def __PyLong_AsUnsignedLongMask(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsUnsignedLongMask_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyLong_AsVoidPtr_fp = None
__PyLong_AsVoidPtr_f = None
__PyLong_AsVoidPtr_tf = t_vpi_systf_data()
def __PyLong_AsVoidPtr(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_AsVoidPtr_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_FromDouble_fp = None
__PyLong_FromDouble_f = None
__PyLong_FromDouble_tf = t_vpi_systf_data()
def __PyLong_FromDouble(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_double(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_FromDouble_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_FromLong_fp = None
__PyLong_FromLong_f = None
__PyLong_FromLong_tf = t_vpi_systf_data()
def __PyLong_FromLong(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __p0
    vpi_set_val_ptr(__tf_h, ctypes.py_object(__rval))
    return 0

__PyLong_FromLongLong_fp = None
__PyLong_FromLongLong_f = None
__PyLong_FromLongLong_tf = t_vpi_systf_data()
def __PyLong_FromLongLong(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_int64(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_FromLongLong_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_FromSize_t_fp = None
__PyLong_FromSize_t_f = None
__PyLong_FromSize_t_tf = t_vpi_systf_data()
def __PyLong_FromSize_t(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_FromSize_t_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_FromSsize_t_fp = None
__PyLong_FromSsize_t_f = None
__PyLong_FromSsize_t_tf = t_vpi_systf_data()
def __PyLong_FromSsize_t(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_FromSsize_t_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_FromString_fp = None
__PyLong_FromString_f = None
__PyLong_FromString_tf = t_vpi_systf_data()
def __PyLong_FromString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_str(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_FromString_f(__p0.encode(), __p1, __p2)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_FromUnicodeObject_fp = None
__PyLong_FromUnicodeObject_f = None
__PyLong_FromUnicodeObject_tf = t_vpi_systf_data()
def __PyLong_FromUnicodeObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __u = vpi_get_pval_ptr(__arg_h)
    __base = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_FromUnicodeObject_f(__u, __base)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_FromUnsignedLong_fp = None
__PyLong_FromUnsignedLong_f = None
__PyLong_FromUnsignedLong_tf = t_vpi_systf_data()
def __PyLong_FromUnsignedLong(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_FromUnsignedLong_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_FromUnsignedLongLong_fp = None
__PyLong_FromUnsignedLongLong_f = None
__PyLong_FromUnsignedLongLong_tf = t_vpi_systf_data()
def __PyLong_FromUnsignedLongLong(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_int64(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_FromUnsignedLongLong_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_FromVoidPtr_fp = None
__PyLong_FromVoidPtr_f = None
__PyLong_FromVoidPtr_tf = t_vpi_systf_data()
def __PyLong_FromVoidPtr(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyLong_FromVoidPtr_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyLong_GetInfo_fp = None
__PyLong_GetInfo_f = None
__PyLong_GetInfo_tf = t_vpi_systf_data()
def __PyLong_GetInfo(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyLong_GetInfo_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_ASCII_fp = None
__PyObject_ASCII_f = None
__PyObject_ASCII_tf = t_vpi_systf_data()
def __PyObject_ASCII(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_ASCII_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_AsFileDescriptor_fp = None
__PyObject_AsFileDescriptor_f = None
__PyObject_AsFileDescriptor_tf = t_vpi_systf_data()
def __PyObject_AsFileDescriptor(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_AsFileDescriptor_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_Bytes_fp = None
__PyObject_Bytes_f = None
__PyObject_Bytes_tf = t_vpi_systf_data()
def __PyObject_Bytes(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Bytes_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_Call_fp = None
__PyObject_Call_f = None
__PyObject_Call_tf = t_vpi_systf_data()
def __PyObject_Call(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    callable = ctypes.cast(vpi_get_pval_ptr(__arg_h), ctypes.py_object)
    args = ctypes.cast(vpi_get_pval_ptr(__arg_h), ctypes.py_object)
    kwargs = ctypes.cast(vpi_get_pval_ptr(__arg_h), ctypes.py_object)
    vpi_free_object(__arg_h)
    __rval = callable(*args)
    vpi_set_val_ptr(__tf_h, ctypes.py_object(__rval))
    return 0

__PyObject_CallFinalizer_fp = None
__PyObject_CallFinalizer_f = None
__PyObject_CallFinalizer_tf = t_vpi_systf_data()
def __PyObject_CallFinalizer(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_CallFinalizer_f(__p0)
    return 0

__PyObject_CallFinalizerFromDealloc_fp = None
__PyObject_CallFinalizerFromDealloc_f = None
__PyObject_CallFinalizerFromDealloc_tf = t_vpi_systf_data()
def __PyObject_CallFinalizerFromDealloc(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_CallFinalizerFromDealloc_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_CallNoArgs_fp = None
__PyObject_CallNoArgs_f = None
__PyObject_CallNoArgs_tf = t_vpi_systf_data()
def __PyObject_CallNoArgs(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __func = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_CallNoArgs_f(__func)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_CallObject_fp = None
__PyObject_CallObject_f = None
__PyObject_CallObject_tf = t_vpi_systf_data()
def __PyObject_CallObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __callable = vpi_get_pval_ptr(__arg_h)
    __args = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_CallObject_f(__callable, __args)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_Calloc_fp = None
__PyObject_Calloc_f = None
__PyObject_Calloc_tf = t_vpi_systf_data()
def __PyObject_Calloc(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __nelem = vpi_get_pval_int(__arg_h)
    __elsize = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Calloc_f(__nelem, __elsize)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_CheckBuffer_fp = None
__PyObject_CheckBuffer_f = None
__PyObject_CheckBuffer_tf = t_vpi_systf_data()
def __PyObject_CheckBuffer(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __obj = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_CheckBuffer_f(__obj)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_ClearWeakRefs_fp = None
__PyObject_ClearWeakRefs_f = None
__PyObject_ClearWeakRefs_tf = t_vpi_systf_data()
def __PyObject_ClearWeakRefs(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_ClearWeakRefs_f(__p0)
    return 0

__PyObject_CopyData_fp = None
__PyObject_CopyData_f = None
__PyObject_CopyData_tf = t_vpi_systf_data()
def __PyObject_CopyData(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __dest = vpi_get_pval_ptr(__arg_h)
    __src = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_CopyData_f(__dest, __src)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_DelItem_fp = None
__PyObject_DelItem_f = None
__PyObject_DelItem_tf = t_vpi_systf_data()
def __PyObject_DelItem(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __o = vpi_get_pval_ptr(__arg_h)
    __key = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_DelItem_f(__o, __key)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_DelItemString_fp = None
__PyObject_DelItemString_f = None
__PyObject_DelItemString_tf = t_vpi_systf_data()
def __PyObject_DelItemString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __o = vpi_get_pval_ptr(__arg_h)
    __key = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_DelItemString_f(__o, __key.encode())
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_Dir_fp = None
__PyObject_Dir_f = None
__PyObject_Dir_tf = t_vpi_systf_data()
def __PyObject_Dir(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Dir_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_Format_fp = None
__PyObject_Format_f = None
__PyObject_Format_tf = t_vpi_systf_data()
def __PyObject_Format(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __obj = vpi_get_pval_ptr(__arg_h)
    __format_spec = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Format_f(__obj, __format_spec)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_Free_fp = None
__PyObject_Free_f = None
__PyObject_Free_tf = t_vpi_systf_data()
def __PyObject_Free(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __ptr = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Free_f(__ptr)
    return 0

__PyObject_GC_Del_fp = None
__PyObject_GC_Del_f = None
__PyObject_GC_Del_tf = t_vpi_systf_data()
def __PyObject_GC_Del(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GC_Del_f(__p0)
    return 0

__PyObject_GC_IsFinalized_fp = None
__PyObject_GC_IsFinalized_f = None
__PyObject_GC_IsFinalized_tf = t_vpi_systf_data()
def __PyObject_GC_IsFinalized(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GC_IsFinalized_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_GC_IsTracked_fp = None
__PyObject_GC_IsTracked_f = None
__PyObject_GC_IsTracked_tf = t_vpi_systf_data()
def __PyObject_GC_IsTracked(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GC_IsTracked_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_GC_Track_fp = None
__PyObject_GC_Track_f = None
__PyObject_GC_Track_tf = t_vpi_systf_data()
def __PyObject_GC_Track(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GC_Track_f(__p0)
    return 0

__PyObject_GC_UnTrack_fp = None
__PyObject_GC_UnTrack_f = None
__PyObject_GC_UnTrack_tf = t_vpi_systf_data()
def __PyObject_GC_UnTrack(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GC_UnTrack_f(__p0)
    return 0

__PyObject_GenericGetAttr_fp = None
__PyObject_GenericGetAttr_f = None
__PyObject_GenericGetAttr_tf = t_vpi_systf_data()
def __PyObject_GenericGetAttr(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GenericGetAttr_f(__p0, __p1)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_GenericGetDict_fp = None
__PyObject_GenericGetDict_f = None
__PyObject_GenericGetDict_tf = t_vpi_systf_data()
def __PyObject_GenericGetDict(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GenericGetDict_f(__p0, __p1)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_GenericSetAttr_fp = None
__PyObject_GenericSetAttr_f = None
__PyObject_GenericSetAttr_tf = t_vpi_systf_data()
def __PyObject_GenericSetAttr(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GenericSetAttr_f(__p0, __p1, __p2)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_GenericSetDict_fp = None
__PyObject_GenericSetDict_f = None
__PyObject_GenericSetDict_tf = t_vpi_systf_data()
def __PyObject_GenericSetDict(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GenericSetDict_f(__p0, __p1, __p2)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_GetAIter_fp = None
__PyObject_GetAIter_f = None
__PyObject_GetAIter_tf = t_vpi_systf_data()
def __PyObject_GetAIter(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GetAIter_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_GetAttr_fp = None
__PyObject_GetAttr_f = None
__PyObject_GetAttr_tf = t_vpi_systf_data()
def __PyObject_GetAttr(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GetAttr_f(__p0, __p1)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

#********************************************************************
#* 
#********************************************************************
__PyObject_GetAttrString_fp = None
__PyObject_GetAttrString_f = None
__PyObject_GetAttrString_tf = t_vpi_systf_data()
def __PyObject_GetAttrString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_str(__arg_h)

    __p0 = ctypes.cast(__p0, ctypes.py_object).value

    print("__p0: %s" % str(__p0))
    vpi_free_object(__arg_h)
#    __rval = __PyObject_GetAttrString_f(__p0, __p1.encode())
    __rval = getattr(__p0, __p1)
    print("__rval: %s" % str(__rval))
    vpi_set_val_ptr(__tf_h, ctypes.py_object(__rval))
    return 0

__PyObject_GetItem_fp = None
__PyObject_GetItem_f = None
__PyObject_GetItem_tf = t_vpi_systf_data()
def __PyObject_GetItem(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __o = vpi_get_pval_ptr(__arg_h)
    __key = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GetItem_f(__o, __key)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_GetIter_fp = None
__PyObject_GetIter_f = None
__PyObject_GetIter_tf = t_vpi_systf_data()
def __PyObject_GetIter(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_GetIter_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_HasAttr_fp = None
__PyObject_HasAttr_f = None
__PyObject_HasAttr_tf = t_vpi_systf_data()
def __PyObject_HasAttr(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_HasAttr_f(__p0, __p1)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_HasAttrString_fp = None
__PyObject_HasAttrString_f = None
__PyObject_HasAttrString_tf = t_vpi_systf_data()
def __PyObject_HasAttrString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_HasAttrString_f(__p0, __p1.encode())
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_IS_GC_fp = None
__PyObject_IS_GC_f = None
__PyObject_IS_GC_tf = t_vpi_systf_data()
def __PyObject_IS_GC(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __obj = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_IS_GC_f(__obj)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_Init_fp = None
__PyObject_Init_f = None
__PyObject_Init_tf = t_vpi_systf_data()
def __PyObject_Init(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Init_f(__p0, __p1)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_IsInstance_fp = None
__PyObject_IsInstance_f = None
__PyObject_IsInstance_tf = t_vpi_systf_data()
def __PyObject_IsInstance(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __object = vpi_get_pval_ptr(__arg_h)
    __typeorclass = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_IsInstance_f(__object, __typeorclass)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_IsSubclass_fp = None
__PyObject_IsSubclass_f = None
__PyObject_IsSubclass_tf = t_vpi_systf_data()
def __PyObject_IsSubclass(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __object = vpi_get_pval_ptr(__arg_h)
    __typeorclass = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_IsSubclass_f(__object, __typeorclass)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_IsTrue_fp = None
__PyObject_IsTrue_f = None
__PyObject_IsTrue_tf = t_vpi_systf_data()
def __PyObject_IsTrue(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_IsTrue_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_LengthHint_fp = None
__PyObject_LengthHint_f = None
__PyObject_LengthHint_tf = t_vpi_systf_data()
def __PyObject_LengthHint(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __o = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_LengthHint_f(__o, __p1)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_Malloc_fp = None
__PyObject_Malloc_f = None
__PyObject_Malloc_tf = t_vpi_systf_data()
def __PyObject_Malloc(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __size = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Malloc_f(__size)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_Not_fp = None
__PyObject_Not_f = None
__PyObject_Not_tf = t_vpi_systf_data()
def __PyObject_Not(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Not_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_Realloc_fp = None
__PyObject_Realloc_f = None
__PyObject_Realloc_tf = t_vpi_systf_data()
def __PyObject_Realloc(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __ptr = vpi_get_pval_ptr(__arg_h)
    __new_size = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Realloc_f(__ptr, __new_size)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_Repr_fp = None
__PyObject_Repr_f = None
__PyObject_Repr_tf = t_vpi_systf_data()
def __PyObject_Repr(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Repr_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_RichCompare_fp = None
__PyObject_RichCompare_f = None
__PyObject_RichCompare_tf = t_vpi_systf_data()
def __PyObject_RichCompare(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_RichCompare_f(__p0, __p1, __p2)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_RichCompareBool_fp = None
__PyObject_RichCompareBool_f = None
__PyObject_RichCompareBool_tf = t_vpi_systf_data()
def __PyObject_RichCompareBool(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_RichCompareBool_f(__p0, __p1, __p2)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_SelfIter_fp = None
__PyObject_SelfIter_f = None
__PyObject_SelfIter_tf = t_vpi_systf_data()
def __PyObject_SelfIter(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_SelfIter_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_SetAttr_fp = None
__PyObject_SetAttr_f = None
__PyObject_SetAttr_tf = t_vpi_systf_data()
def __PyObject_SetAttr(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_SetAttr_f(__p0, __p1, __p2)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_SetAttrString_fp = None
__PyObject_SetAttrString_f = None
__PyObject_SetAttrString_tf = t_vpi_systf_data()
def __PyObject_SetAttrString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_str(__arg_h)
    __p2 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_SetAttrString_f(__p0, __p1.encode(), __p2)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_SetItem_fp = None
__PyObject_SetItem_f = None
__PyObject_SetItem_tf = t_vpi_systf_data()
def __PyObject_SetItem(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __o = vpi_get_pval_ptr(__arg_h)
    __key = vpi_get_pval_ptr(__arg_h)
    __v = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_SetItem_f(__o, __key, __v)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_Size_fp = None
__PyObject_Size_f = None
__PyObject_Size_tf = t_vpi_systf_data()
def __PyObject_Size(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __o = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Size_f(__o)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyObject_Str_fp = None
__PyObject_Str_f = None
__PyObject_Str_tf = t_vpi_systf_data()
def __PyObject_Str(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Str_f(__p0)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyObject_Type_fp = None
__PyObject_Type_f = None
__PyObject_Type_tf = t_vpi_systf_data()
def __PyObject_Type(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __o = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyObject_Type_f(__o)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyTuple_GetItem_fp = None
__PyTuple_GetItem_f = None
__PyTuple_GetItem_tf = t_vpi_systf_data()
def __PyTuple_GetItem(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyTuple_GetItem_f(__p0, __p1)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyTuple_GetSlice_fp = None
__PyTuple_GetSlice_f = None
__PyTuple_GetSlice_tf = t_vpi_systf_data()
def __PyTuple_GetSlice(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_int(__arg_h)
    __p2 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyTuple_GetSlice_f(__p0, __p1, __p2)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

#********************************************************************
#* 
#********************************************************************
__PyTuple_New_fp = None
__PyTuple_New_f = None
__PyTuple_New_tf = t_vpi_systf_data()
def __PyTuple_New(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __size = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = [None]*__size
    print("__rval: %s" % str(__rval))
    vpi_set_val_ptr(__tf_h, ctypes.py_object(__rval))
    return 0

__PyTuple_SetItem_fp = None
__PyTuple_SetItem_f = None
__PyTuple_SetItem_tf = t_vpi_systf_data()
def __PyTuple_SetItem(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = ctypes.cast(vpi_get_pval_ptr(__arg_h), ctypes.py_object).value
    __p1 = vpi_get_pval_int(__arg_h)
    __p2 = ctypes.cast(vpi_get_pval_ptr(__arg_h), ctypes.py_object).value
    vpi_free_object(__arg_h)
#    __rval = __PyTuple_SetItem_f(__p0, __p1, __p2)
    print("__pi: %s" % str(__p0))
    __p0[__p1] = __p2
    # if __p1 == 0:
    #     __p0 = (__p2, __p0[1:])
    # elif __p1 == (len(__p0)-1):
    #     __p0 = (__p0[0:-2], __p2)
    # else:
    #     __p0 = (__p0[0:__p1-1], __p2, __p0[__p1+1:])
    vpi_set_val_int(__tf_h, 1)
    return 0

__PyTuple_Size_fp = None
__PyTuple_Size_f = None
__PyTuple_Size_tf = t_vpi_systf_data()
def __PyTuple_Size(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyTuple_Size_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_AsASCIIString_fp = None
__PyUnicode_AsASCIIString_f = None
__PyUnicode_AsASCIIString_tf = t_vpi_systf_data()
def __PyUnicode_AsASCIIString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsASCIIString_f(__unicode)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsCharmapString_fp = None
__PyUnicode_AsCharmapString_f = None
__PyUnicode_AsCharmapString_tf = t_vpi_systf_data()
def __PyUnicode_AsCharmapString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    __mapping = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsCharmapString_f(__unicode, __mapping)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsDecodedObject_fp = None
__PyUnicode_AsDecodedObject_f = None
__PyUnicode_AsDecodedObject_tf = t_vpi_systf_data()
def __PyUnicode_AsDecodedObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    __encoding = vpi_get_pval_str(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsDecodedObject_f(__unicode, __encoding.encode(), __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsDecodedUnicode_fp = None
__PyUnicode_AsDecodedUnicode_f = None
__PyUnicode_AsDecodedUnicode_tf = t_vpi_systf_data()
def __PyUnicode_AsDecodedUnicode(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    __encoding = vpi_get_pval_str(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsDecodedUnicode_f(__unicode, __encoding.encode(), __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsEncodedObject_fp = None
__PyUnicode_AsEncodedObject_f = None
__PyUnicode_AsEncodedObject_tf = t_vpi_systf_data()
def __PyUnicode_AsEncodedObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    __encoding = vpi_get_pval_str(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsEncodedObject_f(__unicode, __encoding.encode(), __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsEncodedString_fp = None
__PyUnicode_AsEncodedString_f = None
__PyUnicode_AsEncodedString_tf = t_vpi_systf_data()
def __PyUnicode_AsEncodedString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    __encoding = vpi_get_pval_str(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsEncodedString_f(__unicode, __encoding.encode(), __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsEncodedUnicode_fp = None
__PyUnicode_AsEncodedUnicode_f = None
__PyUnicode_AsEncodedUnicode_tf = t_vpi_systf_data()
def __PyUnicode_AsEncodedUnicode(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    __encoding = vpi_get_pval_str(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsEncodedUnicode_f(__unicode, __encoding.encode(), __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsLatin1String_fp = None
__PyUnicode_AsLatin1String_f = None
__PyUnicode_AsLatin1String_tf = t_vpi_systf_data()
def __PyUnicode_AsLatin1String(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsLatin1String_f(__unicode)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsRawUnicodeEscapeString_fp = None
__PyUnicode_AsRawUnicodeEscapeString_f = None
__PyUnicode_AsRawUnicodeEscapeString_tf = t_vpi_systf_data()
def __PyUnicode_AsRawUnicodeEscapeString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsRawUnicodeEscapeString_f(__unicode)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsUTF16String_fp = None
__PyUnicode_AsUTF16String_f = None
__PyUnicode_AsUTF16String_tf = t_vpi_systf_data()
def __PyUnicode_AsUTF16String(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsUTF16String_f(__unicode)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsUTF32String_fp = None
__PyUnicode_AsUTF32String_f = None
__PyUnicode_AsUTF32String_tf = t_vpi_systf_data()
def __PyUnicode_AsUTF32String(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsUTF32String_f(__unicode)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsUTF8_fp = None
__PyUnicode_AsUTF8_f = None
__PyUnicode_AsUTF8_tf = t_vpi_systf_data()
def __PyUnicode_AsUTF8(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsUTF8_f(__unicode)
    vpi_set_val_str(__tf_h, __rval)
    return 0

__PyUnicode_AsUTF8AndSize_fp = None
__PyUnicode_AsUTF8AndSize_f = None
__PyUnicode_AsUTF8AndSize_tf = t_vpi_systf_data()
def __PyUnicode_AsUTF8AndSize(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    __size = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsUTF8AndSize_f(__unicode, __size)
    vpi_set_val_str(__tf_h, __rval)
    return 0

__PyUnicode_AsUTF8String_fp = None
__PyUnicode_AsUTF8String_f = None
__PyUnicode_AsUTF8String_tf = t_vpi_systf_data()
def __PyUnicode_AsUTF8String(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsUTF8String_f(__unicode)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_AsUnicodeEscapeString_fp = None
__PyUnicode_AsUnicodeEscapeString_f = None
__PyUnicode_AsUnicodeEscapeString_tf = t_vpi_systf_data()
def __PyUnicode_AsUnicodeEscapeString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_AsUnicodeEscapeString_f(__unicode)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_BuildEncodingMap_fp = None
__PyUnicode_BuildEncodingMap_f = None
__PyUnicode_BuildEncodingMap_tf = t_vpi_systf_data()
def __PyUnicode_BuildEncodingMap(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_BuildEncodingMap_f(___string)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_Compare_fp = None
__PyUnicode_Compare_f = None
__PyUnicode_Compare_tf = t_vpi_systf_data()
def __PyUnicode_Compare(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __left = vpi_get_pval_ptr(__arg_h)
    __right = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Compare_f(__left, __right)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_CompareWithASCIIString_fp = None
__PyUnicode_CompareWithASCIIString_f = None
__PyUnicode_CompareWithASCIIString_tf = t_vpi_systf_data()
def __PyUnicode_CompareWithASCIIString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __left = vpi_get_pval_ptr(__arg_h)
    __right = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_CompareWithASCIIString_f(__left, __right.encode())
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_Concat_fp = None
__PyUnicode_Concat_f = None
__PyUnicode_Concat_tf = t_vpi_systf_data()
def __PyUnicode_Concat(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __left = vpi_get_pval_ptr(__arg_h)
    __right = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Concat_f(__left, __right)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_Contains_fp = None
__PyUnicode_Contains_f = None
__PyUnicode_Contains_tf = t_vpi_systf_data()
def __PyUnicode_Contains(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __container = vpi_get_pval_ptr(__arg_h)
    __element = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Contains_f(__container, __element)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_CopyCharacters_fp = None
__PyUnicode_CopyCharacters_f = None
__PyUnicode_CopyCharacters_tf = t_vpi_systf_data()
def __PyUnicode_CopyCharacters(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __to = vpi_get_pval_ptr(__arg_h)
    __to_start = vpi_get_pval_int(__arg_h)
    __from = vpi_get_pval_ptr(__arg_h)
    __from_start = vpi_get_pval_int(__arg_h)
    __how_many = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_CopyCharacters_f(__to, __to_start, __from, __from_start, __how_many)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_Count_fp = None
__PyUnicode_Count_f = None
__PyUnicode_Count_tf = t_vpi_systf_data()
def __PyUnicode_Count(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __str = vpi_get_pval_ptr(__arg_h)
    __substr = vpi_get_pval_ptr(__arg_h)
    __start = vpi_get_pval_int(__arg_h)
    ___end = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Count_f(__str, __substr, __start, ___end)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_Decode_fp = None
__PyUnicode_Decode_f = None
__PyUnicode_Decode_tf = t_vpi_systf_data()
def __PyUnicode_Decode(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __s = vpi_get_pval_str(__arg_h)
    __size = vpi_get_pval_int(__arg_h)
    __encoding = vpi_get_pval_str(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Decode_f(__s.encode(), __size, __encoding.encode(), __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeASCII_fp = None
__PyUnicode_DecodeASCII_f = None
__PyUnicode_DecodeASCII_tf = t_vpi_systf_data()
def __PyUnicode_DecodeASCII(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeASCII_f(___string.encode(), __length, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeCharmap_fp = None
__PyUnicode_DecodeCharmap_f = None
__PyUnicode_DecodeCharmap_tf = t_vpi_systf_data()
def __PyUnicode_DecodeCharmap(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __mapping = vpi_get_pval_ptr(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeCharmap_f(___string.encode(), __length, __mapping, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeFSDefault_fp = None
__PyUnicode_DecodeFSDefault_f = None
__PyUnicode_DecodeFSDefault_tf = t_vpi_systf_data()
def __PyUnicode_DecodeFSDefault(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __s = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeFSDefault_f(__s.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeFSDefaultAndSize_fp = None
__PyUnicode_DecodeFSDefaultAndSize_f = None
__PyUnicode_DecodeFSDefaultAndSize_tf = t_vpi_systf_data()
def __PyUnicode_DecodeFSDefaultAndSize(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __s = vpi_get_pval_str(__arg_h)
    __size = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeFSDefaultAndSize_f(__s.encode(), __size)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeLatin1_fp = None
__PyUnicode_DecodeLatin1_f = None
__PyUnicode_DecodeLatin1_tf = t_vpi_systf_data()
def __PyUnicode_DecodeLatin1(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeLatin1_f(___string.encode(), __length, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeLocale_fp = None
__PyUnicode_DecodeLocale_f = None
__PyUnicode_DecodeLocale_tf = t_vpi_systf_data()
def __PyUnicode_DecodeLocale(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __str = vpi_get_pval_str(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeLocale_f(__str.encode(), __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeLocaleAndSize_fp = None
__PyUnicode_DecodeLocaleAndSize_f = None
__PyUnicode_DecodeLocaleAndSize_tf = t_vpi_systf_data()
def __PyUnicode_DecodeLocaleAndSize(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __str = vpi_get_pval_str(__arg_h)
    __len = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeLocaleAndSize_f(__str.encode(), __len, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeRawUnicodeEscape_fp = None
__PyUnicode_DecodeRawUnicodeEscape_f = None
__PyUnicode_DecodeRawUnicodeEscape_tf = t_vpi_systf_data()
def __PyUnicode_DecodeRawUnicodeEscape(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeRawUnicodeEscape_f(___string.encode(), __length, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeUTF16_fp = None
__PyUnicode_DecodeUTF16_f = None
__PyUnicode_DecodeUTF16_tf = t_vpi_systf_data()
def __PyUnicode_DecodeUTF16(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    __byteorder = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeUTF16_f(___string.encode(), __length, __errors.encode(), __byteorder)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeUTF16Stateful_fp = None
__PyUnicode_DecodeUTF16Stateful_f = None
__PyUnicode_DecodeUTF16Stateful_tf = t_vpi_systf_data()
def __PyUnicode_DecodeUTF16Stateful(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    __byteorder = vpi_get_pval_ptr(__arg_h)
    __consumed = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeUTF16Stateful_f(___string.encode(), __length, __errors.encode(), __byteorder, __consumed)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeUTF32_fp = None
__PyUnicode_DecodeUTF32_f = None
__PyUnicode_DecodeUTF32_tf = t_vpi_systf_data()
def __PyUnicode_DecodeUTF32(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    __byteorder = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeUTF32_f(___string.encode(), __length, __errors.encode(), __byteorder)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeUTF32Stateful_fp = None
__PyUnicode_DecodeUTF32Stateful_f = None
__PyUnicode_DecodeUTF32Stateful_tf = t_vpi_systf_data()
def __PyUnicode_DecodeUTF32Stateful(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    __byteorder = vpi_get_pval_ptr(__arg_h)
    __consumed = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeUTF32Stateful_f(___string.encode(), __length, __errors.encode(), __byteorder, __consumed)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeUTF7_fp = None
__PyUnicode_DecodeUTF7_f = None
__PyUnicode_DecodeUTF7_tf = t_vpi_systf_data()
def __PyUnicode_DecodeUTF7(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeUTF7_f(___string.encode(), __length, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeUTF7Stateful_fp = None
__PyUnicode_DecodeUTF7Stateful_f = None
__PyUnicode_DecodeUTF7Stateful_tf = t_vpi_systf_data()
def __PyUnicode_DecodeUTF7Stateful(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    __consumed = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeUTF7Stateful_f(___string.encode(), __length, __errors.encode(), __consumed)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeUTF8_fp = None
__PyUnicode_DecodeUTF8_f = None
__PyUnicode_DecodeUTF8_tf = t_vpi_systf_data()
def __PyUnicode_DecodeUTF8(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeUTF8_f(___string.encode(), __length, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeUTF8Stateful_fp = None
__PyUnicode_DecodeUTF8Stateful_f = None
__PyUnicode_DecodeUTF8Stateful_tf = t_vpi_systf_data()
def __PyUnicode_DecodeUTF8Stateful(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    __consumed = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeUTF8Stateful_f(___string.encode(), __length, __errors.encode(), __consumed)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_DecodeUnicodeEscape_fp = None
__PyUnicode_DecodeUnicodeEscape_f = None
__PyUnicode_DecodeUnicodeEscape_tf = t_vpi_systf_data()
def __PyUnicode_DecodeUnicodeEscape(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    ___string = vpi_get_pval_str(__arg_h)
    __length = vpi_get_pval_int(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_DecodeUnicodeEscape_f(___string.encode(), __length, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_EncodeFSDefault_fp = None
__PyUnicode_EncodeFSDefault_f = None
__PyUnicode_EncodeFSDefault_tf = t_vpi_systf_data()
def __PyUnicode_EncodeFSDefault(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_EncodeFSDefault_f(__unicode)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_EncodeLocale_fp = None
__PyUnicode_EncodeLocale_f = None
__PyUnicode_EncodeLocale_tf = t_vpi_systf_data()
def __PyUnicode_EncodeLocale(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_EncodeLocale_f(__unicode, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_FSConverter_fp = None
__PyUnicode_FSConverter_f = None
__PyUnicode_FSConverter_tf = t_vpi_systf_data()
def __PyUnicode_FSConverter(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_FSConverter_f(__p0, __p1)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_FSDecoder_fp = None
__PyUnicode_FSDecoder_f = None
__PyUnicode_FSDecoder_tf = t_vpi_systf_data()
def __PyUnicode_FSDecoder(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_FSDecoder_f(__p0, __p1)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_Find_fp = None
__PyUnicode_Find_f = None
__PyUnicode_Find_tf = t_vpi_systf_data()
def __PyUnicode_Find(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __str = vpi_get_pval_ptr(__arg_h)
    __substr = vpi_get_pval_ptr(__arg_h)
    __start = vpi_get_pval_int(__arg_h)
    ___end = vpi_get_pval_int(__arg_h)
    __direction = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Find_f(__str, __substr, __start, ___end, __direction)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_Format_fp = None
__PyUnicode_Format_f = None
__PyUnicode_Format_tf = t_vpi_systf_data()
def __PyUnicode_Format(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __format = vpi_get_pval_ptr(__arg_h)
    __args = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Format_f(__format, __args)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_FromEncodedObject_fp = None
__PyUnicode_FromEncodedObject_f = None
__PyUnicode_FromEncodedObject_tf = t_vpi_systf_data()
def __PyUnicode_FromEncodedObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __obj = vpi_get_pval_ptr(__arg_h)
    __encoding = vpi_get_pval_str(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_FromEncodedObject_f(__obj, __encoding.encode(), __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_FromObject_fp = None
__PyUnicode_FromObject_f = None
__PyUnicode_FromObject_tf = t_vpi_systf_data()
def __PyUnicode_FromObject(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __obj = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_FromObject_f(__obj)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_FromOrdinal_fp = None
__PyUnicode_FromOrdinal_f = None
__PyUnicode_FromOrdinal_tf = t_vpi_systf_data()
def __PyUnicode_FromOrdinal(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __ordinal = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_FromOrdinal_f(__ordinal)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_FromString_fp = None
__PyUnicode_FromString_f = None
__PyUnicode_FromString_tf = t_vpi_systf_data()
def __PyUnicode_FromString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __u = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_FromString_f(__u.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_FromStringAndSize_fp = None
__PyUnicode_FromStringAndSize_f = None
__PyUnicode_FromStringAndSize_tf = t_vpi_systf_data()
def __PyUnicode_FromStringAndSize(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __u = vpi_get_pval_str(__arg_h)
    __size = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_FromStringAndSize_f(__u.encode(), __size)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_GetDefaultEncoding_fp = None
__PyUnicode_GetDefaultEncoding_f = None
__PyUnicode_GetDefaultEncoding_tf = t_vpi_systf_data()
def __PyUnicode_GetDefaultEncoding(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __PyUnicode_GetDefaultEncoding_f()
    vpi_set_val_str(__tf_h, __rval)
    return 0

__PyUnicode_GetLength_fp = None
__PyUnicode_GetLength_f = None
__PyUnicode_GetLength_tf = t_vpi_systf_data()
def __PyUnicode_GetLength(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_GetLength_f(__unicode)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_GetSize_fp = None
__PyUnicode_GetSize_f = None
__PyUnicode_GetSize_tf = t_vpi_systf_data()
def __PyUnicode_GetSize(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __unicode = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_GetSize_f(__unicode)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_InternFromString_fp = None
__PyUnicode_InternFromString_f = None
__PyUnicode_InternFromString_tf = t_vpi_systf_data()
def __PyUnicode_InternFromString(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __u = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_InternFromString_f(__u.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_IsIdentifier_fp = None
__PyUnicode_IsIdentifier_f = None
__PyUnicode_IsIdentifier_tf = t_vpi_systf_data()
def __PyUnicode_IsIdentifier(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __s = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_IsIdentifier_f(__s)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_Join_fp = None
__PyUnicode_Join_f = None
__PyUnicode_Join_tf = t_vpi_systf_data()
def __PyUnicode_Join(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __separator = vpi_get_pval_ptr(__arg_h)
    __seq = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Join_f(__separator, __seq)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_Partition_fp = None
__PyUnicode_Partition_f = None
__PyUnicode_Partition_tf = t_vpi_systf_data()
def __PyUnicode_Partition(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __s = vpi_get_pval_ptr(__arg_h)
    __sep = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Partition_f(__s, __sep)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_RPartition_fp = None
__PyUnicode_RPartition_f = None
__PyUnicode_RPartition_tf = t_vpi_systf_data()
def __PyUnicode_RPartition(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __s = vpi_get_pval_ptr(__arg_h)
    __sep = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_RPartition_f(__s, __sep)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_RSplit_fp = None
__PyUnicode_RSplit_f = None
__PyUnicode_RSplit_tf = t_vpi_systf_data()
def __PyUnicode_RSplit(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __s = vpi_get_pval_ptr(__arg_h)
    __sep = vpi_get_pval_ptr(__arg_h)
    __maxsplit = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_RSplit_f(__s, __sep, __maxsplit)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_Replace_fp = None
__PyUnicode_Replace_f = None
__PyUnicode_Replace_tf = t_vpi_systf_data()
def __PyUnicode_Replace(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __str = vpi_get_pval_ptr(__arg_h)
    __substr = vpi_get_pval_ptr(__arg_h)
    __replstr = vpi_get_pval_ptr(__arg_h)
    __maxcount = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Replace_f(__str, __substr, __replstr, __maxcount)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_RichCompare_fp = None
__PyUnicode_RichCompare_f = None
__PyUnicode_RichCompare_tf = t_vpi_systf_data()
def __PyUnicode_RichCompare(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __left = vpi_get_pval_ptr(__arg_h)
    __right = vpi_get_pval_ptr(__arg_h)
    __op = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_RichCompare_f(__left, __right, __op)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_Split_fp = None
__PyUnicode_Split_f = None
__PyUnicode_Split_tf = t_vpi_systf_data()
def __PyUnicode_Split(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __s = vpi_get_pval_ptr(__arg_h)
    __sep = vpi_get_pval_ptr(__arg_h)
    __maxsplit = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Split_f(__s, __sep, __maxsplit)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_Splitlines_fp = None
__PyUnicode_Splitlines_f = None
__PyUnicode_Splitlines_tf = t_vpi_systf_data()
def __PyUnicode_Splitlines(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __s = vpi_get_pval_ptr(__arg_h)
    __keepends = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Splitlines_f(__s, __keepends)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_Substring_fp = None
__PyUnicode_Substring_f = None
__PyUnicode_Substring_tf = t_vpi_systf_data()
def __PyUnicode_Substring(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __str = vpi_get_pval_ptr(__arg_h)
    __start = vpi_get_pval_int(__arg_h)
    ___end = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Substring_f(__str, __start, ___end)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__PyUnicode_Tailmatch_fp = None
__PyUnicode_Tailmatch_f = None
__PyUnicode_Tailmatch_tf = t_vpi_systf_data()
def __PyUnicode_Tailmatch(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __str = vpi_get_pval_ptr(__arg_h)
    __substr = vpi_get_pval_ptr(__arg_h)
    __start = vpi_get_pval_int(__arg_h)
    ___end = vpi_get_pval_int(__arg_h)
    __direction = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Tailmatch_f(__str, __substr, __start, ___end, __direction)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__PyUnicode_Translate_fp = None
__PyUnicode_Translate_f = None
__PyUnicode_Translate_tf = t_vpi_systf_data()
def __PyUnicode_Translate(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __str = vpi_get_pval_ptr(__arg_h)
    ___table = vpi_get_pval_ptr(__arg_h)
    __errors = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __PyUnicode_Translate_f(__str, ___table, __errors.encode())
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__Py_DecRef_fp = None
__Py_DecRef_f = None
__Py_DecRef_tf = t_vpi_systf_data()
def __Py_DecRef(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __Py_DecRef_f(__p0)
    return 0

__Py_EnterRecursiveCall_fp = None
__Py_EnterRecursiveCall_f = None
__Py_EnterRecursiveCall_tf = t_vpi_systf_data()
def __Py_EnterRecursiveCall(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __where = vpi_get_pval_str(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __Py_EnterRecursiveCall_f(__where.encode())
    vpi_set_val_int(__tf_h, __rval)
    return 0

__Py_Finalize_fp = None
__Py_Finalize_f = None
__Py_Finalize_tf = t_vpi_systf_data()
def __Py_Finalize(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_Finalize_f()
    return 0

__Py_FinalizeEx_fp = None
__Py_FinalizeEx_f = None
__Py_FinalizeEx_tf = t_vpi_systf_data()
def __Py_FinalizeEx(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_FinalizeEx_f()
    vpi_set_val_int(__tf_h, __rval)
    return 0

__Py_GenericAlias_fp = None
__Py_GenericAlias_f = None
__Py_GenericAlias_tf = t_vpi_systf_data()
def __Py_GenericAlias(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    __p1 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __Py_GenericAlias_f(__p0, __p1)
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__Py_GetBuildInfo_fp = None
__Py_GetBuildInfo_f = None
__Py_GetBuildInfo_tf = t_vpi_systf_data()
def __Py_GetBuildInfo(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetBuildInfo_f()
    vpi_set_val_str(__tf_h, __rval)
    return 0

__Py_GetCompiler_fp = None
__Py_GetCompiler_f = None
__Py_GetCompiler_tf = t_vpi_systf_data()
def __Py_GetCompiler(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetCompiler_f()
    vpi_set_val_str(__tf_h, __rval)
    return 0

__Py_GetCopyright_fp = None
__Py_GetCopyright_f = None
__Py_GetCopyright_tf = t_vpi_systf_data()
def __Py_GetCopyright(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetCopyright_f()
    vpi_set_val_str(__tf_h, __rval)
    return 0

__Py_GetExecPrefix_fp = None
__Py_GetExecPrefix_f = None
__Py_GetExecPrefix_tf = t_vpi_systf_data()
def __Py_GetExecPrefix(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetExecPrefix_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__Py_GetPath_fp = None
__Py_GetPath_f = None
__Py_GetPath_tf = t_vpi_systf_data()
def __Py_GetPath(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetPath_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__Py_GetPlatform_fp = None
__Py_GetPlatform_f = None
__Py_GetPlatform_tf = t_vpi_systf_data()
def __Py_GetPlatform(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetPlatform_f()
    vpi_set_val_str(__tf_h, __rval)
    return 0

__Py_GetPrefix_fp = None
__Py_GetPrefix_f = None
__Py_GetPrefix_tf = t_vpi_systf_data()
def __Py_GetPrefix(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetPrefix_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__Py_GetProgramFullPath_fp = None
__Py_GetProgramFullPath_f = None
__Py_GetProgramFullPath_tf = t_vpi_systf_data()
def __Py_GetProgramFullPath(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetProgramFullPath_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__Py_GetProgramName_fp = None
__Py_GetProgramName_f = None
__Py_GetProgramName_tf = t_vpi_systf_data()
def __Py_GetProgramName(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetProgramName_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__Py_GetPythonHome_fp = None
__Py_GetPythonHome_f = None
__Py_GetPythonHome_tf = t_vpi_systf_data()
def __Py_GetPythonHome(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetPythonHome_f()
    vpi_set_val_ptr(__tf_h, __rval)
    return 0

__Py_GetRecursionLimit_fp = None
__Py_GetRecursionLimit_f = None
__Py_GetRecursionLimit_tf = t_vpi_systf_data()
def __Py_GetRecursionLimit(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetRecursionLimit_f()
    vpi_set_val_int(__tf_h, __rval)
    return 0

__Py_GetVersion_fp = None
__Py_GetVersion_f = None
__Py_GetVersion_tf = t_vpi_systf_data()
def __Py_GetVersion(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_GetVersion_f()
    vpi_set_val_str(__tf_h, __rval)
    return 0

__Py_IncRef_fp = None
__Py_IncRef_f = None
__Py_IncRef_tf = t_vpi_systf_data()
def __Py_IncRef(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __Py_IncRef_f(__p0)
    return 0

__Py_Initialize_fp = None
__Py_Initialize_f = None
__Py_Initialize_tf = t_vpi_systf_data()
def __Py_Initialize(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_Initialize_f()
    return 0

__Py_InitializeEx_fp = None
__Py_InitializeEx_f = None
__Py_InitializeEx_tf = t_vpi_systf_data()
def __Py_InitializeEx(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __Py_InitializeEx_f(__p0)
    return 0

__Py_IsInitialized_fp = None
__Py_IsInitialized_f = None
__Py_IsInitialized_tf = t_vpi_systf_data()
def __Py_IsInitialized(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_IsInitialized_f()
    vpi_set_val_int(__tf_h, __rval)
    return 0

__Py_LeaveRecursiveCall_fp = None
__Py_LeaveRecursiveCall_f = None
__Py_LeaveRecursiveCall_tf = t_vpi_systf_data()
def __Py_LeaveRecursiveCall(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_LeaveRecursiveCall_f()
    return 0

__Py_MakePendingCalls_fp = None
__Py_MakePendingCalls_f = None
__Py_MakePendingCalls_tf = t_vpi_systf_data()
def __Py_MakePendingCalls(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_MakePendingCalls_f()
    vpi_set_val_int(__tf_h, __rval)
    return 0

__Py_ReprEnter_fp = None
__Py_ReprEnter_f = None
__Py_ReprEnter_tf = t_vpi_systf_data()
def __Py_ReprEnter(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __Py_ReprEnter_f(__p0)
    vpi_set_val_int(__tf_h, __rval)
    return 0

__Py_ReprLeave_fp = None
__Py_ReprLeave_f = None
__Py_ReprLeave_tf = t_vpi_systf_data()
def __Py_ReprLeave(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_ptr(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __Py_ReprLeave_f(__p0)
    return 0

__Py_RunMain_fp = None
__Py_RunMain_f = None
__Py_RunMain_tf = t_vpi_systf_data()
def __Py_RunMain(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __rval = __Py_RunMain_f()
    vpi_set_val_int(__tf_h, __rval)
    return 0

__Py_SetRecursionLimit_fp = None
__Py_SetRecursionLimit_f = None
__Py_SetRecursionLimit_tf = t_vpi_systf_data()
def __Py_SetRecursionLimit(ud):
    __tf_h = vpi_handle(vpiSysTfCall, None)
    __arg_h = vpi_iterate(vpiArgument, __tf_h)
    __p0 = vpi_get_pval_int(__arg_h)
    vpi_free_object(__arg_h)
    __rval = __Py_SetRecursionLimit_f(__p0)
    return 0
def register_tf():
    from .api import vpi_register_systf, t_vpi_systf_data, vpiSysFunc, vpiSysTask

    libpy_path = os.path.join(
        sysconfig.get_config_var("LIBDIR"),
        sysconfig.get_config_var("INSTSONAME"))
    print("libpy_path: %s" % str(libpy_path))
    libpy = ctypes.cdll.LoadLibrary(libpy_path)

    tf_func_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))
    global __PyErr_BadArgument_fp, __PyErr_BadArgument_f, __PyErr_BadArgument_tf
    __PyErr_BadArgument_f = getattr(libpy, "PyErr_BadArgument")
    __PyErr_BadArgument_f.restype = ctypes.c_int
    __PyErr_BadArgument_f.argtypes = []
    __PyErr_BadArgument_tf.tfname = "$PyErr_BadArgument".encode()
    __PyErr_BadArgument_tf.type = vpiSysFunc
    __PyErr_BadArgument_fp = tf_func_t(__PyErr_BadArgument)
    __PyErr_BadArgument_tf.calltf = __PyErr_BadArgument_fp
    __PyErr_BadArgument_tf.userdata = None
    name = __PyErr_BadArgument_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_BadArgument_tf))

    global __PyErr_CheckSignals_fp, __PyErr_CheckSignals_f, __PyErr_CheckSignals_tf
    __PyErr_CheckSignals_f = getattr(libpy, "PyErr_CheckSignals")
    __PyErr_CheckSignals_f.restype = ctypes.c_int
    __PyErr_CheckSignals_f.argtypes = []
    __PyErr_CheckSignals_tf.tfname = "$PyErr_CheckSignals".encode()
    __PyErr_CheckSignals_tf.type = vpiSysFunc
    __PyErr_CheckSignals_fp = tf_func_t(__PyErr_CheckSignals)
    __PyErr_CheckSignals_tf.calltf = __PyErr_CheckSignals_fp
    __PyErr_CheckSignals_tf.userdata = None
    name = __PyErr_CheckSignals_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_CheckSignals_tf))

    global __PyErr_Clear_fp, __PyErr_Clear_f, __PyErr_Clear_tf
    __PyErr_Clear_f = getattr(libpy, "PyErr_Clear")
    __PyErr_Clear_f.restype = None
    __PyErr_Clear_f.argtypes = []
    __PyErr_Clear_tf.tfname = "$PyErr_Clear".encode()
    __PyErr_Clear_tf.type = vpiSysTask
    __PyErr_Clear_fp = tf_func_t(__PyErr_Clear)
    __PyErr_Clear_tf.calltf = __PyErr_Clear_fp
    __PyErr_Clear_tf.userdata = None
    name = __PyErr_Clear_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_Clear_tf))

    global __PyErr_Display_fp, __PyErr_Display_f, __PyErr_Display_tf
    __PyErr_Display_f = getattr(libpy, "PyErr_Display")
    __PyErr_Display_f.restype = None
    __PyErr_Display_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_Display_tf.tfname = "$PyErr_Display".encode()
    __PyErr_Display_tf.type = vpiSysTask
    __PyErr_Display_fp = tf_func_t(__PyErr_Display)
    __PyErr_Display_tf.calltf = __PyErr_Display_fp
    __PyErr_Display_tf.userdata = None
    name = __PyErr_Display_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_Display_tf))

    global __PyErr_ExceptionMatches_fp, __PyErr_ExceptionMatches_f, __PyErr_ExceptionMatches_tf
    __PyErr_ExceptionMatches_f = getattr(libpy, "PyErr_ExceptionMatches")
    __PyErr_ExceptionMatches_f.restype = ctypes.c_int
    __PyErr_ExceptionMatches_f.argtypes = [ctypes.c_void_p]
    __PyErr_ExceptionMatches_tf.tfname = "$PyErr_ExceptionMatches".encode()
    __PyErr_ExceptionMatches_tf.type = vpiSysFunc
    __PyErr_ExceptionMatches_fp = tf_func_t(__PyErr_ExceptionMatches)
    __PyErr_ExceptionMatches_tf.calltf = __PyErr_ExceptionMatches_fp
    __PyErr_ExceptionMatches_tf.userdata = None
    name = __PyErr_ExceptionMatches_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_ExceptionMatches_tf))

    global __PyErr_GivenExceptionMatches_fp, __PyErr_GivenExceptionMatches_f, __PyErr_GivenExceptionMatches_tf
    __PyErr_GivenExceptionMatches_f = getattr(libpy, "PyErr_GivenExceptionMatches")
    __PyErr_GivenExceptionMatches_f.restype = ctypes.c_int
    __PyErr_GivenExceptionMatches_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_GivenExceptionMatches_tf.tfname = "$PyErr_GivenExceptionMatches".encode()
    __PyErr_GivenExceptionMatches_tf.type = vpiSysFunc
    __PyErr_GivenExceptionMatches_fp = tf_func_t(__PyErr_GivenExceptionMatches)
    __PyErr_GivenExceptionMatches_tf.calltf = __PyErr_GivenExceptionMatches_fp
    __PyErr_GivenExceptionMatches_tf.userdata = None
    name = __PyErr_GivenExceptionMatches_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_GivenExceptionMatches_tf))

    global __PyErr_NewException_fp, __PyErr_NewException_f, __PyErr_NewException_tf
    __PyErr_NewException_f = getattr(libpy, "PyErr_NewException")
    __PyErr_NewException_f.restype = ctypes.c_void_p
    __PyErr_NewException_f.argtypes = [ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_NewException_tf.tfname = "$PyErr_NewException".encode()
    __PyErr_NewException_tf.type = vpiSysFunc
    __PyErr_NewException_fp = tf_func_t(__PyErr_NewException)
    __PyErr_NewException_tf.calltf = __PyErr_NewException_fp
    __PyErr_NewException_tf.sizetf = sizetf64_fp
    __PyErr_NewException_tf.userdata = None
    name = __PyErr_NewException_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_NewException_tf))

    global __PyErr_NewExceptionWithDoc_fp, __PyErr_NewExceptionWithDoc_f, __PyErr_NewExceptionWithDoc_tf
    __PyErr_NewExceptionWithDoc_f = getattr(libpy, "PyErr_NewExceptionWithDoc")
    __PyErr_NewExceptionWithDoc_f.restype = ctypes.c_void_p
    __PyErr_NewExceptionWithDoc_f.argtypes = [ctypes.c_char_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_NewExceptionWithDoc_tf.tfname = "$PyErr_NewExceptionWithDoc".encode()
    __PyErr_NewExceptionWithDoc_tf.type = vpiSysFunc
    __PyErr_NewExceptionWithDoc_fp = tf_func_t(__PyErr_NewExceptionWithDoc)
    __PyErr_NewExceptionWithDoc_tf.calltf = __PyErr_NewExceptionWithDoc_fp
    __PyErr_NewExceptionWithDoc_tf.sizetf = sizetf64_fp
    __PyErr_NewExceptionWithDoc_tf.userdata = None
    name = __PyErr_NewExceptionWithDoc_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_NewExceptionWithDoc_tf))

    global __PyErr_NoMemory_fp, __PyErr_NoMemory_f, __PyErr_NoMemory_tf
    __PyErr_NoMemory_f = getattr(libpy, "PyErr_NoMemory")
    __PyErr_NoMemory_f.restype = ctypes.c_void_p
    __PyErr_NoMemory_f.argtypes = []
    __PyErr_NoMemory_tf.tfname = "$PyErr_NoMemory".encode()
    __PyErr_NoMemory_tf.type = vpiSysFunc
    __PyErr_NoMemory_fp = tf_func_t(__PyErr_NoMemory)
    __PyErr_NoMemory_tf.calltf = __PyErr_NoMemory_fp
    __PyErr_NoMemory_tf.sizetf = sizetf64_fp
    __PyErr_NoMemory_tf.userdata = None
    name = __PyErr_NoMemory_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_NoMemory_tf))

    global __PyErr_Occurred_fp, __PyErr_Occurred_f, __PyErr_Occurred_tf
    __PyErr_Occurred_f = getattr(libpy, "PyErr_Occurred")
    __PyErr_Occurred_f.restype = ctypes.c_void_p
    __PyErr_Occurred_f.argtypes = []
    __PyErr_Occurred_tf.tfname = "$PyErr_Occurred".encode()
    __PyErr_Occurred_tf.type = vpiSysFunc
    __PyErr_Occurred_fp = tf_func_t(__PyErr_Occurred)
    __PyErr_Occurred_tf.calltf = __PyErr_Occurred_fp
    __PyErr_Occurred_tf.sizetf = sizetf64_fp
    __PyErr_Occurred_tf.userdata = None
    name = __PyErr_Occurred_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_Occurred_tf))

    global __PyErr_Print_fp, __PyErr_Print_f, __PyErr_Print_tf
    __PyErr_Print_f = getattr(libpy, "PyErr_Print")
    __PyErr_Print_f.restype = None
    __PyErr_Print_f.argtypes = []
    __PyErr_Print_tf.tfname = "$PyErr_Print".encode()
    __PyErr_Print_tf.type = vpiSysTask
    __PyErr_Print_fp = tf_func_t(__PyErr_Print)
    __PyErr_Print_tf.calltf = __PyErr_Print_fp
    __PyErr_Print_tf.userdata = None
    name = __PyErr_Print_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_Print_tf))

    global __PyErr_PrintEx_fp, __PyErr_PrintEx_f, __PyErr_PrintEx_tf
    __PyErr_PrintEx_f = getattr(libpy, "PyErr_PrintEx")
    __PyErr_PrintEx_f.restype = None
    __PyErr_PrintEx_f.argtypes = [ctypes.c_int]
    __PyErr_PrintEx_tf.tfname = "$PyErr_PrintEx".encode()
    __PyErr_PrintEx_tf.type = vpiSysTask
    __PyErr_PrintEx_fp = tf_func_t(__PyErr_PrintEx)
    __PyErr_PrintEx_tf.calltf = __PyErr_PrintEx_fp
    __PyErr_PrintEx_tf.userdata = None
    name = __PyErr_PrintEx_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_PrintEx_tf))

    global __PyErr_ProgramText_fp, __PyErr_ProgramText_f, __PyErr_ProgramText_tf
    __PyErr_ProgramText_f = getattr(libpy, "PyErr_ProgramText")
    __PyErr_ProgramText_f.restype = ctypes.c_void_p
    __PyErr_ProgramText_f.argtypes = [ctypes.c_char_p,ctypes.c_int]
    __PyErr_ProgramText_tf.tfname = "$PyErr_ProgramText".encode()
    __PyErr_ProgramText_tf.type = vpiSysFunc
    __PyErr_ProgramText_fp = tf_func_t(__PyErr_ProgramText)
    __PyErr_ProgramText_tf.calltf = __PyErr_ProgramText_fp
    __PyErr_ProgramText_tf.sizetf = sizetf64_fp
    __PyErr_ProgramText_tf.userdata = None
    name = __PyErr_ProgramText_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_ProgramText_tf))

    global __PyErr_ProgramTextObject_fp, __PyErr_ProgramTextObject_f, __PyErr_ProgramTextObject_tf
    __PyErr_ProgramTextObject_f = getattr(libpy, "PyErr_ProgramTextObject")
    __PyErr_ProgramTextObject_f.restype = ctypes.c_void_p
    __PyErr_ProgramTextObject_f.argtypes = [ctypes.c_void_p,ctypes.c_int]
    __PyErr_ProgramTextObject_tf.tfname = "$PyErr_ProgramTextObject".encode()
    __PyErr_ProgramTextObject_tf.type = vpiSysFunc
    __PyErr_ProgramTextObject_fp = tf_func_t(__PyErr_ProgramTextObject)
    __PyErr_ProgramTextObject_tf.calltf = __PyErr_ProgramTextObject_fp
    __PyErr_ProgramTextObject_tf.sizetf = sizetf64_fp
    __PyErr_ProgramTextObject_tf.userdata = None
    name = __PyErr_ProgramTextObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_ProgramTextObject_tf))

    global __PyErr_RangedSyntaxLocationObject_fp, __PyErr_RangedSyntaxLocationObject_f, __PyErr_RangedSyntaxLocationObject_tf
    __PyErr_RangedSyntaxLocationObject_f = getattr(libpy, "PyErr_RangedSyntaxLocationObject")
    __PyErr_RangedSyntaxLocationObject_f.restype = None
    __PyErr_RangedSyntaxLocationObject_f.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
    __PyErr_RangedSyntaxLocationObject_tf.tfname = "$PyErr_RangedSyntaxLocationObject".encode()
    __PyErr_RangedSyntaxLocationObject_tf.type = vpiSysTask
    __PyErr_RangedSyntaxLocationObject_fp = tf_func_t(__PyErr_RangedSyntaxLocationObject)
    __PyErr_RangedSyntaxLocationObject_tf.calltf = __PyErr_RangedSyntaxLocationObject_fp
    __PyErr_RangedSyntaxLocationObject_tf.userdata = None
    name = __PyErr_RangedSyntaxLocationObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_RangedSyntaxLocationObject_tf))

    global __PyErr_Restore_fp, __PyErr_Restore_f, __PyErr_Restore_tf
    __PyErr_Restore_f = getattr(libpy, "PyErr_Restore")
    __PyErr_Restore_f.restype = None
    __PyErr_Restore_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_Restore_tf.tfname = "$PyErr_Restore".encode()
    __PyErr_Restore_tf.type = vpiSysTask
    __PyErr_Restore_fp = tf_func_t(__PyErr_Restore)
    __PyErr_Restore_tf.calltf = __PyErr_Restore_fp
    __PyErr_Restore_tf.userdata = None
    name = __PyErr_Restore_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_Restore_tf))

    global __PyErr_SetExcInfo_fp, __PyErr_SetExcInfo_f, __PyErr_SetExcInfo_tf
    __PyErr_SetExcInfo_f = getattr(libpy, "PyErr_SetExcInfo")
    __PyErr_SetExcInfo_f.restype = None
    __PyErr_SetExcInfo_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_SetExcInfo_tf.tfname = "$PyErr_SetExcInfo".encode()
    __PyErr_SetExcInfo_tf.type = vpiSysTask
    __PyErr_SetExcInfo_fp = tf_func_t(__PyErr_SetExcInfo)
    __PyErr_SetExcInfo_tf.calltf = __PyErr_SetExcInfo_fp
    __PyErr_SetExcInfo_tf.userdata = None
    name = __PyErr_SetExcInfo_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetExcInfo_tf))

    global __PyErr_SetFromErrno_fp, __PyErr_SetFromErrno_f, __PyErr_SetFromErrno_tf
    __PyErr_SetFromErrno_f = getattr(libpy, "PyErr_SetFromErrno")
    __PyErr_SetFromErrno_f.restype = ctypes.c_void_p
    __PyErr_SetFromErrno_f.argtypes = [ctypes.c_void_p]
    __PyErr_SetFromErrno_tf.tfname = "$PyErr_SetFromErrno".encode()
    __PyErr_SetFromErrno_tf.type = vpiSysFunc
    __PyErr_SetFromErrno_fp = tf_func_t(__PyErr_SetFromErrno)
    __PyErr_SetFromErrno_tf.calltf = __PyErr_SetFromErrno_fp
    __PyErr_SetFromErrno_tf.sizetf = sizetf64_fp
    __PyErr_SetFromErrno_tf.userdata = None
    name = __PyErr_SetFromErrno_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetFromErrno_tf))

    global __PyErr_SetFromErrnoWithFilename_fp, __PyErr_SetFromErrnoWithFilename_f, __PyErr_SetFromErrnoWithFilename_tf
    __PyErr_SetFromErrnoWithFilename_f = getattr(libpy, "PyErr_SetFromErrnoWithFilename")
    __PyErr_SetFromErrnoWithFilename_f.restype = ctypes.c_void_p
    __PyErr_SetFromErrnoWithFilename_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    __PyErr_SetFromErrnoWithFilename_tf.tfname = "$PyErr_SetFromErrnoWithFilename".encode()
    __PyErr_SetFromErrnoWithFilename_tf.type = vpiSysFunc
    __PyErr_SetFromErrnoWithFilename_fp = tf_func_t(__PyErr_SetFromErrnoWithFilename)
    __PyErr_SetFromErrnoWithFilename_tf.calltf = __PyErr_SetFromErrnoWithFilename_fp
    __PyErr_SetFromErrnoWithFilename_tf.sizetf = sizetf64_fp
    __PyErr_SetFromErrnoWithFilename_tf.userdata = None
    name = __PyErr_SetFromErrnoWithFilename_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetFromErrnoWithFilename_tf))

    global __PyErr_SetFromErrnoWithFilenameObject_fp, __PyErr_SetFromErrnoWithFilenameObject_f, __PyErr_SetFromErrnoWithFilenameObject_tf
    __PyErr_SetFromErrnoWithFilenameObject_f = getattr(libpy, "PyErr_SetFromErrnoWithFilenameObject")
    __PyErr_SetFromErrnoWithFilenameObject_f.restype = ctypes.c_void_p
    __PyErr_SetFromErrnoWithFilenameObject_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_SetFromErrnoWithFilenameObject_tf.tfname = "$PyErr_SetFromErrnoWithFilenameObject".encode()
    __PyErr_SetFromErrnoWithFilenameObject_tf.type = vpiSysFunc
    __PyErr_SetFromErrnoWithFilenameObject_fp = tf_func_t(__PyErr_SetFromErrnoWithFilenameObject)
    __PyErr_SetFromErrnoWithFilenameObject_tf.calltf = __PyErr_SetFromErrnoWithFilenameObject_fp
    __PyErr_SetFromErrnoWithFilenameObject_tf.sizetf = sizetf64_fp
    __PyErr_SetFromErrnoWithFilenameObject_tf.userdata = None
    name = __PyErr_SetFromErrnoWithFilenameObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetFromErrnoWithFilenameObject_tf))

    global __PyErr_SetFromErrnoWithFilenameObjects_fp, __PyErr_SetFromErrnoWithFilenameObjects_f, __PyErr_SetFromErrnoWithFilenameObjects_tf
    __PyErr_SetFromErrnoWithFilenameObjects_f = getattr(libpy, "PyErr_SetFromErrnoWithFilenameObjects")
    __PyErr_SetFromErrnoWithFilenameObjects_f.restype = ctypes.c_void_p
    __PyErr_SetFromErrnoWithFilenameObjects_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_SetFromErrnoWithFilenameObjects_tf.tfname = "$PyErr_SetFromErrnoWithFilenameObjects".encode()
    __PyErr_SetFromErrnoWithFilenameObjects_tf.type = vpiSysFunc
    __PyErr_SetFromErrnoWithFilenameObjects_fp = tf_func_t(__PyErr_SetFromErrnoWithFilenameObjects)
    __PyErr_SetFromErrnoWithFilenameObjects_tf.calltf = __PyErr_SetFromErrnoWithFilenameObjects_fp
    __PyErr_SetFromErrnoWithFilenameObjects_tf.sizetf = sizetf64_fp
    __PyErr_SetFromErrnoWithFilenameObjects_tf.userdata = None
    name = __PyErr_SetFromErrnoWithFilenameObjects_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetFromErrnoWithFilenameObjects_tf))

    global __PyErr_SetImportError_fp, __PyErr_SetImportError_f, __PyErr_SetImportError_tf
    __PyErr_SetImportError_f = getattr(libpy, "PyErr_SetImportError")
    __PyErr_SetImportError_f.restype = ctypes.c_void_p
    __PyErr_SetImportError_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_SetImportError_tf.tfname = "$PyErr_SetImportError".encode()
    __PyErr_SetImportError_tf.type = vpiSysFunc
    __PyErr_SetImportError_fp = tf_func_t(__PyErr_SetImportError)
    __PyErr_SetImportError_tf.calltf = __PyErr_SetImportError_fp
    __PyErr_SetImportError_tf.sizetf = sizetf64_fp
    __PyErr_SetImportError_tf.userdata = None
    name = __PyErr_SetImportError_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetImportError_tf))

    global __PyErr_SetImportErrorSubclass_fp, __PyErr_SetImportErrorSubclass_f, __PyErr_SetImportErrorSubclass_tf
    __PyErr_SetImportErrorSubclass_f = getattr(libpy, "PyErr_SetImportErrorSubclass")
    __PyErr_SetImportErrorSubclass_f.restype = ctypes.c_void_p
    __PyErr_SetImportErrorSubclass_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_SetImportErrorSubclass_tf.tfname = "$PyErr_SetImportErrorSubclass".encode()
    __PyErr_SetImportErrorSubclass_tf.type = vpiSysFunc
    __PyErr_SetImportErrorSubclass_fp = tf_func_t(__PyErr_SetImportErrorSubclass)
    __PyErr_SetImportErrorSubclass_tf.calltf = __PyErr_SetImportErrorSubclass_fp
    __PyErr_SetImportErrorSubclass_tf.sizetf = sizetf64_fp
    __PyErr_SetImportErrorSubclass_tf.userdata = None
    name = __PyErr_SetImportErrorSubclass_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetImportErrorSubclass_tf))

    global __PyErr_SetInterrupt_fp, __PyErr_SetInterrupt_f, __PyErr_SetInterrupt_tf
    __PyErr_SetInterrupt_f = getattr(libpy, "PyErr_SetInterrupt")
    __PyErr_SetInterrupt_f.restype = None
    __PyErr_SetInterrupt_f.argtypes = []
    __PyErr_SetInterrupt_tf.tfname = "$PyErr_SetInterrupt".encode()
    __PyErr_SetInterrupt_tf.type = vpiSysTask
    __PyErr_SetInterrupt_fp = tf_func_t(__PyErr_SetInterrupt)
    __PyErr_SetInterrupt_tf.calltf = __PyErr_SetInterrupt_fp
    __PyErr_SetInterrupt_tf.userdata = None
    name = __PyErr_SetInterrupt_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetInterrupt_tf))

    global __PyErr_SetInterruptEx_fp, __PyErr_SetInterruptEx_f, __PyErr_SetInterruptEx_tf
    __PyErr_SetInterruptEx_f = getattr(libpy, "PyErr_SetInterruptEx")
    __PyErr_SetInterruptEx_f.restype = ctypes.c_int
    __PyErr_SetInterruptEx_f.argtypes = [ctypes.c_int]
    __PyErr_SetInterruptEx_tf.tfname = "$PyErr_SetInterruptEx".encode()
    __PyErr_SetInterruptEx_tf.type = vpiSysFunc
    __PyErr_SetInterruptEx_fp = tf_func_t(__PyErr_SetInterruptEx)
    __PyErr_SetInterruptEx_tf.calltf = __PyErr_SetInterruptEx_fp
    __PyErr_SetInterruptEx_tf.userdata = None
    name = __PyErr_SetInterruptEx_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetInterruptEx_tf))

    global __PyErr_SetNone_fp, __PyErr_SetNone_f, __PyErr_SetNone_tf
    __PyErr_SetNone_f = getattr(libpy, "PyErr_SetNone")
    __PyErr_SetNone_f.restype = None
    __PyErr_SetNone_f.argtypes = [ctypes.c_void_p]
    __PyErr_SetNone_tf.tfname = "$PyErr_SetNone".encode()
    __PyErr_SetNone_tf.type = vpiSysTask
    __PyErr_SetNone_fp = tf_func_t(__PyErr_SetNone)
    __PyErr_SetNone_tf.calltf = __PyErr_SetNone_fp
    __PyErr_SetNone_tf.userdata = None
    name = __PyErr_SetNone_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetNone_tf))

    global __PyErr_SetObject_fp, __PyErr_SetObject_f, __PyErr_SetObject_tf
    __PyErr_SetObject_f = getattr(libpy, "PyErr_SetObject")
    __PyErr_SetObject_f.restype = None
    __PyErr_SetObject_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_SetObject_tf.tfname = "$PyErr_SetObject".encode()
    __PyErr_SetObject_tf.type = vpiSysTask
    __PyErr_SetObject_fp = tf_func_t(__PyErr_SetObject)
    __PyErr_SetObject_tf.calltf = __PyErr_SetObject_fp
    __PyErr_SetObject_tf.userdata = None
    name = __PyErr_SetObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetObject_tf))

    global __PyErr_SetString_fp, __PyErr_SetString_f, __PyErr_SetString_tf
    __PyErr_SetString_f = getattr(libpy, "PyErr_SetString")
    __PyErr_SetString_f.restype = None
    __PyErr_SetString_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    __PyErr_SetString_tf.tfname = "$PyErr_SetString".encode()
    __PyErr_SetString_tf.type = vpiSysTask
    __PyErr_SetString_fp = tf_func_t(__PyErr_SetString)
    __PyErr_SetString_tf.calltf = __PyErr_SetString_fp
    __PyErr_SetString_tf.userdata = None
    name = __PyErr_SetString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SetString_tf))

    global __PyErr_SyntaxLocation_fp, __PyErr_SyntaxLocation_f, __PyErr_SyntaxLocation_tf
    __PyErr_SyntaxLocation_f = getattr(libpy, "PyErr_SyntaxLocation")
    __PyErr_SyntaxLocation_f.restype = None
    __PyErr_SyntaxLocation_f.argtypes = [ctypes.c_char_p,ctypes.c_int]
    __PyErr_SyntaxLocation_tf.tfname = "$PyErr_SyntaxLocation".encode()
    __PyErr_SyntaxLocation_tf.type = vpiSysTask
    __PyErr_SyntaxLocation_fp = tf_func_t(__PyErr_SyntaxLocation)
    __PyErr_SyntaxLocation_tf.calltf = __PyErr_SyntaxLocation_fp
    __PyErr_SyntaxLocation_tf.userdata = None
    name = __PyErr_SyntaxLocation_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SyntaxLocation_tf))

    global __PyErr_SyntaxLocationEx_fp, __PyErr_SyntaxLocationEx_f, __PyErr_SyntaxLocationEx_tf
    __PyErr_SyntaxLocationEx_f = getattr(libpy, "PyErr_SyntaxLocationEx")
    __PyErr_SyntaxLocationEx_f.restype = None
    __PyErr_SyntaxLocationEx_f.argtypes = [ctypes.c_char_p,ctypes.c_int,ctypes.c_int]
    __PyErr_SyntaxLocationEx_tf.tfname = "$PyErr_SyntaxLocationEx".encode()
    __PyErr_SyntaxLocationEx_tf.type = vpiSysTask
    __PyErr_SyntaxLocationEx_fp = tf_func_t(__PyErr_SyntaxLocationEx)
    __PyErr_SyntaxLocationEx_tf.calltf = __PyErr_SyntaxLocationEx_fp
    __PyErr_SyntaxLocationEx_tf.userdata = None
    name = __PyErr_SyntaxLocationEx_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SyntaxLocationEx_tf))

    global __PyErr_SyntaxLocationObject_fp, __PyErr_SyntaxLocationObject_f, __PyErr_SyntaxLocationObject_tf
    __PyErr_SyntaxLocationObject_f = getattr(libpy, "PyErr_SyntaxLocationObject")
    __PyErr_SyntaxLocationObject_f.restype = None
    __PyErr_SyntaxLocationObject_f.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
    __PyErr_SyntaxLocationObject_tf.tfname = "$PyErr_SyntaxLocationObject".encode()
    __PyErr_SyntaxLocationObject_tf.type = vpiSysTask
    __PyErr_SyntaxLocationObject_fp = tf_func_t(__PyErr_SyntaxLocationObject)
    __PyErr_SyntaxLocationObject_tf.calltf = __PyErr_SyntaxLocationObject_fp
    __PyErr_SyntaxLocationObject_tf.userdata = None
    name = __PyErr_SyntaxLocationObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_SyntaxLocationObject_tf))

    global __PyErr_WarnEx_fp, __PyErr_WarnEx_f, __PyErr_WarnEx_tf
    __PyErr_WarnEx_f = getattr(libpy, "PyErr_WarnEx")
    __PyErr_WarnEx_f.restype = ctypes.c_int
    __PyErr_WarnEx_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_uint]
    __PyErr_WarnEx_tf.tfname = "$PyErr_WarnEx".encode()
    __PyErr_WarnEx_tf.type = vpiSysFunc
    __PyErr_WarnEx_fp = tf_func_t(__PyErr_WarnEx)
    __PyErr_WarnEx_tf.calltf = __PyErr_WarnEx_fp
    __PyErr_WarnEx_tf.userdata = None
    name = __PyErr_WarnEx_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_WarnEx_tf))

    global __PyErr_WarnExplicit_fp, __PyErr_WarnExplicit_f, __PyErr_WarnExplicit_tf
    __PyErr_WarnExplicit_f = getattr(libpy, "PyErr_WarnExplicit")
    __PyErr_WarnExplicit_f.restype = ctypes.c_int
    __PyErr_WarnExplicit_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_void_p]
    __PyErr_WarnExplicit_tf.tfname = "$PyErr_WarnExplicit".encode()
    __PyErr_WarnExplicit_tf.type = vpiSysFunc
    __PyErr_WarnExplicit_fp = tf_func_t(__PyErr_WarnExplicit)
    __PyErr_WarnExplicit_tf.calltf = __PyErr_WarnExplicit_fp
    __PyErr_WarnExplicit_tf.userdata = None
    name = __PyErr_WarnExplicit_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_WarnExplicit_tf))

    global __PyErr_WarnExplicitObject_fp, __PyErr_WarnExplicitObject_f, __PyErr_WarnExplicitObject_tf
    __PyErr_WarnExplicitObject_f = getattr(libpy, "PyErr_WarnExplicitObject")
    __PyErr_WarnExplicitObject_f.restype = ctypes.c_int
    __PyErr_WarnExplicitObject_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p]
    __PyErr_WarnExplicitObject_tf.tfname = "$PyErr_WarnExplicitObject".encode()
    __PyErr_WarnExplicitObject_tf.type = vpiSysFunc
    __PyErr_WarnExplicitObject_fp = tf_func_t(__PyErr_WarnExplicitObject)
    __PyErr_WarnExplicitObject_tf.calltf = __PyErr_WarnExplicitObject_fp
    __PyErr_WarnExplicitObject_tf.userdata = None
    name = __PyErr_WarnExplicitObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_WarnExplicitObject_tf))

    global __PyErr_WriteUnraisable_fp, __PyErr_WriteUnraisable_f, __PyErr_WriteUnraisable_tf
    __PyErr_WriteUnraisable_f = getattr(libpy, "PyErr_WriteUnraisable")
    __PyErr_WriteUnraisable_f.restype = None
    __PyErr_WriteUnraisable_f.argtypes = [ctypes.c_void_p]
    __PyErr_WriteUnraisable_tf.tfname = "$PyErr_WriteUnraisable".encode()
    __PyErr_WriteUnraisable_tf.type = vpiSysTask
    __PyErr_WriteUnraisable_fp = tf_func_t(__PyErr_WriteUnraisable)
    __PyErr_WriteUnraisable_tf.calltf = __PyErr_WriteUnraisable_fp
    __PyErr_WriteUnraisable_tf.userdata = None
    name = __PyErr_WriteUnraisable_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyErr_WriteUnraisable_tf))

    global __PyEval_EvalCode_fp, __PyEval_EvalCode_f, __PyEval_EvalCode_tf
    __PyEval_EvalCode_f = getattr(libpy, "PyEval_EvalCode")
    __PyEval_EvalCode_f.restype = ctypes.c_void_p
    __PyEval_EvalCode_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyEval_EvalCode_tf.tfname = "$PyEval_EvalCode".encode()
    __PyEval_EvalCode_tf.type = vpiSysFunc
    __PyEval_EvalCode_fp = tf_func_t(__PyEval_EvalCode)
    __PyEval_EvalCode_tf.calltf = __PyEval_EvalCode_fp
    __PyEval_EvalCode_tf.sizetf = sizetf64_fp
    __PyEval_EvalCode_tf.userdata = None
    name = __PyEval_EvalCode_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyEval_EvalCode_tf))

    global __PyEval_GetBuiltins_fp, __PyEval_GetBuiltins_f, __PyEval_GetBuiltins_tf
    __PyEval_GetBuiltins_f = getattr(libpy, "PyEval_GetBuiltins")
    __PyEval_GetBuiltins_f.restype = ctypes.c_void_p
    __PyEval_GetBuiltins_f.argtypes = []
    __PyEval_GetBuiltins_tf.tfname = "$PyEval_GetBuiltins".encode()
    __PyEval_GetBuiltins_tf.type = vpiSysFunc
    __PyEval_GetBuiltins_fp = tf_func_t(__PyEval_GetBuiltins)
    __PyEval_GetBuiltins_tf.calltf = __PyEval_GetBuiltins_fp
    __PyEval_GetBuiltins_tf.sizetf = sizetf64_fp
    __PyEval_GetBuiltins_tf.userdata = None
    name = __PyEval_GetBuiltins_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyEval_GetBuiltins_tf))

    global __PyEval_GetFuncDesc_fp, __PyEval_GetFuncDesc_f, __PyEval_GetFuncDesc_tf
    __PyEval_GetFuncDesc_f = getattr(libpy, "PyEval_GetFuncDesc")
    __PyEval_GetFuncDesc_f.restype = ctypes.c_char_p
    __PyEval_GetFuncDesc_f.argtypes = [ctypes.c_void_p]
    __PyEval_GetFuncDesc_tf.tfname = "$PyEval_GetFuncDesc".encode()
    __PyEval_GetFuncDesc_tf.type = vpiSysTask
    __PyEval_GetFuncDesc_fp = tf_func_t(__PyEval_GetFuncDesc)
    __PyEval_GetFuncDesc_tf.calltf = __PyEval_GetFuncDesc_fp
    __PyEval_GetFuncDesc_tf.userdata = None
    name = __PyEval_GetFuncDesc_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyEval_GetFuncDesc_tf))

    global __PyEval_GetFuncName_fp, __PyEval_GetFuncName_f, __PyEval_GetFuncName_tf
    __PyEval_GetFuncName_f = getattr(libpy, "PyEval_GetFuncName")
    __PyEval_GetFuncName_f.restype = ctypes.c_char_p
    __PyEval_GetFuncName_f.argtypes = [ctypes.c_void_p]
    __PyEval_GetFuncName_tf.tfname = "$PyEval_GetFuncName".encode()
    __PyEval_GetFuncName_tf.type = vpiSysTask
    __PyEval_GetFuncName_fp = tf_func_t(__PyEval_GetFuncName)
    __PyEval_GetFuncName_tf.calltf = __PyEval_GetFuncName_fp
    __PyEval_GetFuncName_tf.userdata = None
    name = __PyEval_GetFuncName_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyEval_GetFuncName_tf))

    global __PyEval_GetGlobals_fp, __PyEval_GetGlobals_f, __PyEval_GetGlobals_tf
    __PyEval_GetGlobals_f = getattr(libpy, "PyEval_GetGlobals")
    __PyEval_GetGlobals_f.restype = ctypes.c_void_p
    __PyEval_GetGlobals_f.argtypes = []
    __PyEval_GetGlobals_tf.tfname = "$PyEval_GetGlobals".encode()
    __PyEval_GetGlobals_tf.type = vpiSysFunc
    __PyEval_GetGlobals_fp = tf_func_t(__PyEval_GetGlobals)
    __PyEval_GetGlobals_tf.calltf = __PyEval_GetGlobals_fp
    __PyEval_GetGlobals_tf.sizetf = sizetf64_fp
    __PyEval_GetGlobals_tf.userdata = None
    name = __PyEval_GetGlobals_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyEval_GetGlobals_tf))

    global __PyEval_GetLocals_fp, __PyEval_GetLocals_f, __PyEval_GetLocals_tf
    __PyEval_GetLocals_f = getattr(libpy, "PyEval_GetLocals")
    __PyEval_GetLocals_f.restype = ctypes.c_void_p
    __PyEval_GetLocals_f.argtypes = []
    __PyEval_GetLocals_tf.tfname = "$PyEval_GetLocals".encode()
    __PyEval_GetLocals_tf.type = vpiSysFunc
    __PyEval_GetLocals_fp = tf_func_t(__PyEval_GetLocals)
    __PyEval_GetLocals_tf.calltf = __PyEval_GetLocals_fp
    __PyEval_GetLocals_tf.sizetf = sizetf64_fp
    __PyEval_GetLocals_tf.userdata = None
    name = __PyEval_GetLocals_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyEval_GetLocals_tf))

    global __PyImport_AddModule_fp, __PyImport_AddModule_f, __PyImport_AddModule_tf
    __PyImport_AddModule_f = getattr(libpy, "PyImport_AddModule")
    __PyImport_AddModule_f.restype = ctypes.c_void_p
    __PyImport_AddModule_f.argtypes = [ctypes.c_char_p]
    __PyImport_AddModule_tf.tfname = "$PyImport_AddModule".encode()
    __PyImport_AddModule_tf.type = vpiSysFunc
    __PyImport_AddModule_fp = tf_func_t(__PyImport_AddModule)
    __PyImport_AddModule_tf.calltf = __PyImport_AddModule_fp
    __PyImport_AddModule_tf.sizetf = sizetf64_fp
    __PyImport_AddModule_tf.userdata = None
    name = __PyImport_AddModule_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_AddModule_tf))

    global __PyImport_AddModuleObject_fp, __PyImport_AddModuleObject_f, __PyImport_AddModuleObject_tf
    __PyImport_AddModuleObject_f = getattr(libpy, "PyImport_AddModuleObject")
    __PyImport_AddModuleObject_f.restype = ctypes.c_void_p
    __PyImport_AddModuleObject_f.argtypes = [ctypes.c_void_p]
    __PyImport_AddModuleObject_tf.tfname = "$PyImport_AddModuleObject".encode()
    __PyImport_AddModuleObject_tf.type = vpiSysFunc
    __PyImport_AddModuleObject_fp = tf_func_t(__PyImport_AddModuleObject)
    __PyImport_AddModuleObject_tf.calltf = __PyImport_AddModuleObject_fp
    __PyImport_AddModuleObject_tf.sizetf = sizetf64_fp
    __PyImport_AddModuleObject_tf.userdata = None
    name = __PyImport_AddModuleObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_AddModuleObject_tf))

    global __PyImport_ExecCodeModule_fp, __PyImport_ExecCodeModule_f, __PyImport_ExecCodeModule_tf
    __PyImport_ExecCodeModule_f = getattr(libpy, "PyImport_ExecCodeModule")
    __PyImport_ExecCodeModule_f.restype = ctypes.c_void_p
    __PyImport_ExecCodeModule_f.argtypes = [ctypes.c_char_p,ctypes.c_void_p]
    __PyImport_ExecCodeModule_tf.tfname = "$PyImport_ExecCodeModule".encode()
    __PyImport_ExecCodeModule_tf.type = vpiSysFunc
    __PyImport_ExecCodeModule_fp = tf_func_t(__PyImport_ExecCodeModule)
    __PyImport_ExecCodeModule_tf.calltf = __PyImport_ExecCodeModule_fp
    __PyImport_ExecCodeModule_tf.sizetf = sizetf64_fp
    __PyImport_ExecCodeModule_tf.userdata = None
    name = __PyImport_ExecCodeModule_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ExecCodeModule_tf))

    global __PyImport_ExecCodeModuleEx_fp, __PyImport_ExecCodeModuleEx_f, __PyImport_ExecCodeModuleEx_tf
    __PyImport_ExecCodeModuleEx_f = getattr(libpy, "PyImport_ExecCodeModuleEx")
    __PyImport_ExecCodeModuleEx_f.restype = ctypes.c_void_p
    __PyImport_ExecCodeModuleEx_f.argtypes = [ctypes.c_char_p,ctypes.c_void_p,ctypes.c_char_p]
    __PyImport_ExecCodeModuleEx_tf.tfname = "$PyImport_ExecCodeModuleEx".encode()
    __PyImport_ExecCodeModuleEx_tf.type = vpiSysFunc
    __PyImport_ExecCodeModuleEx_fp = tf_func_t(__PyImport_ExecCodeModuleEx)
    __PyImport_ExecCodeModuleEx_tf.calltf = __PyImport_ExecCodeModuleEx_fp
    __PyImport_ExecCodeModuleEx_tf.sizetf = sizetf64_fp
    __PyImport_ExecCodeModuleEx_tf.userdata = None
    name = __PyImport_ExecCodeModuleEx_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ExecCodeModuleEx_tf))

    global __PyImport_ExecCodeModuleObject_fp, __PyImport_ExecCodeModuleObject_f, __PyImport_ExecCodeModuleObject_tf
    __PyImport_ExecCodeModuleObject_f = getattr(libpy, "PyImport_ExecCodeModuleObject")
    __PyImport_ExecCodeModuleObject_f.restype = ctypes.c_void_p
    __PyImport_ExecCodeModuleObject_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyImport_ExecCodeModuleObject_tf.tfname = "$PyImport_ExecCodeModuleObject".encode()
    __PyImport_ExecCodeModuleObject_tf.type = vpiSysFunc
    __PyImport_ExecCodeModuleObject_fp = tf_func_t(__PyImport_ExecCodeModuleObject)
    __PyImport_ExecCodeModuleObject_tf.calltf = __PyImport_ExecCodeModuleObject_fp
    __PyImport_ExecCodeModuleObject_tf.sizetf = sizetf64_fp
    __PyImport_ExecCodeModuleObject_tf.userdata = None
    name = __PyImport_ExecCodeModuleObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ExecCodeModuleObject_tf))

    global __PyImport_ExecCodeModuleWithPathnames_fp, __PyImport_ExecCodeModuleWithPathnames_f, __PyImport_ExecCodeModuleWithPathnames_tf
    __PyImport_ExecCodeModuleWithPathnames_f = getattr(libpy, "PyImport_ExecCodeModuleWithPathnames")
    __PyImport_ExecCodeModuleWithPathnames_f.restype = ctypes.c_void_p
    __PyImport_ExecCodeModuleWithPathnames_f.argtypes = [ctypes.c_char_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
    __PyImport_ExecCodeModuleWithPathnames_tf.tfname = "$PyImport_ExecCodeModuleWithPathnames".encode()
    __PyImport_ExecCodeModuleWithPathnames_tf.type = vpiSysFunc
    __PyImport_ExecCodeModuleWithPathnames_fp = tf_func_t(__PyImport_ExecCodeModuleWithPathnames)
    __PyImport_ExecCodeModuleWithPathnames_tf.calltf = __PyImport_ExecCodeModuleWithPathnames_fp
    __PyImport_ExecCodeModuleWithPathnames_tf.sizetf = sizetf64_fp
    __PyImport_ExecCodeModuleWithPathnames_tf.userdata = None
    name = __PyImport_ExecCodeModuleWithPathnames_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ExecCodeModuleWithPathnames_tf))

    global __PyImport_GetImporter_fp, __PyImport_GetImporter_f, __PyImport_GetImporter_tf
    __PyImport_GetImporter_f = getattr(libpy, "PyImport_GetImporter")
    __PyImport_GetImporter_f.restype = ctypes.c_void_p
    __PyImport_GetImporter_f.argtypes = [ctypes.c_void_p]
    __PyImport_GetImporter_tf.tfname = "$PyImport_GetImporter".encode()
    __PyImport_GetImporter_tf.type = vpiSysFunc
    __PyImport_GetImporter_fp = tf_func_t(__PyImport_GetImporter)
    __PyImport_GetImporter_tf.calltf = __PyImport_GetImporter_fp
    __PyImport_GetImporter_tf.sizetf = sizetf64_fp
    __PyImport_GetImporter_tf.userdata = None
    name = __PyImport_GetImporter_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_GetImporter_tf))

    global __PyImport_GetMagicNumber_fp, __PyImport_GetMagicNumber_f, __PyImport_GetMagicNumber_tf
    __PyImport_GetMagicNumber_f = getattr(libpy, "PyImport_GetMagicNumber")
    __PyImport_GetMagicNumber_f.restype = ctypes.c_int
    __PyImport_GetMagicNumber_f.argtypes = []
    __PyImport_GetMagicNumber_tf.tfname = "$PyImport_GetMagicNumber".encode()
    __PyImport_GetMagicNumber_tf.type = vpiSysFunc
    __PyImport_GetMagicNumber_fp = tf_func_t(__PyImport_GetMagicNumber)
    __PyImport_GetMagicNumber_tf.calltf = __PyImport_GetMagicNumber_fp
    __PyImport_GetMagicNumber_tf.userdata = None
    name = __PyImport_GetMagicNumber_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_GetMagicNumber_tf))

    global __PyImport_GetMagicTag_fp, __PyImport_GetMagicTag_f, __PyImport_GetMagicTag_tf
    __PyImport_GetMagicTag_f = getattr(libpy, "PyImport_GetMagicTag")
    __PyImport_GetMagicTag_f.restype = ctypes.c_char_p
    __PyImport_GetMagicTag_f.argtypes = []
    __PyImport_GetMagicTag_tf.tfname = "$PyImport_GetMagicTag".encode()
    __PyImport_GetMagicTag_tf.type = vpiSysTask
    __PyImport_GetMagicTag_fp = tf_func_t(__PyImport_GetMagicTag)
    __PyImport_GetMagicTag_tf.calltf = __PyImport_GetMagicTag_fp
    __PyImport_GetMagicTag_tf.userdata = None
    name = __PyImport_GetMagicTag_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_GetMagicTag_tf))

    global __PyImport_GetModule_fp, __PyImport_GetModule_f, __PyImport_GetModule_tf
    __PyImport_GetModule_f = getattr(libpy, "PyImport_GetModule")
    __PyImport_GetModule_f.restype = ctypes.c_void_p
    __PyImport_GetModule_f.argtypes = [ctypes.c_void_p]
    __PyImport_GetModule_tf.tfname = "$PyImport_GetModule".encode()
    __PyImport_GetModule_tf.type = vpiSysFunc
    __PyImport_GetModule_fp = tf_func_t(__PyImport_GetModule)
    __PyImport_GetModule_tf.calltf = __PyImport_GetModule_fp
    __PyImport_GetModule_tf.sizetf = sizetf64_fp
    __PyImport_GetModule_tf.userdata = None
    name = __PyImport_GetModule_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_GetModule_tf))

    global __PyImport_GetModuleDict_fp, __PyImport_GetModuleDict_f, __PyImport_GetModuleDict_tf
    __PyImport_GetModuleDict_f = getattr(libpy, "PyImport_GetModuleDict")
    __PyImport_GetModuleDict_f.restype = ctypes.c_void_p
    __PyImport_GetModuleDict_f.argtypes = []
    __PyImport_GetModuleDict_tf.tfname = "$PyImport_GetModuleDict".encode()
    __PyImport_GetModuleDict_tf.type = vpiSysFunc
    __PyImport_GetModuleDict_fp = tf_func_t(__PyImport_GetModuleDict)
    __PyImport_GetModuleDict_tf.calltf = __PyImport_GetModuleDict_fp
    __PyImport_GetModuleDict_tf.sizetf = sizetf64_fp
    __PyImport_GetModuleDict_tf.userdata = None
    name = __PyImport_GetModuleDict_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_GetModuleDict_tf))

    global __PyImport_Import_fp, __PyImport_Import_f, __PyImport_Import_tf
    __PyImport_Import_f = getattr(libpy, "PyImport_Import")
    __PyImport_Import_f.restype = ctypes.c_void_p
    __PyImport_Import_f.argtypes = [ctypes.c_void_p]
    __PyImport_Import_tf.tfname = "$PyImport_Import".encode()
    __PyImport_Import_tf.type = vpiSysFunc
    __PyImport_Import_fp = tf_func_t(__PyImport_Import)
    __PyImport_Import_tf.calltf = __PyImport_Import_fp
    __PyImport_Import_tf.sizetf = sizetf64_fp
    __PyImport_Import_tf.userdata = None
    name = __PyImport_Import_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_Import_tf))

    global __PyImport_ImportFrozenModule_fp, __PyImport_ImportFrozenModule_f, __PyImport_ImportFrozenModule_tf
    __PyImport_ImportFrozenModule_f = getattr(libpy, "PyImport_ImportFrozenModule")
    __PyImport_ImportFrozenModule_f.restype = ctypes.c_int
    __PyImport_ImportFrozenModule_f.argtypes = [ctypes.c_char_p]
    __PyImport_ImportFrozenModule_tf.tfname = "$PyImport_ImportFrozenModule".encode()
    __PyImport_ImportFrozenModule_tf.type = vpiSysFunc
    __PyImport_ImportFrozenModule_fp = tf_func_t(__PyImport_ImportFrozenModule)
    __PyImport_ImportFrozenModule_tf.calltf = __PyImport_ImportFrozenModule_fp
    __PyImport_ImportFrozenModule_tf.userdata = None
    name = __PyImport_ImportFrozenModule_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ImportFrozenModule_tf))

    global __PyImport_ImportFrozenModuleObject_fp, __PyImport_ImportFrozenModuleObject_f, __PyImport_ImportFrozenModuleObject_tf
    __PyImport_ImportFrozenModuleObject_f = getattr(libpy, "PyImport_ImportFrozenModuleObject")
    __PyImport_ImportFrozenModuleObject_f.restype = ctypes.c_int
    __PyImport_ImportFrozenModuleObject_f.argtypes = [ctypes.c_void_p]
    __PyImport_ImportFrozenModuleObject_tf.tfname = "$PyImport_ImportFrozenModuleObject".encode()
    __PyImport_ImportFrozenModuleObject_tf.type = vpiSysFunc
    __PyImport_ImportFrozenModuleObject_fp = tf_func_t(__PyImport_ImportFrozenModuleObject)
    __PyImport_ImportFrozenModuleObject_tf.calltf = __PyImport_ImportFrozenModuleObject_fp
    __PyImport_ImportFrozenModuleObject_tf.userdata = None
    name = __PyImport_ImportFrozenModuleObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ImportFrozenModuleObject_tf))

    global __PyImport_ImportModule_fp, __PyImport_ImportModule_f, __PyImport_ImportModule_tf
    __PyImport_ImportModule_f = getattr(libpy, "PyImport_ImportModule")
    __PyImport_ImportModule_f.restype = ctypes.c_void_p
    __PyImport_ImportModule_f.argtypes = [ctypes.c_char_p]
    __PyImport_ImportModule_tf.tfname = "$PyImport_ImportModule".encode()
    __PyImport_ImportModule_tf.type = vpiSysFunc
    __PyImport_ImportModule_fp = tf_func_t(__PyImport_ImportModule)
    __PyImport_ImportModule_tf.calltf = __PyImport_ImportModule_fp
    __PyImport_ImportModule_tf.sizetf = sizetf64_fp
    __PyImport_ImportModule_tf.userdata = None
    name = __PyImport_ImportModule_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ImportModule_tf))

    global __PyImport_ImportModuleLevel_fp, __PyImport_ImportModuleLevel_f, __PyImport_ImportModuleLevel_tf
    __PyImport_ImportModuleLevel_f = getattr(libpy, "PyImport_ImportModuleLevel")
    __PyImport_ImportModuleLevel_f.restype = ctypes.c_void_p
    __PyImport_ImportModuleLevel_f.argtypes = [ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
    __PyImport_ImportModuleLevel_tf.tfname = "$PyImport_ImportModuleLevel".encode()
    __PyImport_ImportModuleLevel_tf.type = vpiSysFunc
    __PyImport_ImportModuleLevel_fp = tf_func_t(__PyImport_ImportModuleLevel)
    __PyImport_ImportModuleLevel_tf.calltf = __PyImport_ImportModuleLevel_fp
    __PyImport_ImportModuleLevel_tf.sizetf = sizetf64_fp
    __PyImport_ImportModuleLevel_tf.userdata = None
    name = __PyImport_ImportModuleLevel_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ImportModuleLevel_tf))

    global __PyImport_ImportModuleLevelObject_fp, __PyImport_ImportModuleLevelObject_f, __PyImport_ImportModuleLevelObject_tf
    __PyImport_ImportModuleLevelObject_f = getattr(libpy, "PyImport_ImportModuleLevelObject")
    __PyImport_ImportModuleLevelObject_f.restype = ctypes.c_void_p
    __PyImport_ImportModuleLevelObject_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
    __PyImport_ImportModuleLevelObject_tf.tfname = "$PyImport_ImportModuleLevelObject".encode()
    __PyImport_ImportModuleLevelObject_tf.type = vpiSysFunc
    __PyImport_ImportModuleLevelObject_fp = tf_func_t(__PyImport_ImportModuleLevelObject)
    __PyImport_ImportModuleLevelObject_tf.calltf = __PyImport_ImportModuleLevelObject_fp
    __PyImport_ImportModuleLevelObject_tf.sizetf = sizetf64_fp
    __PyImport_ImportModuleLevelObject_tf.userdata = None
    name = __PyImport_ImportModuleLevelObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ImportModuleLevelObject_tf))

    global __PyImport_ImportModuleNoBlock_fp, __PyImport_ImportModuleNoBlock_f, __PyImport_ImportModuleNoBlock_tf
    __PyImport_ImportModuleNoBlock_f = getattr(libpy, "PyImport_ImportModuleNoBlock")
    __PyImport_ImportModuleNoBlock_f.restype = ctypes.c_void_p
    __PyImport_ImportModuleNoBlock_f.argtypes = [ctypes.c_char_p]
    __PyImport_ImportModuleNoBlock_tf.tfname = "$PyImport_ImportModuleNoBlock".encode()
    __PyImport_ImportModuleNoBlock_tf.type = vpiSysFunc
    __PyImport_ImportModuleNoBlock_fp = tf_func_t(__PyImport_ImportModuleNoBlock)
    __PyImport_ImportModuleNoBlock_tf.calltf = __PyImport_ImportModuleNoBlock_fp
    __PyImport_ImportModuleNoBlock_tf.sizetf = sizetf64_fp
    __PyImport_ImportModuleNoBlock_tf.userdata = None
    name = __PyImport_ImportModuleNoBlock_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ImportModuleNoBlock_tf))

    global __PyImport_ReloadModule_fp, __PyImport_ReloadModule_f, __PyImport_ReloadModule_tf
    __PyImport_ReloadModule_f = getattr(libpy, "PyImport_ReloadModule")
    __PyImport_ReloadModule_f.restype = ctypes.c_void_p
    __PyImport_ReloadModule_f.argtypes = [ctypes.c_void_p]
    __PyImport_ReloadModule_tf.tfname = "$PyImport_ReloadModule".encode()
    __PyImport_ReloadModule_tf.type = vpiSysFunc
    __PyImport_ReloadModule_fp = tf_func_t(__PyImport_ReloadModule)
    __PyImport_ReloadModule_tf.calltf = __PyImport_ReloadModule_fp
    __PyImport_ReloadModule_tf.sizetf = sizetf64_fp
    __PyImport_ReloadModule_tf.userdata = None
    name = __PyImport_ReloadModule_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyImport_ReloadModule_tf))

    global __PyLong_AsDouble_fp, __PyLong_AsDouble_f, __PyLong_AsDouble_tf
    __PyLong_AsDouble_f = getattr(libpy, "PyLong_AsDouble")
    __PyLong_AsDouble_f.restype = ctypes.c_double
    __PyLong_AsDouble_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsDouble_tf.tfname = "$PyLong_AsDouble".encode()
    __PyLong_AsDouble_tf.type = vpiSysFunc
    __PyLong_AsDouble_fp = tf_func_t(__PyLong_AsDouble)
    __PyLong_AsDouble_tf.calltf = __PyLong_AsDouble_fp
    __PyLong_AsDouble_tf.sizetf = sizetf64_fp
    __PyLong_AsDouble_tf.userdata = None
    name = __PyLong_AsDouble_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsDouble_tf))

    global __PyLong_AsLong_fp, __PyLong_AsLong_f, __PyLong_AsLong_tf
    __PyLong_AsLong_f = getattr(libpy, "PyLong_AsLong")
    __PyLong_AsLong_f.restype = ctypes.c_int
    __PyLong_AsLong_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsLong_tf.tfname = "$PyLong_AsLong".encode()
    __PyLong_AsLong_tf.type = vpiSysFunc
    __PyLong_AsLong_fp = tf_func_t(__PyLong_AsLong)
    __PyLong_AsLong_tf.calltf = __PyLong_AsLong_fp
    __PyLong_AsLong_tf.userdata = None
    name = __PyLong_AsLong_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsLong_tf))

    global __PyLong_AsLongAndOverflow_fp, __PyLong_AsLongAndOverflow_f, __PyLong_AsLongAndOverflow_tf
    __PyLong_AsLongAndOverflow_f = getattr(libpy, "PyLong_AsLongAndOverflow")
    __PyLong_AsLongAndOverflow_f.restype = ctypes.c_int
    __PyLong_AsLongAndOverflow_f.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]
    __PyLong_AsLongAndOverflow_tf.tfname = "$PyLong_AsLongAndOverflow".encode()
    __PyLong_AsLongAndOverflow_tf.type = vpiSysFunc
    __PyLong_AsLongAndOverflow_fp = tf_func_t(__PyLong_AsLongAndOverflow)
    __PyLong_AsLongAndOverflow_tf.calltf = __PyLong_AsLongAndOverflow_fp
    __PyLong_AsLongAndOverflow_tf.userdata = None
    name = __PyLong_AsLongAndOverflow_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsLongAndOverflow_tf))

    global __PyLong_AsLongLong_fp, __PyLong_AsLongLong_f, __PyLong_AsLongLong_tf
    __PyLong_AsLongLong_f = getattr(libpy, "PyLong_AsLongLong")
    __PyLong_AsLongLong_f.restype = ctypes.c_longlong
    __PyLong_AsLongLong_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsLongLong_tf.tfname = "$PyLong_AsLongLong".encode()
    __PyLong_AsLongLong_tf.type = vpiSysFunc
    __PyLong_AsLongLong_fp = tf_func_t(__PyLong_AsLongLong)
    __PyLong_AsLongLong_tf.calltf = __PyLong_AsLongLong_fp
    __PyLong_AsLongLong_tf.sizetf = sizetf64_fp
    __PyLong_AsLongLong_tf.userdata = None
    name = __PyLong_AsLongLong_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsLongLong_tf))

    global __PyLong_AsLongLongAndOverflow_fp, __PyLong_AsLongLongAndOverflow_f, __PyLong_AsLongLongAndOverflow_tf
    __PyLong_AsLongLongAndOverflow_f = getattr(libpy, "PyLong_AsLongLongAndOverflow")
    __PyLong_AsLongLongAndOverflow_f.restype = ctypes.c_longlong
    __PyLong_AsLongLongAndOverflow_f.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]
    __PyLong_AsLongLongAndOverflow_tf.tfname = "$PyLong_AsLongLongAndOverflow".encode()
    __PyLong_AsLongLongAndOverflow_tf.type = vpiSysFunc
    __PyLong_AsLongLongAndOverflow_fp = tf_func_t(__PyLong_AsLongLongAndOverflow)
    __PyLong_AsLongLongAndOverflow_tf.calltf = __PyLong_AsLongLongAndOverflow_fp
    __PyLong_AsLongLongAndOverflow_tf.sizetf = sizetf64_fp
    __PyLong_AsLongLongAndOverflow_tf.userdata = None
    name = __PyLong_AsLongLongAndOverflow_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsLongLongAndOverflow_tf))

    global __PyLong_AsSize_t_fp, __PyLong_AsSize_t_f, __PyLong_AsSize_t_tf
    __PyLong_AsSize_t_f = getattr(libpy, "PyLong_AsSize_t")
    __PyLong_AsSize_t_f.restype = ctypes.c_uint
    __PyLong_AsSize_t_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsSize_t_tf.tfname = "$PyLong_AsSize_t".encode()
    __PyLong_AsSize_t_tf.type = vpiSysFunc
    __PyLong_AsSize_t_fp = tf_func_t(__PyLong_AsSize_t)
    __PyLong_AsSize_t_tf.calltf = __PyLong_AsSize_t_fp
    __PyLong_AsSize_t_tf.userdata = None
    name = __PyLong_AsSize_t_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsSize_t_tf))

    global __PyLong_AsSsize_t_fp, __PyLong_AsSsize_t_f, __PyLong_AsSsize_t_tf
    __PyLong_AsSsize_t_f = getattr(libpy, "PyLong_AsSsize_t")
    __PyLong_AsSsize_t_f.restype = ctypes.c_uint
    __PyLong_AsSsize_t_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsSsize_t_tf.tfname = "$PyLong_AsSsize_t".encode()
    __PyLong_AsSsize_t_tf.type = vpiSysFunc
    __PyLong_AsSsize_t_fp = tf_func_t(__PyLong_AsSsize_t)
    __PyLong_AsSsize_t_tf.calltf = __PyLong_AsSsize_t_fp
    __PyLong_AsSsize_t_tf.userdata = None
    name = __PyLong_AsSsize_t_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsSsize_t_tf))

    global __PyLong_AsUnsignedLong_fp, __PyLong_AsUnsignedLong_f, __PyLong_AsUnsignedLong_tf
    __PyLong_AsUnsignedLong_f = getattr(libpy, "PyLong_AsUnsignedLong")
    __PyLong_AsUnsignedLong_f.restype = ctypes.c_uint
    __PyLong_AsUnsignedLong_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsUnsignedLong_tf.tfname = "$PyLong_AsUnsignedLong".encode()
    __PyLong_AsUnsignedLong_tf.type = vpiSysFunc
    __PyLong_AsUnsignedLong_fp = tf_func_t(__PyLong_AsUnsignedLong)
    __PyLong_AsUnsignedLong_tf.calltf = __PyLong_AsUnsignedLong_fp
    __PyLong_AsUnsignedLong_tf.userdata = None
    name = __PyLong_AsUnsignedLong_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsUnsignedLong_tf))

    global __PyLong_AsUnsignedLongLong_fp, __PyLong_AsUnsignedLongLong_f, __PyLong_AsUnsignedLongLong_tf
    __PyLong_AsUnsignedLongLong_f = getattr(libpy, "PyLong_AsUnsignedLongLong")
    __PyLong_AsUnsignedLongLong_f.restype = ctypes.c_ulonglong
    __PyLong_AsUnsignedLongLong_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsUnsignedLongLong_tf.tfname = "$PyLong_AsUnsignedLongLong".encode()
    __PyLong_AsUnsignedLongLong_tf.type = vpiSysFunc
    __PyLong_AsUnsignedLongLong_fp = tf_func_t(__PyLong_AsUnsignedLongLong)
    __PyLong_AsUnsignedLongLong_tf.calltf = __PyLong_AsUnsignedLongLong_fp
    __PyLong_AsUnsignedLongLong_tf.sizetf = sizetf64_fp
    __PyLong_AsUnsignedLongLong_tf.userdata = None
    name = __PyLong_AsUnsignedLongLong_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsUnsignedLongLong_tf))

    global __PyLong_AsUnsignedLongLongMask_fp, __PyLong_AsUnsignedLongLongMask_f, __PyLong_AsUnsignedLongLongMask_tf
    __PyLong_AsUnsignedLongLongMask_f = getattr(libpy, "PyLong_AsUnsignedLongLongMask")
    __PyLong_AsUnsignedLongLongMask_f.restype = ctypes.c_ulonglong
    __PyLong_AsUnsignedLongLongMask_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsUnsignedLongLongMask_tf.tfname = "$PyLong_AsUnsignedLongLongMask".encode()
    __PyLong_AsUnsignedLongLongMask_tf.type = vpiSysFunc
    __PyLong_AsUnsignedLongLongMask_fp = tf_func_t(__PyLong_AsUnsignedLongLongMask)
    __PyLong_AsUnsignedLongLongMask_tf.calltf = __PyLong_AsUnsignedLongLongMask_fp
    __PyLong_AsUnsignedLongLongMask_tf.sizetf = sizetf64_fp
    __PyLong_AsUnsignedLongLongMask_tf.userdata = None
    name = __PyLong_AsUnsignedLongLongMask_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsUnsignedLongLongMask_tf))

    global __PyLong_AsUnsignedLongMask_fp, __PyLong_AsUnsignedLongMask_f, __PyLong_AsUnsignedLongMask_tf
    __PyLong_AsUnsignedLongMask_f = getattr(libpy, "PyLong_AsUnsignedLongMask")
    __PyLong_AsUnsignedLongMask_f.restype = ctypes.c_uint
    __PyLong_AsUnsignedLongMask_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsUnsignedLongMask_tf.tfname = "$PyLong_AsUnsignedLongMask".encode()
    __PyLong_AsUnsignedLongMask_tf.type = vpiSysFunc
    __PyLong_AsUnsignedLongMask_fp = tf_func_t(__PyLong_AsUnsignedLongMask)
    __PyLong_AsUnsignedLongMask_tf.calltf = __PyLong_AsUnsignedLongMask_fp
    __PyLong_AsUnsignedLongMask_tf.userdata = None
    name = __PyLong_AsUnsignedLongMask_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsUnsignedLongMask_tf))

    global __PyLong_AsVoidPtr_fp, __PyLong_AsVoidPtr_f, __PyLong_AsVoidPtr_tf
    __PyLong_AsVoidPtr_f = getattr(libpy, "PyLong_AsVoidPtr")
    __PyLong_AsVoidPtr_f.restype = ctypes.c_void_p
    __PyLong_AsVoidPtr_f.argtypes = [ctypes.c_void_p]
    __PyLong_AsVoidPtr_tf.tfname = "$PyLong_AsVoidPtr".encode()
    __PyLong_AsVoidPtr_tf.type = vpiSysFunc
    __PyLong_AsVoidPtr_fp = tf_func_t(__PyLong_AsVoidPtr)
    __PyLong_AsVoidPtr_tf.calltf = __PyLong_AsVoidPtr_fp
    __PyLong_AsVoidPtr_tf.sizetf = sizetf64_fp
    __PyLong_AsVoidPtr_tf.userdata = None
    name = __PyLong_AsVoidPtr_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_AsVoidPtr_tf))

    global __PyLong_FromDouble_fp, __PyLong_FromDouble_f, __PyLong_FromDouble_tf
    __PyLong_FromDouble_f = getattr(libpy, "PyLong_FromDouble")
    __PyLong_FromDouble_f.restype = ctypes.c_void_p
    __PyLong_FromDouble_f.argtypes = [ctypes.c_double]
    __PyLong_FromDouble_tf.tfname = "$PyLong_FromDouble".encode()
    __PyLong_FromDouble_tf.type = vpiSysFunc
    __PyLong_FromDouble_fp = tf_func_t(__PyLong_FromDouble)
    __PyLong_FromDouble_tf.calltf = __PyLong_FromDouble_fp
    __PyLong_FromDouble_tf.sizetf = sizetf64_fp
    __PyLong_FromDouble_tf.userdata = None
    name = __PyLong_FromDouble_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromDouble_tf))

    global __PyLong_FromLong_fp, __PyLong_FromLong_f, __PyLong_FromLong_tf
    __PyLong_FromLong_f = getattr(libpy, "PyLong_FromLong")
    __PyLong_FromLong_f.restype = ctypes.c_void_p
    __PyLong_FromLong_f.argtypes = [ctypes.c_int]
    __PyLong_FromLong_tf.tfname = "$PyLong_FromLong".encode()
    __PyLong_FromLong_tf.type = vpiSysFunc
    __PyLong_FromLong_fp = tf_func_t(__PyLong_FromLong)
    __PyLong_FromLong_tf.calltf = __PyLong_FromLong_fp
    __PyLong_FromLong_tf.sizetf = sizetf64_fp
    __PyLong_FromLong_tf.userdata = None
    name = __PyLong_FromLong_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromLong_tf))

    global __PyLong_FromLongLong_fp, __PyLong_FromLongLong_f, __PyLong_FromLongLong_tf
    __PyLong_FromLongLong_f = getattr(libpy, "PyLong_FromLongLong")
    __PyLong_FromLongLong_f.restype = ctypes.c_void_p
    __PyLong_FromLongLong_f.argtypes = [ctypes.c_longlong]
    __PyLong_FromLongLong_tf.tfname = "$PyLong_FromLongLong".encode()
    __PyLong_FromLongLong_tf.type = vpiSysFunc
    __PyLong_FromLongLong_fp = tf_func_t(__PyLong_FromLongLong)
    __PyLong_FromLongLong_tf.calltf = __PyLong_FromLongLong_fp
    __PyLong_FromLongLong_tf.sizetf = sizetf64_fp
    __PyLong_FromLongLong_tf.userdata = None
    name = __PyLong_FromLongLong_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromLongLong_tf))

    global __PyLong_FromSize_t_fp, __PyLong_FromSize_t_f, __PyLong_FromSize_t_tf
    __PyLong_FromSize_t_f = getattr(libpy, "PyLong_FromSize_t")
    __PyLong_FromSize_t_f.restype = ctypes.c_void_p
    __PyLong_FromSize_t_f.argtypes = [ctypes.c_uint]
    __PyLong_FromSize_t_tf.tfname = "$PyLong_FromSize_t".encode()
    __PyLong_FromSize_t_tf.type = vpiSysFunc
    __PyLong_FromSize_t_fp = tf_func_t(__PyLong_FromSize_t)
    __PyLong_FromSize_t_tf.calltf = __PyLong_FromSize_t_fp
    __PyLong_FromSize_t_tf.sizetf = sizetf64_fp
    __PyLong_FromSize_t_tf.userdata = None
    name = __PyLong_FromSize_t_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromSize_t_tf))

    global __PyLong_FromSsize_t_fp, __PyLong_FromSsize_t_f, __PyLong_FromSsize_t_tf
    __PyLong_FromSsize_t_f = getattr(libpy, "PyLong_FromSsize_t")
    __PyLong_FromSsize_t_f.restype = ctypes.c_void_p
    __PyLong_FromSsize_t_f.argtypes = [ctypes.c_uint]
    __PyLong_FromSsize_t_tf.tfname = "$PyLong_FromSsize_t".encode()
    __PyLong_FromSsize_t_tf.type = vpiSysFunc
    __PyLong_FromSsize_t_fp = tf_func_t(__PyLong_FromSsize_t)
    __PyLong_FromSsize_t_tf.calltf = __PyLong_FromSsize_t_fp
    __PyLong_FromSsize_t_tf.sizetf = sizetf64_fp
    __PyLong_FromSsize_t_tf.userdata = None
    name = __PyLong_FromSsize_t_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromSsize_t_tf))

    global __PyLong_FromString_fp, __PyLong_FromString_f, __PyLong_FromString_tf
    __PyLong_FromString_f = getattr(libpy, "PyLong_FromString")
    __PyLong_FromString_f.restype = ctypes.c_void_p
    __PyLong_FromString_f.argtypes = [ctypes.c_char_p,ctypes.POINTER(ctypes.c_char_p),ctypes.c_int]
    __PyLong_FromString_tf.tfname = "$PyLong_FromString".encode()
    __PyLong_FromString_tf.type = vpiSysFunc
    __PyLong_FromString_fp = tf_func_t(__PyLong_FromString)
    __PyLong_FromString_tf.calltf = __PyLong_FromString_fp
    __PyLong_FromString_tf.sizetf = sizetf64_fp
    __PyLong_FromString_tf.userdata = None
    name = __PyLong_FromString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromString_tf))

    global __PyLong_FromUnicodeObject_fp, __PyLong_FromUnicodeObject_f, __PyLong_FromUnicodeObject_tf
    __PyLong_FromUnicodeObject_f = getattr(libpy, "PyLong_FromUnicodeObject")
    __PyLong_FromUnicodeObject_f.restype = ctypes.c_void_p
    __PyLong_FromUnicodeObject_f.argtypes = [ctypes.c_void_p,ctypes.c_int]
    __PyLong_FromUnicodeObject_tf.tfname = "$PyLong_FromUnicodeObject".encode()
    __PyLong_FromUnicodeObject_tf.type = vpiSysFunc
    __PyLong_FromUnicodeObject_fp = tf_func_t(__PyLong_FromUnicodeObject)
    __PyLong_FromUnicodeObject_tf.calltf = __PyLong_FromUnicodeObject_fp
    __PyLong_FromUnicodeObject_tf.sizetf = sizetf64_fp
    __PyLong_FromUnicodeObject_tf.userdata = None
    name = __PyLong_FromUnicodeObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromUnicodeObject_tf))

    global __PyLong_FromUnsignedLong_fp, __PyLong_FromUnsignedLong_f, __PyLong_FromUnsignedLong_tf
    __PyLong_FromUnsignedLong_f = getattr(libpy, "PyLong_FromUnsignedLong")
    __PyLong_FromUnsignedLong_f.restype = ctypes.c_void_p
    __PyLong_FromUnsignedLong_f.argtypes = [ctypes.c_uint]
    __PyLong_FromUnsignedLong_tf.tfname = "$PyLong_FromUnsignedLong".encode()
    __PyLong_FromUnsignedLong_tf.type = vpiSysFunc
    __PyLong_FromUnsignedLong_fp = tf_func_t(__PyLong_FromUnsignedLong)
    __PyLong_FromUnsignedLong_tf.calltf = __PyLong_FromUnsignedLong_fp
    __PyLong_FromUnsignedLong_tf.sizetf = sizetf64_fp
    __PyLong_FromUnsignedLong_tf.userdata = None
    name = __PyLong_FromUnsignedLong_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromUnsignedLong_tf))

    global __PyLong_FromUnsignedLongLong_fp, __PyLong_FromUnsignedLongLong_f, __PyLong_FromUnsignedLongLong_tf
    __PyLong_FromUnsignedLongLong_f = getattr(libpy, "PyLong_FromUnsignedLongLong")
    __PyLong_FromUnsignedLongLong_f.restype = ctypes.c_void_p
    __PyLong_FromUnsignedLongLong_f.argtypes = [ctypes.c_ulonglong]
    __PyLong_FromUnsignedLongLong_tf.tfname = "$PyLong_FromUnsignedLongLong".encode()
    __PyLong_FromUnsignedLongLong_tf.type = vpiSysFunc
    __PyLong_FromUnsignedLongLong_fp = tf_func_t(__PyLong_FromUnsignedLongLong)
    __PyLong_FromUnsignedLongLong_tf.calltf = __PyLong_FromUnsignedLongLong_fp
    __PyLong_FromUnsignedLongLong_tf.sizetf = sizetf64_fp
    __PyLong_FromUnsignedLongLong_tf.userdata = None
    name = __PyLong_FromUnsignedLongLong_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromUnsignedLongLong_tf))

    global __PyLong_FromVoidPtr_fp, __PyLong_FromVoidPtr_f, __PyLong_FromVoidPtr_tf
    __PyLong_FromVoidPtr_f = getattr(libpy, "PyLong_FromVoidPtr")
    __PyLong_FromVoidPtr_f.restype = ctypes.c_void_p
    __PyLong_FromVoidPtr_f.argtypes = [ctypes.c_void_p]
    __PyLong_FromVoidPtr_tf.tfname = "$PyLong_FromVoidPtr".encode()
    __PyLong_FromVoidPtr_tf.type = vpiSysFunc
    __PyLong_FromVoidPtr_fp = tf_func_t(__PyLong_FromVoidPtr)
    __PyLong_FromVoidPtr_tf.calltf = __PyLong_FromVoidPtr_fp
    __PyLong_FromVoidPtr_tf.sizetf = sizetf64_fp
    __PyLong_FromVoidPtr_tf.userdata = None
    name = __PyLong_FromVoidPtr_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_FromVoidPtr_tf))

    global __PyLong_GetInfo_fp, __PyLong_GetInfo_f, __PyLong_GetInfo_tf
    __PyLong_GetInfo_f = getattr(libpy, "PyLong_GetInfo")
    __PyLong_GetInfo_f.restype = ctypes.c_void_p
    __PyLong_GetInfo_f.argtypes = []
    __PyLong_GetInfo_tf.tfname = "$PyLong_GetInfo".encode()
    __PyLong_GetInfo_tf.type = vpiSysFunc
    __PyLong_GetInfo_fp = tf_func_t(__PyLong_GetInfo)
    __PyLong_GetInfo_tf.calltf = __PyLong_GetInfo_fp
    __PyLong_GetInfo_tf.sizetf = sizetf64_fp
    __PyLong_GetInfo_tf.userdata = None
    name = __PyLong_GetInfo_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyLong_GetInfo_tf))

    global __PyObject_ASCII_fp, __PyObject_ASCII_f, __PyObject_ASCII_tf
    __PyObject_ASCII_f = getattr(libpy, "PyObject_ASCII")
    __PyObject_ASCII_f.restype = ctypes.c_void_p
    __PyObject_ASCII_f.argtypes = [ctypes.c_void_p]
    __PyObject_ASCII_tf.tfname = "$PyObject_ASCII".encode()
    __PyObject_ASCII_tf.type = vpiSysFunc
    __PyObject_ASCII_fp = tf_func_t(__PyObject_ASCII)
    __PyObject_ASCII_tf.calltf = __PyObject_ASCII_fp
    __PyObject_ASCII_tf.sizetf = sizetf64_fp
    __PyObject_ASCII_tf.userdata = None
    name = __PyObject_ASCII_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_ASCII_tf))

    global __PyObject_AsFileDescriptor_fp, __PyObject_AsFileDescriptor_f, __PyObject_AsFileDescriptor_tf
    __PyObject_AsFileDescriptor_f = getattr(libpy, "PyObject_AsFileDescriptor")
    __PyObject_AsFileDescriptor_f.restype = ctypes.c_int
    __PyObject_AsFileDescriptor_f.argtypes = [ctypes.c_void_p]
    __PyObject_AsFileDescriptor_tf.tfname = "$PyObject_AsFileDescriptor".encode()
    __PyObject_AsFileDescriptor_tf.type = vpiSysFunc
    __PyObject_AsFileDescriptor_fp = tf_func_t(__PyObject_AsFileDescriptor)
    __PyObject_AsFileDescriptor_tf.calltf = __PyObject_AsFileDescriptor_fp
    __PyObject_AsFileDescriptor_tf.userdata = None
    name = __PyObject_AsFileDescriptor_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_AsFileDescriptor_tf))

    global __PyObject_Bytes_fp, __PyObject_Bytes_f, __PyObject_Bytes_tf
    __PyObject_Bytes_f = getattr(libpy, "PyObject_Bytes")
    __PyObject_Bytes_f.restype = ctypes.c_void_p
    __PyObject_Bytes_f.argtypes = [ctypes.c_void_p]
    __PyObject_Bytes_tf.tfname = "$PyObject_Bytes".encode()
    __PyObject_Bytes_tf.type = vpiSysFunc
    __PyObject_Bytes_fp = tf_func_t(__PyObject_Bytes)
    __PyObject_Bytes_tf.calltf = __PyObject_Bytes_fp
    __PyObject_Bytes_tf.sizetf = sizetf64_fp
    __PyObject_Bytes_tf.userdata = None
    name = __PyObject_Bytes_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Bytes_tf))

    global __PyObject_Call_fp, __PyObject_Call_f, __PyObject_Call_tf
    __PyObject_Call_f = getattr(libpy, "PyObject_Call")
    __PyObject_Call_f.restype = ctypes.c_void_p
    __PyObject_Call_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_Call_tf.tfname = "$PyObject_Call".encode()
    __PyObject_Call_tf.type = vpiSysFunc
    __PyObject_Call_fp = tf_func_t(__PyObject_Call)
    __PyObject_Call_tf.calltf = __PyObject_Call_fp
    __PyObject_Call_tf.sizetf = sizetf64_fp
    __PyObject_Call_tf.userdata = None
    name = __PyObject_Call_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Call_tf))

    global __PyObject_CallFinalizer_fp, __PyObject_CallFinalizer_f, __PyObject_CallFinalizer_tf
    __PyObject_CallFinalizer_f = getattr(libpy, "PyObject_CallFinalizer")
    __PyObject_CallFinalizer_f.restype = None
    __PyObject_CallFinalizer_f.argtypes = [ctypes.c_void_p]
    __PyObject_CallFinalizer_tf.tfname = "$PyObject_CallFinalizer".encode()
    __PyObject_CallFinalizer_tf.type = vpiSysTask
    __PyObject_CallFinalizer_fp = tf_func_t(__PyObject_CallFinalizer)
    __PyObject_CallFinalizer_tf.calltf = __PyObject_CallFinalizer_fp
    __PyObject_CallFinalizer_tf.userdata = None
    name = __PyObject_CallFinalizer_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_CallFinalizer_tf))

    global __PyObject_CallFinalizerFromDealloc_fp, __PyObject_CallFinalizerFromDealloc_f, __PyObject_CallFinalizerFromDealloc_tf
    __PyObject_CallFinalizerFromDealloc_f = getattr(libpy, "PyObject_CallFinalizerFromDealloc")
    __PyObject_CallFinalizerFromDealloc_f.restype = ctypes.c_int
    __PyObject_CallFinalizerFromDealloc_f.argtypes = [ctypes.c_void_p]
    __PyObject_CallFinalizerFromDealloc_tf.tfname = "$PyObject_CallFinalizerFromDealloc".encode()
    __PyObject_CallFinalizerFromDealloc_tf.type = vpiSysFunc
    __PyObject_CallFinalizerFromDealloc_fp = tf_func_t(__PyObject_CallFinalizerFromDealloc)
    __PyObject_CallFinalizerFromDealloc_tf.calltf = __PyObject_CallFinalizerFromDealloc_fp
    __PyObject_CallFinalizerFromDealloc_tf.userdata = None
    name = __PyObject_CallFinalizerFromDealloc_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_CallFinalizerFromDealloc_tf))

    global __PyObject_CallNoArgs_fp, __PyObject_CallNoArgs_f, __PyObject_CallNoArgs_tf
    __PyObject_CallNoArgs_f = getattr(libpy, "PyObject_CallNoArgs")
    __PyObject_CallNoArgs_f.restype = ctypes.c_void_p
    __PyObject_CallNoArgs_f.argtypes = [ctypes.c_void_p]
    __PyObject_CallNoArgs_tf.tfname = "$PyObject_CallNoArgs".encode()
    __PyObject_CallNoArgs_tf.type = vpiSysFunc
    __PyObject_CallNoArgs_fp = tf_func_t(__PyObject_CallNoArgs)
    __PyObject_CallNoArgs_tf.calltf = __PyObject_CallNoArgs_fp
    __PyObject_CallNoArgs_tf.sizetf = sizetf64_fp
    __PyObject_CallNoArgs_tf.userdata = None
    name = __PyObject_CallNoArgs_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_CallNoArgs_tf))

    global __PyObject_CallObject_fp, __PyObject_CallObject_f, __PyObject_CallObject_tf
    __PyObject_CallObject_f = getattr(libpy, "PyObject_CallObject")
    __PyObject_CallObject_f.restype = ctypes.c_void_p
    __PyObject_CallObject_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_CallObject_tf.tfname = "$PyObject_CallObject".encode()
    __PyObject_CallObject_tf.type = vpiSysFunc
    __PyObject_CallObject_fp = tf_func_t(__PyObject_CallObject)
    __PyObject_CallObject_tf.calltf = __PyObject_CallObject_fp
    __PyObject_CallObject_tf.sizetf = sizetf64_fp
    __PyObject_CallObject_tf.userdata = None
    name = __PyObject_CallObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_CallObject_tf))

    global __PyObject_Calloc_fp, __PyObject_Calloc_f, __PyObject_Calloc_tf
    __PyObject_Calloc_f = getattr(libpy, "PyObject_Calloc")
    __PyObject_Calloc_f.restype = ctypes.c_void_p
    __PyObject_Calloc_f.argtypes = [ctypes.c_uint,ctypes.c_uint]
    __PyObject_Calloc_tf.tfname = "$PyObject_Calloc".encode()
    __PyObject_Calloc_tf.type = vpiSysFunc
    __PyObject_Calloc_fp = tf_func_t(__PyObject_Calloc)
    __PyObject_Calloc_tf.calltf = __PyObject_Calloc_fp
    __PyObject_Calloc_tf.sizetf = sizetf64_fp
    __PyObject_Calloc_tf.userdata = None
    name = __PyObject_Calloc_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Calloc_tf))

    global __PyObject_CheckBuffer_fp, __PyObject_CheckBuffer_f, __PyObject_CheckBuffer_tf
    __PyObject_CheckBuffer_f = getattr(libpy, "PyObject_CheckBuffer")
    __PyObject_CheckBuffer_f.restype = ctypes.c_int
    __PyObject_CheckBuffer_f.argtypes = [ctypes.c_void_p]
    __PyObject_CheckBuffer_tf.tfname = "$PyObject_CheckBuffer".encode()
    __PyObject_CheckBuffer_tf.type = vpiSysFunc
    __PyObject_CheckBuffer_fp = tf_func_t(__PyObject_CheckBuffer)
    __PyObject_CheckBuffer_tf.calltf = __PyObject_CheckBuffer_fp
    __PyObject_CheckBuffer_tf.userdata = None
    name = __PyObject_CheckBuffer_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_CheckBuffer_tf))

    global __PyObject_ClearWeakRefs_fp, __PyObject_ClearWeakRefs_f, __PyObject_ClearWeakRefs_tf
    __PyObject_ClearWeakRefs_f = getattr(libpy, "PyObject_ClearWeakRefs")
    __PyObject_ClearWeakRefs_f.restype = None
    __PyObject_ClearWeakRefs_f.argtypes = [ctypes.c_void_p]
    __PyObject_ClearWeakRefs_tf.tfname = "$PyObject_ClearWeakRefs".encode()
    __PyObject_ClearWeakRefs_tf.type = vpiSysTask
    __PyObject_ClearWeakRefs_fp = tf_func_t(__PyObject_ClearWeakRefs)
    __PyObject_ClearWeakRefs_tf.calltf = __PyObject_ClearWeakRefs_fp
    __PyObject_ClearWeakRefs_tf.userdata = None
    name = __PyObject_ClearWeakRefs_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_ClearWeakRefs_tf))

    global __PyObject_CopyData_fp, __PyObject_CopyData_f, __PyObject_CopyData_tf
    __PyObject_CopyData_f = getattr(libpy, "PyObject_CopyData")
    __PyObject_CopyData_f.restype = ctypes.c_int
    __PyObject_CopyData_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_CopyData_tf.tfname = "$PyObject_CopyData".encode()
    __PyObject_CopyData_tf.type = vpiSysFunc
    __PyObject_CopyData_fp = tf_func_t(__PyObject_CopyData)
    __PyObject_CopyData_tf.calltf = __PyObject_CopyData_fp
    __PyObject_CopyData_tf.userdata = None
    name = __PyObject_CopyData_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_CopyData_tf))

    global __PyObject_DelItem_fp, __PyObject_DelItem_f, __PyObject_DelItem_tf
    __PyObject_DelItem_f = getattr(libpy, "PyObject_DelItem")
    __PyObject_DelItem_f.restype = ctypes.c_int
    __PyObject_DelItem_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_DelItem_tf.tfname = "$PyObject_DelItem".encode()
    __PyObject_DelItem_tf.type = vpiSysFunc
    __PyObject_DelItem_fp = tf_func_t(__PyObject_DelItem)
    __PyObject_DelItem_tf.calltf = __PyObject_DelItem_fp
    __PyObject_DelItem_tf.userdata = None
    name = __PyObject_DelItem_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_DelItem_tf))

    global __PyObject_DelItemString_fp, __PyObject_DelItemString_f, __PyObject_DelItemString_tf
    __PyObject_DelItemString_f = getattr(libpy, "PyObject_DelItemString")
    __PyObject_DelItemString_f.restype = ctypes.c_int
    __PyObject_DelItemString_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    __PyObject_DelItemString_tf.tfname = "$PyObject_DelItemString".encode()
    __PyObject_DelItemString_tf.type = vpiSysFunc
    __PyObject_DelItemString_fp = tf_func_t(__PyObject_DelItemString)
    __PyObject_DelItemString_tf.calltf = __PyObject_DelItemString_fp
    __PyObject_DelItemString_tf.userdata = None
    name = __PyObject_DelItemString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_DelItemString_tf))

    global __PyObject_Dir_fp, __PyObject_Dir_f, __PyObject_Dir_tf
    __PyObject_Dir_f = getattr(libpy, "PyObject_Dir")
    __PyObject_Dir_f.restype = ctypes.c_void_p
    __PyObject_Dir_f.argtypes = [ctypes.c_void_p]
    __PyObject_Dir_tf.tfname = "$PyObject_Dir".encode()
    __PyObject_Dir_tf.type = vpiSysFunc
    __PyObject_Dir_fp = tf_func_t(__PyObject_Dir)
    __PyObject_Dir_tf.calltf = __PyObject_Dir_fp
    __PyObject_Dir_tf.sizetf = sizetf64_fp
    __PyObject_Dir_tf.userdata = None
    name = __PyObject_Dir_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Dir_tf))

    global __PyObject_Format_fp, __PyObject_Format_f, __PyObject_Format_tf
    __PyObject_Format_f = getattr(libpy, "PyObject_Format")
    __PyObject_Format_f.restype = ctypes.c_void_p
    __PyObject_Format_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_Format_tf.tfname = "$PyObject_Format".encode()
    __PyObject_Format_tf.type = vpiSysFunc
    __PyObject_Format_fp = tf_func_t(__PyObject_Format)
    __PyObject_Format_tf.calltf = __PyObject_Format_fp
    __PyObject_Format_tf.sizetf = sizetf64_fp
    __PyObject_Format_tf.userdata = None
    name = __PyObject_Format_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Format_tf))

    global __PyObject_Free_fp, __PyObject_Free_f, __PyObject_Free_tf
    __PyObject_Free_f = getattr(libpy, "PyObject_Free")
    __PyObject_Free_f.restype = None
    __PyObject_Free_f.argtypes = [ctypes.c_void_p]
    __PyObject_Free_tf.tfname = "$PyObject_Free".encode()
    __PyObject_Free_tf.type = vpiSysTask
    __PyObject_Free_fp = tf_func_t(__PyObject_Free)
    __PyObject_Free_tf.calltf = __PyObject_Free_fp
    __PyObject_Free_tf.userdata = None
    name = __PyObject_Free_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Free_tf))

    global __PyObject_GC_Del_fp, __PyObject_GC_Del_f, __PyObject_GC_Del_tf
    __PyObject_GC_Del_f = getattr(libpy, "PyObject_GC_Del")
    __PyObject_GC_Del_f.restype = None
    __PyObject_GC_Del_f.argtypes = [ctypes.c_void_p]
    __PyObject_GC_Del_tf.tfname = "$PyObject_GC_Del".encode()
    __PyObject_GC_Del_tf.type = vpiSysTask
    __PyObject_GC_Del_fp = tf_func_t(__PyObject_GC_Del)
    __PyObject_GC_Del_tf.calltf = __PyObject_GC_Del_fp
    __PyObject_GC_Del_tf.userdata = None
    name = __PyObject_GC_Del_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GC_Del_tf))

    global __PyObject_GC_IsFinalized_fp, __PyObject_GC_IsFinalized_f, __PyObject_GC_IsFinalized_tf
    __PyObject_GC_IsFinalized_f = getattr(libpy, "PyObject_GC_IsFinalized")
    __PyObject_GC_IsFinalized_f.restype = ctypes.c_int
    __PyObject_GC_IsFinalized_f.argtypes = [ctypes.c_void_p]
    __PyObject_GC_IsFinalized_tf.tfname = "$PyObject_GC_IsFinalized".encode()
    __PyObject_GC_IsFinalized_tf.type = vpiSysFunc
    __PyObject_GC_IsFinalized_fp = tf_func_t(__PyObject_GC_IsFinalized)
    __PyObject_GC_IsFinalized_tf.calltf = __PyObject_GC_IsFinalized_fp
    __PyObject_GC_IsFinalized_tf.userdata = None
    name = __PyObject_GC_IsFinalized_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GC_IsFinalized_tf))

    global __PyObject_GC_IsTracked_fp, __PyObject_GC_IsTracked_f, __PyObject_GC_IsTracked_tf
    __PyObject_GC_IsTracked_f = getattr(libpy, "PyObject_GC_IsTracked")
    __PyObject_GC_IsTracked_f.restype = ctypes.c_int
    __PyObject_GC_IsTracked_f.argtypes = [ctypes.c_void_p]
    __PyObject_GC_IsTracked_tf.tfname = "$PyObject_GC_IsTracked".encode()
    __PyObject_GC_IsTracked_tf.type = vpiSysFunc
    __PyObject_GC_IsTracked_fp = tf_func_t(__PyObject_GC_IsTracked)
    __PyObject_GC_IsTracked_tf.calltf = __PyObject_GC_IsTracked_fp
    __PyObject_GC_IsTracked_tf.userdata = None
    name = __PyObject_GC_IsTracked_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GC_IsTracked_tf))

    global __PyObject_GC_Track_fp, __PyObject_GC_Track_f, __PyObject_GC_Track_tf
    __PyObject_GC_Track_f = getattr(libpy, "PyObject_GC_Track")
    __PyObject_GC_Track_f.restype = None
    __PyObject_GC_Track_f.argtypes = [ctypes.c_void_p]
    __PyObject_GC_Track_tf.tfname = "$PyObject_GC_Track".encode()
    __PyObject_GC_Track_tf.type = vpiSysTask
    __PyObject_GC_Track_fp = tf_func_t(__PyObject_GC_Track)
    __PyObject_GC_Track_tf.calltf = __PyObject_GC_Track_fp
    __PyObject_GC_Track_tf.userdata = None
    name = __PyObject_GC_Track_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GC_Track_tf))

    global __PyObject_GC_UnTrack_fp, __PyObject_GC_UnTrack_f, __PyObject_GC_UnTrack_tf
    __PyObject_GC_UnTrack_f = getattr(libpy, "PyObject_GC_UnTrack")
    __PyObject_GC_UnTrack_f.restype = None
    __PyObject_GC_UnTrack_f.argtypes = [ctypes.c_void_p]
    __PyObject_GC_UnTrack_tf.tfname = "$PyObject_GC_UnTrack".encode()
    __PyObject_GC_UnTrack_tf.type = vpiSysTask
    __PyObject_GC_UnTrack_fp = tf_func_t(__PyObject_GC_UnTrack)
    __PyObject_GC_UnTrack_tf.calltf = __PyObject_GC_UnTrack_fp
    __PyObject_GC_UnTrack_tf.userdata = None
    name = __PyObject_GC_UnTrack_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GC_UnTrack_tf))

    global __PyObject_GenericGetAttr_fp, __PyObject_GenericGetAttr_f, __PyObject_GenericGetAttr_tf
    __PyObject_GenericGetAttr_f = getattr(libpy, "PyObject_GenericGetAttr")
    __PyObject_GenericGetAttr_f.restype = ctypes.c_void_p
    __PyObject_GenericGetAttr_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_GenericGetAttr_tf.tfname = "$PyObject_GenericGetAttr".encode()
    __PyObject_GenericGetAttr_tf.type = vpiSysFunc
    __PyObject_GenericGetAttr_fp = tf_func_t(__PyObject_GenericGetAttr)
    __PyObject_GenericGetAttr_tf.calltf = __PyObject_GenericGetAttr_fp
    __PyObject_GenericGetAttr_tf.sizetf = sizetf64_fp
    __PyObject_GenericGetAttr_tf.userdata = None
    name = __PyObject_GenericGetAttr_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GenericGetAttr_tf))

    global __PyObject_GenericGetDict_fp, __PyObject_GenericGetDict_f, __PyObject_GenericGetDict_tf
    __PyObject_GenericGetDict_f = getattr(libpy, "PyObject_GenericGetDict")
    __PyObject_GenericGetDict_f.restype = ctypes.c_void_p
    __PyObject_GenericGetDict_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_GenericGetDict_tf.tfname = "$PyObject_GenericGetDict".encode()
    __PyObject_GenericGetDict_tf.type = vpiSysFunc
    __PyObject_GenericGetDict_fp = tf_func_t(__PyObject_GenericGetDict)
    __PyObject_GenericGetDict_tf.calltf = __PyObject_GenericGetDict_fp
    __PyObject_GenericGetDict_tf.sizetf = sizetf64_fp
    __PyObject_GenericGetDict_tf.userdata = None
    name = __PyObject_GenericGetDict_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GenericGetDict_tf))

    global __PyObject_GenericSetAttr_fp, __PyObject_GenericSetAttr_f, __PyObject_GenericSetAttr_tf
    __PyObject_GenericSetAttr_f = getattr(libpy, "PyObject_GenericSetAttr")
    __PyObject_GenericSetAttr_f.restype = ctypes.c_int
    __PyObject_GenericSetAttr_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_GenericSetAttr_tf.tfname = "$PyObject_GenericSetAttr".encode()
    __PyObject_GenericSetAttr_tf.type = vpiSysFunc
    __PyObject_GenericSetAttr_fp = tf_func_t(__PyObject_GenericSetAttr)
    __PyObject_GenericSetAttr_tf.calltf = __PyObject_GenericSetAttr_fp
    __PyObject_GenericSetAttr_tf.userdata = None
    name = __PyObject_GenericSetAttr_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GenericSetAttr_tf))

    global __PyObject_GenericSetDict_fp, __PyObject_GenericSetDict_f, __PyObject_GenericSetDict_tf
    __PyObject_GenericSetDict_f = getattr(libpy, "PyObject_GenericSetDict")
    __PyObject_GenericSetDict_f.restype = ctypes.c_int
    __PyObject_GenericSetDict_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_GenericSetDict_tf.tfname = "$PyObject_GenericSetDict".encode()
    __PyObject_GenericSetDict_tf.type = vpiSysFunc
    __PyObject_GenericSetDict_fp = tf_func_t(__PyObject_GenericSetDict)
    __PyObject_GenericSetDict_tf.calltf = __PyObject_GenericSetDict_fp
    __PyObject_GenericSetDict_tf.userdata = None
    name = __PyObject_GenericSetDict_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GenericSetDict_tf))

    global __PyObject_GetAIter_fp, __PyObject_GetAIter_f, __PyObject_GetAIter_tf
    __PyObject_GetAIter_f = getattr(libpy, "PyObject_GetAIter")
    __PyObject_GetAIter_f.restype = ctypes.c_void_p
    __PyObject_GetAIter_f.argtypes = [ctypes.c_void_p]
    __PyObject_GetAIter_tf.tfname = "$PyObject_GetAIter".encode()
    __PyObject_GetAIter_tf.type = vpiSysFunc
    __PyObject_GetAIter_fp = tf_func_t(__PyObject_GetAIter)
    __PyObject_GetAIter_tf.calltf = __PyObject_GetAIter_fp
    __PyObject_GetAIter_tf.sizetf = sizetf64_fp
    __PyObject_GetAIter_tf.userdata = None
    name = __PyObject_GetAIter_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GetAIter_tf))

    global __PyObject_GetAttr_fp, __PyObject_GetAttr_f, __PyObject_GetAttr_tf
    __PyObject_GetAttr_f = getattr(libpy, "PyObject_GetAttr")
    __PyObject_GetAttr_f.restype = ctypes.c_void_p
    __PyObject_GetAttr_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_GetAttr_tf.tfname = "$PyObject_GetAttr".encode()
    __PyObject_GetAttr_tf.type = vpiSysFunc
    __PyObject_GetAttr_fp = tf_func_t(__PyObject_GetAttr)
    __PyObject_GetAttr_tf.calltf = __PyObject_GetAttr_fp
    __PyObject_GetAttr_tf.sizetf = sizetf64_fp
    __PyObject_GetAttr_tf.userdata = None
    name = __PyObject_GetAttr_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GetAttr_tf))

    global __PyObject_GetAttrString_fp, __PyObject_GetAttrString_f, __PyObject_GetAttrString_tf
    __PyObject_GetAttrString_f = getattr(libpy, "PyObject_GetAttrString")
    __PyObject_GetAttrString_f.restype = ctypes.c_void_p
    __PyObject_GetAttrString_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    __PyObject_GetAttrString_tf.tfname = "$PyObject_GetAttrString".encode()
    __PyObject_GetAttrString_tf.type = vpiSysFunc
    __PyObject_GetAttrString_fp = tf_func_t(__PyObject_GetAttrString)
    __PyObject_GetAttrString_tf.calltf = __PyObject_GetAttrString_fp
    __PyObject_GetAttrString_tf.sizetf = sizetf64_fp
    __PyObject_GetAttrString_tf.userdata = None
    name = __PyObject_GetAttrString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GetAttrString_tf))

    global __PyObject_GetItem_fp, __PyObject_GetItem_f, __PyObject_GetItem_tf
    __PyObject_GetItem_f = getattr(libpy, "PyObject_GetItem")
    __PyObject_GetItem_f.restype = ctypes.c_void_p
    __PyObject_GetItem_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_GetItem_tf.tfname = "$PyObject_GetItem".encode()
    __PyObject_GetItem_tf.type = vpiSysFunc
    __PyObject_GetItem_fp = tf_func_t(__PyObject_GetItem)
    __PyObject_GetItem_tf.calltf = __PyObject_GetItem_fp
    __PyObject_GetItem_tf.sizetf = sizetf64_fp
    __PyObject_GetItem_tf.userdata = None
    name = __PyObject_GetItem_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GetItem_tf))

    global __PyObject_GetIter_fp, __PyObject_GetIter_f, __PyObject_GetIter_tf
    __PyObject_GetIter_f = getattr(libpy, "PyObject_GetIter")
    __PyObject_GetIter_f.restype = ctypes.c_void_p
    __PyObject_GetIter_f.argtypes = [ctypes.c_void_p]
    __PyObject_GetIter_tf.tfname = "$PyObject_GetIter".encode()
    __PyObject_GetIter_tf.type = vpiSysFunc
    __PyObject_GetIter_fp = tf_func_t(__PyObject_GetIter)
    __PyObject_GetIter_tf.calltf = __PyObject_GetIter_fp
    __PyObject_GetIter_tf.sizetf = sizetf64_fp
    __PyObject_GetIter_tf.userdata = None
    name = __PyObject_GetIter_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_GetIter_tf))

    global __PyObject_HasAttr_fp, __PyObject_HasAttr_f, __PyObject_HasAttr_tf
    __PyObject_HasAttr_f = getattr(libpy, "PyObject_HasAttr")
    __PyObject_HasAttr_f.restype = ctypes.c_int
    __PyObject_HasAttr_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_HasAttr_tf.tfname = "$PyObject_HasAttr".encode()
    __PyObject_HasAttr_tf.type = vpiSysFunc
    __PyObject_HasAttr_fp = tf_func_t(__PyObject_HasAttr)
    __PyObject_HasAttr_tf.calltf = __PyObject_HasAttr_fp
    __PyObject_HasAttr_tf.userdata = None
    name = __PyObject_HasAttr_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_HasAttr_tf))

    global __PyObject_HasAttrString_fp, __PyObject_HasAttrString_f, __PyObject_HasAttrString_tf
    __PyObject_HasAttrString_f = getattr(libpy, "PyObject_HasAttrString")
    __PyObject_HasAttrString_f.restype = ctypes.c_int
    __PyObject_HasAttrString_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    __PyObject_HasAttrString_tf.tfname = "$PyObject_HasAttrString".encode()
    __PyObject_HasAttrString_tf.type = vpiSysFunc
    __PyObject_HasAttrString_fp = tf_func_t(__PyObject_HasAttrString)
    __PyObject_HasAttrString_tf.calltf = __PyObject_HasAttrString_fp
    __PyObject_HasAttrString_tf.userdata = None
    name = __PyObject_HasAttrString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_HasAttrString_tf))

    global __PyObject_IS_GC_fp, __PyObject_IS_GC_f, __PyObject_IS_GC_tf
    __PyObject_IS_GC_f = getattr(libpy, "PyObject_IS_GC")
    __PyObject_IS_GC_f.restype = ctypes.c_int
    __PyObject_IS_GC_f.argtypes = [ctypes.c_void_p]
    __PyObject_IS_GC_tf.tfname = "$PyObject_IS_GC".encode()
    __PyObject_IS_GC_tf.type = vpiSysFunc
    __PyObject_IS_GC_fp = tf_func_t(__PyObject_IS_GC)
    __PyObject_IS_GC_tf.calltf = __PyObject_IS_GC_fp
    __PyObject_IS_GC_tf.userdata = None
    name = __PyObject_IS_GC_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_IS_GC_tf))

    global __PyObject_Init_fp, __PyObject_Init_f, __PyObject_Init_tf
    __PyObject_Init_f = getattr(libpy, "PyObject_Init")
    __PyObject_Init_f.restype = ctypes.c_void_p
    __PyObject_Init_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_Init_tf.tfname = "$PyObject_Init".encode()
    __PyObject_Init_tf.type = vpiSysFunc
    __PyObject_Init_fp = tf_func_t(__PyObject_Init)
    __PyObject_Init_tf.calltf = __PyObject_Init_fp
    __PyObject_Init_tf.sizetf = sizetf64_fp
    __PyObject_Init_tf.userdata = None
    name = __PyObject_Init_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Init_tf))

    global __PyObject_IsInstance_fp, __PyObject_IsInstance_f, __PyObject_IsInstance_tf
    __PyObject_IsInstance_f = getattr(libpy, "PyObject_IsInstance")
    __PyObject_IsInstance_f.restype = ctypes.c_int
    __PyObject_IsInstance_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_IsInstance_tf.tfname = "$PyObject_IsInstance".encode()
    __PyObject_IsInstance_tf.type = vpiSysFunc
    __PyObject_IsInstance_fp = tf_func_t(__PyObject_IsInstance)
    __PyObject_IsInstance_tf.calltf = __PyObject_IsInstance_fp
    __PyObject_IsInstance_tf.userdata = None
    name = __PyObject_IsInstance_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_IsInstance_tf))

    global __PyObject_IsSubclass_fp, __PyObject_IsSubclass_f, __PyObject_IsSubclass_tf
    __PyObject_IsSubclass_f = getattr(libpy, "PyObject_IsSubclass")
    __PyObject_IsSubclass_f.restype = ctypes.c_int
    __PyObject_IsSubclass_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_IsSubclass_tf.tfname = "$PyObject_IsSubclass".encode()
    __PyObject_IsSubclass_tf.type = vpiSysFunc
    __PyObject_IsSubclass_fp = tf_func_t(__PyObject_IsSubclass)
    __PyObject_IsSubclass_tf.calltf = __PyObject_IsSubclass_fp
    __PyObject_IsSubclass_tf.userdata = None
    name = __PyObject_IsSubclass_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_IsSubclass_tf))

    global __PyObject_IsTrue_fp, __PyObject_IsTrue_f, __PyObject_IsTrue_tf
    __PyObject_IsTrue_f = getattr(libpy, "PyObject_IsTrue")
    __PyObject_IsTrue_f.restype = ctypes.c_int
    __PyObject_IsTrue_f.argtypes = [ctypes.c_void_p]
    __PyObject_IsTrue_tf.tfname = "$PyObject_IsTrue".encode()
    __PyObject_IsTrue_tf.type = vpiSysFunc
    __PyObject_IsTrue_fp = tf_func_t(__PyObject_IsTrue)
    __PyObject_IsTrue_tf.calltf = __PyObject_IsTrue_fp
    __PyObject_IsTrue_tf.userdata = None
    name = __PyObject_IsTrue_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_IsTrue_tf))

    global __PyObject_LengthHint_fp, __PyObject_LengthHint_f, __PyObject_LengthHint_tf
    __PyObject_LengthHint_f = getattr(libpy, "PyObject_LengthHint")
    __PyObject_LengthHint_f.restype = ctypes.c_uint
    __PyObject_LengthHint_f.argtypes = [ctypes.c_void_p,ctypes.c_uint]
    __PyObject_LengthHint_tf.tfname = "$PyObject_LengthHint".encode()
    __PyObject_LengthHint_tf.type = vpiSysFunc
    __PyObject_LengthHint_fp = tf_func_t(__PyObject_LengthHint)
    __PyObject_LengthHint_tf.calltf = __PyObject_LengthHint_fp
    __PyObject_LengthHint_tf.userdata = None
    name = __PyObject_LengthHint_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_LengthHint_tf))

    global __PyObject_Malloc_fp, __PyObject_Malloc_f, __PyObject_Malloc_tf
    __PyObject_Malloc_f = getattr(libpy, "PyObject_Malloc")
    __PyObject_Malloc_f.restype = ctypes.c_void_p
    __PyObject_Malloc_f.argtypes = [ctypes.c_uint]
    __PyObject_Malloc_tf.tfname = "$PyObject_Malloc".encode()
    __PyObject_Malloc_tf.type = vpiSysFunc
    __PyObject_Malloc_fp = tf_func_t(__PyObject_Malloc)
    __PyObject_Malloc_tf.calltf = __PyObject_Malloc_fp
    __PyObject_Malloc_tf.sizetf = sizetf64_fp
    __PyObject_Malloc_tf.userdata = None
    name = __PyObject_Malloc_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Malloc_tf))

    global __PyObject_Not_fp, __PyObject_Not_f, __PyObject_Not_tf
    __PyObject_Not_f = getattr(libpy, "PyObject_Not")
    __PyObject_Not_f.restype = ctypes.c_int
    __PyObject_Not_f.argtypes = [ctypes.c_void_p]
    __PyObject_Not_tf.tfname = "$PyObject_Not".encode()
    __PyObject_Not_tf.type = vpiSysFunc
    __PyObject_Not_fp = tf_func_t(__PyObject_Not)
    __PyObject_Not_tf.calltf = __PyObject_Not_fp
    __PyObject_Not_tf.userdata = None
    name = __PyObject_Not_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Not_tf))

    global __PyObject_Realloc_fp, __PyObject_Realloc_f, __PyObject_Realloc_tf
    __PyObject_Realloc_f = getattr(libpy, "PyObject_Realloc")
    __PyObject_Realloc_f.restype = ctypes.c_void_p
    __PyObject_Realloc_f.argtypes = [ctypes.c_void_p,ctypes.c_uint]
    __PyObject_Realloc_tf.tfname = "$PyObject_Realloc".encode()
    __PyObject_Realloc_tf.type = vpiSysFunc
    __PyObject_Realloc_fp = tf_func_t(__PyObject_Realloc)
    __PyObject_Realloc_tf.calltf = __PyObject_Realloc_fp
    __PyObject_Realloc_tf.sizetf = sizetf64_fp
    __PyObject_Realloc_tf.userdata = None
    name = __PyObject_Realloc_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Realloc_tf))

    global __PyObject_Repr_fp, __PyObject_Repr_f, __PyObject_Repr_tf
    __PyObject_Repr_f = getattr(libpy, "PyObject_Repr")
    __PyObject_Repr_f.restype = ctypes.c_void_p
    __PyObject_Repr_f.argtypes = [ctypes.c_void_p]
    __PyObject_Repr_tf.tfname = "$PyObject_Repr".encode()
    __PyObject_Repr_tf.type = vpiSysFunc
    __PyObject_Repr_fp = tf_func_t(__PyObject_Repr)
    __PyObject_Repr_tf.calltf = __PyObject_Repr_fp
    __PyObject_Repr_tf.sizetf = sizetf64_fp
    __PyObject_Repr_tf.userdata = None
    name = __PyObject_Repr_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Repr_tf))

    global __PyObject_RichCompare_fp, __PyObject_RichCompare_f, __PyObject_RichCompare_tf
    __PyObject_RichCompare_f = getattr(libpy, "PyObject_RichCompare")
    __PyObject_RichCompare_f.restype = ctypes.c_void_p
    __PyObject_RichCompare_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
    __PyObject_RichCompare_tf.tfname = "$PyObject_RichCompare".encode()
    __PyObject_RichCompare_tf.type = vpiSysFunc
    __PyObject_RichCompare_fp = tf_func_t(__PyObject_RichCompare)
    __PyObject_RichCompare_tf.calltf = __PyObject_RichCompare_fp
    __PyObject_RichCompare_tf.sizetf = sizetf64_fp
    __PyObject_RichCompare_tf.userdata = None
    name = __PyObject_RichCompare_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_RichCompare_tf))

    global __PyObject_RichCompareBool_fp, __PyObject_RichCompareBool_f, __PyObject_RichCompareBool_tf
    __PyObject_RichCompareBool_f = getattr(libpy, "PyObject_RichCompareBool")
    __PyObject_RichCompareBool_f.restype = ctypes.c_int
    __PyObject_RichCompareBool_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
    __PyObject_RichCompareBool_tf.tfname = "$PyObject_RichCompareBool".encode()
    __PyObject_RichCompareBool_tf.type = vpiSysFunc
    __PyObject_RichCompareBool_fp = tf_func_t(__PyObject_RichCompareBool)
    __PyObject_RichCompareBool_tf.calltf = __PyObject_RichCompareBool_fp
    __PyObject_RichCompareBool_tf.userdata = None
    name = __PyObject_RichCompareBool_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_RichCompareBool_tf))

    global __PyObject_SelfIter_fp, __PyObject_SelfIter_f, __PyObject_SelfIter_tf
    __PyObject_SelfIter_f = getattr(libpy, "PyObject_SelfIter")
    __PyObject_SelfIter_f.restype = ctypes.c_void_p
    __PyObject_SelfIter_f.argtypes = [ctypes.c_void_p]
    __PyObject_SelfIter_tf.tfname = "$PyObject_SelfIter".encode()
    __PyObject_SelfIter_tf.type = vpiSysFunc
    __PyObject_SelfIter_fp = tf_func_t(__PyObject_SelfIter)
    __PyObject_SelfIter_tf.calltf = __PyObject_SelfIter_fp
    __PyObject_SelfIter_tf.sizetf = sizetf64_fp
    __PyObject_SelfIter_tf.userdata = None
    name = __PyObject_SelfIter_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_SelfIter_tf))

    global __PyObject_SetAttr_fp, __PyObject_SetAttr_f, __PyObject_SetAttr_tf
    __PyObject_SetAttr_f = getattr(libpy, "PyObject_SetAttr")
    __PyObject_SetAttr_f.restype = ctypes.c_int
    __PyObject_SetAttr_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_SetAttr_tf.tfname = "$PyObject_SetAttr".encode()
    __PyObject_SetAttr_tf.type = vpiSysFunc
    __PyObject_SetAttr_fp = tf_func_t(__PyObject_SetAttr)
    __PyObject_SetAttr_tf.calltf = __PyObject_SetAttr_fp
    __PyObject_SetAttr_tf.userdata = None
    name = __PyObject_SetAttr_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_SetAttr_tf))

    global __PyObject_SetAttrString_fp, __PyObject_SetAttrString_f, __PyObject_SetAttrString_tf
    __PyObject_SetAttrString_f = getattr(libpy, "PyObject_SetAttrString")
    __PyObject_SetAttrString_f.restype = ctypes.c_int
    __PyObject_SetAttrString_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
    __PyObject_SetAttrString_tf.tfname = "$PyObject_SetAttrString".encode()
    __PyObject_SetAttrString_tf.type = vpiSysFunc
    __PyObject_SetAttrString_fp = tf_func_t(__PyObject_SetAttrString)
    __PyObject_SetAttrString_tf.calltf = __PyObject_SetAttrString_fp
    __PyObject_SetAttrString_tf.userdata = None
    name = __PyObject_SetAttrString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_SetAttrString_tf))

    global __PyObject_SetItem_fp, __PyObject_SetItem_f, __PyObject_SetItem_tf
    __PyObject_SetItem_f = getattr(libpy, "PyObject_SetItem")
    __PyObject_SetItem_f.restype = ctypes.c_int
    __PyObject_SetItem_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    __PyObject_SetItem_tf.tfname = "$PyObject_SetItem".encode()
    __PyObject_SetItem_tf.type = vpiSysFunc
    __PyObject_SetItem_fp = tf_func_t(__PyObject_SetItem)
    __PyObject_SetItem_tf.calltf = __PyObject_SetItem_fp
    __PyObject_SetItem_tf.userdata = None
    name = __PyObject_SetItem_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_SetItem_tf))

    global __PyObject_Size_fp, __PyObject_Size_f, __PyObject_Size_tf
    __PyObject_Size_f = getattr(libpy, "PyObject_Size")
    __PyObject_Size_f.restype = ctypes.c_uint
    __PyObject_Size_f.argtypes = [ctypes.c_void_p]
    __PyObject_Size_tf.tfname = "$PyObject_Size".encode()
    __PyObject_Size_tf.type = vpiSysFunc
    __PyObject_Size_fp = tf_func_t(__PyObject_Size)
    __PyObject_Size_tf.calltf = __PyObject_Size_fp
    __PyObject_Size_tf.userdata = None
    name = __PyObject_Size_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Size_tf))

    global __PyObject_Str_fp, __PyObject_Str_f, __PyObject_Str_tf
    __PyObject_Str_f = getattr(libpy, "PyObject_Str")
    __PyObject_Str_f.restype = ctypes.c_void_p
    __PyObject_Str_f.argtypes = [ctypes.c_void_p]
    __PyObject_Str_tf.tfname = "$PyObject_Str".encode()
    __PyObject_Str_tf.type = vpiSysFunc
    __PyObject_Str_fp = tf_func_t(__PyObject_Str)
    __PyObject_Str_tf.calltf = __PyObject_Str_fp
    __PyObject_Str_tf.sizetf = sizetf64_fp
    __PyObject_Str_tf.userdata = None
    name = __PyObject_Str_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Str_tf))

    global __PyObject_Type_fp, __PyObject_Type_f, __PyObject_Type_tf
    __PyObject_Type_f = getattr(libpy, "PyObject_Type")
    __PyObject_Type_f.restype = ctypes.c_void_p
    __PyObject_Type_f.argtypes = [ctypes.c_void_p]
    __PyObject_Type_tf.tfname = "$PyObject_Type".encode()
    __PyObject_Type_tf.type = vpiSysFunc
    __PyObject_Type_fp = tf_func_t(__PyObject_Type)
    __PyObject_Type_tf.calltf = __PyObject_Type_fp
    __PyObject_Type_tf.sizetf = sizetf64_fp
    __PyObject_Type_tf.userdata = None
    name = __PyObject_Type_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyObject_Type_tf))

    global __PyTuple_GetItem_fp, __PyTuple_GetItem_f, __PyTuple_GetItem_tf
    __PyTuple_GetItem_f = getattr(libpy, "PyTuple_GetItem")
    __PyTuple_GetItem_f.restype = ctypes.c_void_p
    __PyTuple_GetItem_f.argtypes = [ctypes.c_void_p,ctypes.c_uint]
    __PyTuple_GetItem_tf.tfname = "$PyTuple_GetItem".encode()
    __PyTuple_GetItem_tf.type = vpiSysFunc
    __PyTuple_GetItem_fp = tf_func_t(__PyTuple_GetItem)
    __PyTuple_GetItem_tf.calltf = __PyTuple_GetItem_fp
    __PyTuple_GetItem_tf.sizetf = sizetf64_fp
    __PyTuple_GetItem_tf.userdata = None
    name = __PyTuple_GetItem_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyTuple_GetItem_tf))

    global __PyTuple_GetSlice_fp, __PyTuple_GetSlice_f, __PyTuple_GetSlice_tf
    __PyTuple_GetSlice_f = getattr(libpy, "PyTuple_GetSlice")
    __PyTuple_GetSlice_f.restype = ctypes.c_void_p
    __PyTuple_GetSlice_f.argtypes = [ctypes.c_void_p,ctypes.c_uint,ctypes.c_uint]
    __PyTuple_GetSlice_tf.tfname = "$PyTuple_GetSlice".encode()
    __PyTuple_GetSlice_tf.type = vpiSysFunc
    __PyTuple_GetSlice_fp = tf_func_t(__PyTuple_GetSlice)
    __PyTuple_GetSlice_tf.calltf = __PyTuple_GetSlice_fp
    __PyTuple_GetSlice_tf.sizetf = sizetf64_fp
    __PyTuple_GetSlice_tf.userdata = None
    name = __PyTuple_GetSlice_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyTuple_GetSlice_tf))

    global __PyTuple_New_fp, __PyTuple_New_f, __PyTuple_New_tf
    __PyTuple_New_f = getattr(libpy, "PyTuple_New")
    __PyTuple_New_f.restype = ctypes.c_void_p
    __PyTuple_New_f.argtypes = [ctypes.c_uint]
    __PyTuple_New_tf.tfname = "$PyTuple_New".encode()
    __PyTuple_New_tf.type = vpiSysFunc
    __PyTuple_New_fp = tf_func_t(__PyTuple_New)
    __PyTuple_New_tf.calltf = __PyTuple_New_fp
    __PyTuple_New_tf.sizetf = sizetf64_fp
    __PyTuple_New_tf.userdata = None
    name = __PyTuple_New_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyTuple_New_tf))

    global __PyTuple_SetItem_fp, __PyTuple_SetItem_f, __PyTuple_SetItem_tf
    __PyTuple_SetItem_f = getattr(libpy, "PyTuple_SetItem")
    __PyTuple_SetItem_f.restype = ctypes.c_int
    __PyTuple_SetItem_f.argtypes = [ctypes.c_void_p,ctypes.c_uint,ctypes.c_void_p]
    __PyTuple_SetItem_tf.tfname = "$PyTuple_SetItem".encode()
    __PyTuple_SetItem_tf.type = vpiSysFunc
    __PyTuple_SetItem_fp = tf_func_t(__PyTuple_SetItem)
    __PyTuple_SetItem_tf.calltf = __PyTuple_SetItem_fp
    __PyTuple_SetItem_tf.userdata = None
    name = __PyTuple_SetItem_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyTuple_SetItem_tf))

    global __PyTuple_Size_fp, __PyTuple_Size_f, __PyTuple_Size_tf
    __PyTuple_Size_f = getattr(libpy, "PyTuple_Size")
    __PyTuple_Size_f.restype = ctypes.c_uint
    __PyTuple_Size_f.argtypes = [ctypes.c_void_p]
    __PyTuple_Size_tf.tfname = "$PyTuple_Size".encode()
    __PyTuple_Size_tf.type = vpiSysFunc
    __PyTuple_Size_fp = tf_func_t(__PyTuple_Size)
    __PyTuple_Size_tf.calltf = __PyTuple_Size_fp
    __PyTuple_Size_tf.userdata = None
    name = __PyTuple_Size_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyTuple_Size_tf))

    global __PyUnicode_AsASCIIString_fp, __PyUnicode_AsASCIIString_f, __PyUnicode_AsASCIIString_tf
    __PyUnicode_AsASCIIString_f = getattr(libpy, "PyUnicode_AsASCIIString")
    __PyUnicode_AsASCIIString_f.restype = ctypes.c_void_p
    __PyUnicode_AsASCIIString_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_AsASCIIString_tf.tfname = "$PyUnicode_AsASCIIString".encode()
    __PyUnicode_AsASCIIString_tf.type = vpiSysFunc
    __PyUnicode_AsASCIIString_fp = tf_func_t(__PyUnicode_AsASCIIString)
    __PyUnicode_AsASCIIString_tf.calltf = __PyUnicode_AsASCIIString_fp
    __PyUnicode_AsASCIIString_tf.sizetf = sizetf64_fp
    __PyUnicode_AsASCIIString_tf.userdata = None
    name = __PyUnicode_AsASCIIString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsASCIIString_tf))

    global __PyUnicode_AsCharmapString_fp, __PyUnicode_AsCharmapString_f, __PyUnicode_AsCharmapString_tf
    __PyUnicode_AsCharmapString_f = getattr(libpy, "PyUnicode_AsCharmapString")
    __PyUnicode_AsCharmapString_f.restype = ctypes.c_void_p
    __PyUnicode_AsCharmapString_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_AsCharmapString_tf.tfname = "$PyUnicode_AsCharmapString".encode()
    __PyUnicode_AsCharmapString_tf.type = vpiSysFunc
    __PyUnicode_AsCharmapString_fp = tf_func_t(__PyUnicode_AsCharmapString)
    __PyUnicode_AsCharmapString_tf.calltf = __PyUnicode_AsCharmapString_fp
    __PyUnicode_AsCharmapString_tf.sizetf = sizetf64_fp
    __PyUnicode_AsCharmapString_tf.userdata = None
    name = __PyUnicode_AsCharmapString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsCharmapString_tf))

    global __PyUnicode_AsDecodedObject_fp, __PyUnicode_AsDecodedObject_f, __PyUnicode_AsDecodedObject_tf
    __PyUnicode_AsDecodedObject_f = getattr(libpy, "PyUnicode_AsDecodedObject")
    __PyUnicode_AsDecodedObject_f.restype = ctypes.c_void_p
    __PyUnicode_AsDecodedObject_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
    __PyUnicode_AsDecodedObject_tf.tfname = "$PyUnicode_AsDecodedObject".encode()
    __PyUnicode_AsDecodedObject_tf.type = vpiSysFunc
    __PyUnicode_AsDecodedObject_fp = tf_func_t(__PyUnicode_AsDecodedObject)
    __PyUnicode_AsDecodedObject_tf.calltf = __PyUnicode_AsDecodedObject_fp
    __PyUnicode_AsDecodedObject_tf.sizetf = sizetf64_fp
    __PyUnicode_AsDecodedObject_tf.userdata = None
    name = __PyUnicode_AsDecodedObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsDecodedObject_tf))

    global __PyUnicode_AsDecodedUnicode_fp, __PyUnicode_AsDecodedUnicode_f, __PyUnicode_AsDecodedUnicode_tf
    __PyUnicode_AsDecodedUnicode_f = getattr(libpy, "PyUnicode_AsDecodedUnicode")
    __PyUnicode_AsDecodedUnicode_f.restype = ctypes.c_void_p
    __PyUnicode_AsDecodedUnicode_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
    __PyUnicode_AsDecodedUnicode_tf.tfname = "$PyUnicode_AsDecodedUnicode".encode()
    __PyUnicode_AsDecodedUnicode_tf.type = vpiSysFunc
    __PyUnicode_AsDecodedUnicode_fp = tf_func_t(__PyUnicode_AsDecodedUnicode)
    __PyUnicode_AsDecodedUnicode_tf.calltf = __PyUnicode_AsDecodedUnicode_fp
    __PyUnicode_AsDecodedUnicode_tf.sizetf = sizetf64_fp
    __PyUnicode_AsDecodedUnicode_tf.userdata = None
    name = __PyUnicode_AsDecodedUnicode_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsDecodedUnicode_tf))

    global __PyUnicode_AsEncodedObject_fp, __PyUnicode_AsEncodedObject_f, __PyUnicode_AsEncodedObject_tf
    __PyUnicode_AsEncodedObject_f = getattr(libpy, "PyUnicode_AsEncodedObject")
    __PyUnicode_AsEncodedObject_f.restype = ctypes.c_void_p
    __PyUnicode_AsEncodedObject_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
    __PyUnicode_AsEncodedObject_tf.tfname = "$PyUnicode_AsEncodedObject".encode()
    __PyUnicode_AsEncodedObject_tf.type = vpiSysFunc
    __PyUnicode_AsEncodedObject_fp = tf_func_t(__PyUnicode_AsEncodedObject)
    __PyUnicode_AsEncodedObject_tf.calltf = __PyUnicode_AsEncodedObject_fp
    __PyUnicode_AsEncodedObject_tf.sizetf = sizetf64_fp
    __PyUnicode_AsEncodedObject_tf.userdata = None
    name = __PyUnicode_AsEncodedObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsEncodedObject_tf))

    global __PyUnicode_AsEncodedString_fp, __PyUnicode_AsEncodedString_f, __PyUnicode_AsEncodedString_tf
    __PyUnicode_AsEncodedString_f = getattr(libpy, "PyUnicode_AsEncodedString")
    __PyUnicode_AsEncodedString_f.restype = ctypes.c_void_p
    __PyUnicode_AsEncodedString_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
    __PyUnicode_AsEncodedString_tf.tfname = "$PyUnicode_AsEncodedString".encode()
    __PyUnicode_AsEncodedString_tf.type = vpiSysFunc
    __PyUnicode_AsEncodedString_fp = tf_func_t(__PyUnicode_AsEncodedString)
    __PyUnicode_AsEncodedString_tf.calltf = __PyUnicode_AsEncodedString_fp
    __PyUnicode_AsEncodedString_tf.sizetf = sizetf64_fp
    __PyUnicode_AsEncodedString_tf.userdata = None
    name = __PyUnicode_AsEncodedString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsEncodedString_tf))

    global __PyUnicode_AsEncodedUnicode_fp, __PyUnicode_AsEncodedUnicode_f, __PyUnicode_AsEncodedUnicode_tf
    __PyUnicode_AsEncodedUnicode_f = getattr(libpy, "PyUnicode_AsEncodedUnicode")
    __PyUnicode_AsEncodedUnicode_f.restype = ctypes.c_void_p
    __PyUnicode_AsEncodedUnicode_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
    __PyUnicode_AsEncodedUnicode_tf.tfname = "$PyUnicode_AsEncodedUnicode".encode()
    __PyUnicode_AsEncodedUnicode_tf.type = vpiSysFunc
    __PyUnicode_AsEncodedUnicode_fp = tf_func_t(__PyUnicode_AsEncodedUnicode)
    __PyUnicode_AsEncodedUnicode_tf.calltf = __PyUnicode_AsEncodedUnicode_fp
    __PyUnicode_AsEncodedUnicode_tf.sizetf = sizetf64_fp
    __PyUnicode_AsEncodedUnicode_tf.userdata = None
    name = __PyUnicode_AsEncodedUnicode_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsEncodedUnicode_tf))

    global __PyUnicode_AsLatin1String_fp, __PyUnicode_AsLatin1String_f, __PyUnicode_AsLatin1String_tf
    __PyUnicode_AsLatin1String_f = getattr(libpy, "PyUnicode_AsLatin1String")
    __PyUnicode_AsLatin1String_f.restype = ctypes.c_void_p
    __PyUnicode_AsLatin1String_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_AsLatin1String_tf.tfname = "$PyUnicode_AsLatin1String".encode()
    __PyUnicode_AsLatin1String_tf.type = vpiSysFunc
    __PyUnicode_AsLatin1String_fp = tf_func_t(__PyUnicode_AsLatin1String)
    __PyUnicode_AsLatin1String_tf.calltf = __PyUnicode_AsLatin1String_fp
    __PyUnicode_AsLatin1String_tf.sizetf = sizetf64_fp
    __PyUnicode_AsLatin1String_tf.userdata = None
    name = __PyUnicode_AsLatin1String_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsLatin1String_tf))

    global __PyUnicode_AsRawUnicodeEscapeString_fp, __PyUnicode_AsRawUnicodeEscapeString_f, __PyUnicode_AsRawUnicodeEscapeString_tf
    __PyUnicode_AsRawUnicodeEscapeString_f = getattr(libpy, "PyUnicode_AsRawUnicodeEscapeString")
    __PyUnicode_AsRawUnicodeEscapeString_f.restype = ctypes.c_void_p
    __PyUnicode_AsRawUnicodeEscapeString_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_AsRawUnicodeEscapeString_tf.tfname = "$PyUnicode_AsRawUnicodeEscapeString".encode()
    __PyUnicode_AsRawUnicodeEscapeString_tf.type = vpiSysFunc
    __PyUnicode_AsRawUnicodeEscapeString_fp = tf_func_t(__PyUnicode_AsRawUnicodeEscapeString)
    __PyUnicode_AsRawUnicodeEscapeString_tf.calltf = __PyUnicode_AsRawUnicodeEscapeString_fp
    __PyUnicode_AsRawUnicodeEscapeString_tf.sizetf = sizetf64_fp
    __PyUnicode_AsRawUnicodeEscapeString_tf.userdata = None
    name = __PyUnicode_AsRawUnicodeEscapeString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsRawUnicodeEscapeString_tf))

    global __PyUnicode_AsUTF16String_fp, __PyUnicode_AsUTF16String_f, __PyUnicode_AsUTF16String_tf
    __PyUnicode_AsUTF16String_f = getattr(libpy, "PyUnicode_AsUTF16String")
    __PyUnicode_AsUTF16String_f.restype = ctypes.c_void_p
    __PyUnicode_AsUTF16String_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_AsUTF16String_tf.tfname = "$PyUnicode_AsUTF16String".encode()
    __PyUnicode_AsUTF16String_tf.type = vpiSysFunc
    __PyUnicode_AsUTF16String_fp = tf_func_t(__PyUnicode_AsUTF16String)
    __PyUnicode_AsUTF16String_tf.calltf = __PyUnicode_AsUTF16String_fp
    __PyUnicode_AsUTF16String_tf.sizetf = sizetf64_fp
    __PyUnicode_AsUTF16String_tf.userdata = None
    name = __PyUnicode_AsUTF16String_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsUTF16String_tf))

    global __PyUnicode_AsUTF32String_fp, __PyUnicode_AsUTF32String_f, __PyUnicode_AsUTF32String_tf
    __PyUnicode_AsUTF32String_f = getattr(libpy, "PyUnicode_AsUTF32String")
    __PyUnicode_AsUTF32String_f.restype = ctypes.c_void_p
    __PyUnicode_AsUTF32String_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_AsUTF32String_tf.tfname = "$PyUnicode_AsUTF32String".encode()
    __PyUnicode_AsUTF32String_tf.type = vpiSysFunc
    __PyUnicode_AsUTF32String_fp = tf_func_t(__PyUnicode_AsUTF32String)
    __PyUnicode_AsUTF32String_tf.calltf = __PyUnicode_AsUTF32String_fp
    __PyUnicode_AsUTF32String_tf.sizetf = sizetf64_fp
    __PyUnicode_AsUTF32String_tf.userdata = None
    name = __PyUnicode_AsUTF32String_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsUTF32String_tf))

    global __PyUnicode_AsUTF8_fp, __PyUnicode_AsUTF8_f, __PyUnicode_AsUTF8_tf
    __PyUnicode_AsUTF8_f = getattr(libpy, "PyUnicode_AsUTF8")
    __PyUnicode_AsUTF8_f.restype = ctypes.c_char_p
    __PyUnicode_AsUTF8_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_AsUTF8_tf.tfname = "$PyUnicode_AsUTF8".encode()
    __PyUnicode_AsUTF8_tf.type = vpiSysTask
    __PyUnicode_AsUTF8_fp = tf_func_t(__PyUnicode_AsUTF8)
    __PyUnicode_AsUTF8_tf.calltf = __PyUnicode_AsUTF8_fp
    __PyUnicode_AsUTF8_tf.userdata = None
    name = __PyUnicode_AsUTF8_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsUTF8_tf))

    global __PyUnicode_AsUTF8AndSize_fp, __PyUnicode_AsUTF8AndSize_f, __PyUnicode_AsUTF8AndSize_tf
    __PyUnicode_AsUTF8AndSize_f = getattr(libpy, "PyUnicode_AsUTF8AndSize")
    __PyUnicode_AsUTF8AndSize_f.restype = ctypes.c_char_p
    __PyUnicode_AsUTF8AndSize_f.argtypes = [ctypes.c_void_p,ctypes.POINTER(ctypes.c_uint)]
    __PyUnicode_AsUTF8AndSize_tf.tfname = "$PyUnicode_AsUTF8AndSize".encode()
    __PyUnicode_AsUTF8AndSize_tf.type = vpiSysTask
    __PyUnicode_AsUTF8AndSize_fp = tf_func_t(__PyUnicode_AsUTF8AndSize)
    __PyUnicode_AsUTF8AndSize_tf.calltf = __PyUnicode_AsUTF8AndSize_fp
    __PyUnicode_AsUTF8AndSize_tf.userdata = None
    name = __PyUnicode_AsUTF8AndSize_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsUTF8AndSize_tf))

    global __PyUnicode_AsUTF8String_fp, __PyUnicode_AsUTF8String_f, __PyUnicode_AsUTF8String_tf
    __PyUnicode_AsUTF8String_f = getattr(libpy, "PyUnicode_AsUTF8String")
    __PyUnicode_AsUTF8String_f.restype = ctypes.c_void_p
    __PyUnicode_AsUTF8String_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_AsUTF8String_tf.tfname = "$PyUnicode_AsUTF8String".encode()
    __PyUnicode_AsUTF8String_tf.type = vpiSysFunc
    __PyUnicode_AsUTF8String_fp = tf_func_t(__PyUnicode_AsUTF8String)
    __PyUnicode_AsUTF8String_tf.calltf = __PyUnicode_AsUTF8String_fp
    __PyUnicode_AsUTF8String_tf.sizetf = sizetf64_fp
    __PyUnicode_AsUTF8String_tf.userdata = None
    name = __PyUnicode_AsUTF8String_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsUTF8String_tf))

    global __PyUnicode_AsUnicodeEscapeString_fp, __PyUnicode_AsUnicodeEscapeString_f, __PyUnicode_AsUnicodeEscapeString_tf
    __PyUnicode_AsUnicodeEscapeString_f = getattr(libpy, "PyUnicode_AsUnicodeEscapeString")
    __PyUnicode_AsUnicodeEscapeString_f.restype = ctypes.c_void_p
    __PyUnicode_AsUnicodeEscapeString_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_AsUnicodeEscapeString_tf.tfname = "$PyUnicode_AsUnicodeEscapeString".encode()
    __PyUnicode_AsUnicodeEscapeString_tf.type = vpiSysFunc
    __PyUnicode_AsUnicodeEscapeString_fp = tf_func_t(__PyUnicode_AsUnicodeEscapeString)
    __PyUnicode_AsUnicodeEscapeString_tf.calltf = __PyUnicode_AsUnicodeEscapeString_fp
    __PyUnicode_AsUnicodeEscapeString_tf.sizetf = sizetf64_fp
    __PyUnicode_AsUnicodeEscapeString_tf.userdata = None
    name = __PyUnicode_AsUnicodeEscapeString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_AsUnicodeEscapeString_tf))

    global __PyUnicode_BuildEncodingMap_fp, __PyUnicode_BuildEncodingMap_f, __PyUnicode_BuildEncodingMap_tf
    __PyUnicode_BuildEncodingMap_f = getattr(libpy, "PyUnicode_BuildEncodingMap")
    __PyUnicode_BuildEncodingMap_f.restype = ctypes.c_void_p
    __PyUnicode_BuildEncodingMap_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_BuildEncodingMap_tf.tfname = "$PyUnicode_BuildEncodingMap".encode()
    __PyUnicode_BuildEncodingMap_tf.type = vpiSysFunc
    __PyUnicode_BuildEncodingMap_fp = tf_func_t(__PyUnicode_BuildEncodingMap)
    __PyUnicode_BuildEncodingMap_tf.calltf = __PyUnicode_BuildEncodingMap_fp
    __PyUnicode_BuildEncodingMap_tf.sizetf = sizetf64_fp
    __PyUnicode_BuildEncodingMap_tf.userdata = None
    name = __PyUnicode_BuildEncodingMap_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_BuildEncodingMap_tf))

    global __PyUnicode_Compare_fp, __PyUnicode_Compare_f, __PyUnicode_Compare_tf
    __PyUnicode_Compare_f = getattr(libpy, "PyUnicode_Compare")
    __PyUnicode_Compare_f.restype = ctypes.c_int
    __PyUnicode_Compare_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_Compare_tf.tfname = "$PyUnicode_Compare".encode()
    __PyUnicode_Compare_tf.type = vpiSysFunc
    __PyUnicode_Compare_fp = tf_func_t(__PyUnicode_Compare)
    __PyUnicode_Compare_tf.calltf = __PyUnicode_Compare_fp
    __PyUnicode_Compare_tf.userdata = None
    name = __PyUnicode_Compare_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Compare_tf))

    global __PyUnicode_CompareWithASCIIString_fp, __PyUnicode_CompareWithASCIIString_f, __PyUnicode_CompareWithASCIIString_tf
    __PyUnicode_CompareWithASCIIString_f = getattr(libpy, "PyUnicode_CompareWithASCIIString")
    __PyUnicode_CompareWithASCIIString_f.restype = ctypes.c_int
    __PyUnicode_CompareWithASCIIString_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    __PyUnicode_CompareWithASCIIString_tf.tfname = "$PyUnicode_CompareWithASCIIString".encode()
    __PyUnicode_CompareWithASCIIString_tf.type = vpiSysFunc
    __PyUnicode_CompareWithASCIIString_fp = tf_func_t(__PyUnicode_CompareWithASCIIString)
    __PyUnicode_CompareWithASCIIString_tf.calltf = __PyUnicode_CompareWithASCIIString_fp
    __PyUnicode_CompareWithASCIIString_tf.userdata = None
    name = __PyUnicode_CompareWithASCIIString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_CompareWithASCIIString_tf))

    global __PyUnicode_Concat_fp, __PyUnicode_Concat_f, __PyUnicode_Concat_tf
    __PyUnicode_Concat_f = getattr(libpy, "PyUnicode_Concat")
    __PyUnicode_Concat_f.restype = ctypes.c_void_p
    __PyUnicode_Concat_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_Concat_tf.tfname = "$PyUnicode_Concat".encode()
    __PyUnicode_Concat_tf.type = vpiSysFunc
    __PyUnicode_Concat_fp = tf_func_t(__PyUnicode_Concat)
    __PyUnicode_Concat_tf.calltf = __PyUnicode_Concat_fp
    __PyUnicode_Concat_tf.sizetf = sizetf64_fp
    __PyUnicode_Concat_tf.userdata = None
    name = __PyUnicode_Concat_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Concat_tf))

    global __PyUnicode_Contains_fp, __PyUnicode_Contains_f, __PyUnicode_Contains_tf
    __PyUnicode_Contains_f = getattr(libpy, "PyUnicode_Contains")
    __PyUnicode_Contains_f.restype = ctypes.c_int
    __PyUnicode_Contains_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_Contains_tf.tfname = "$PyUnicode_Contains".encode()
    __PyUnicode_Contains_tf.type = vpiSysFunc
    __PyUnicode_Contains_fp = tf_func_t(__PyUnicode_Contains)
    __PyUnicode_Contains_tf.calltf = __PyUnicode_Contains_fp
    __PyUnicode_Contains_tf.userdata = None
    name = __PyUnicode_Contains_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Contains_tf))

    global __PyUnicode_CopyCharacters_fp, __PyUnicode_CopyCharacters_f, __PyUnicode_CopyCharacters_tf
    __PyUnicode_CopyCharacters_f = getattr(libpy, "PyUnicode_CopyCharacters")
    __PyUnicode_CopyCharacters_f.restype = ctypes.c_uint
    __PyUnicode_CopyCharacters_f.argtypes = [ctypes.c_void_p,ctypes.c_uint,ctypes.c_void_p,ctypes.c_uint,ctypes.c_uint]
    __PyUnicode_CopyCharacters_tf.tfname = "$PyUnicode_CopyCharacters".encode()
    __PyUnicode_CopyCharacters_tf.type = vpiSysFunc
    __PyUnicode_CopyCharacters_fp = tf_func_t(__PyUnicode_CopyCharacters)
    __PyUnicode_CopyCharacters_tf.calltf = __PyUnicode_CopyCharacters_fp
    __PyUnicode_CopyCharacters_tf.userdata = None
    name = __PyUnicode_CopyCharacters_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_CopyCharacters_tf))

    global __PyUnicode_Count_fp, __PyUnicode_Count_f, __PyUnicode_Count_tf
    __PyUnicode_Count_f = getattr(libpy, "PyUnicode_Count")
    __PyUnicode_Count_f.restype = ctypes.c_uint
    __PyUnicode_Count_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_uint,ctypes.c_uint]
    __PyUnicode_Count_tf.tfname = "$PyUnicode_Count".encode()
    __PyUnicode_Count_tf.type = vpiSysFunc
    __PyUnicode_Count_fp = tf_func_t(__PyUnicode_Count)
    __PyUnicode_Count_tf.calltf = __PyUnicode_Count_fp
    __PyUnicode_Count_tf.userdata = None
    name = __PyUnicode_Count_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Count_tf))

    global __PyUnicode_Decode_fp, __PyUnicode_Decode_f, __PyUnicode_Decode_tf
    __PyUnicode_Decode_f = getattr(libpy, "PyUnicode_Decode")
    __PyUnicode_Decode_f.restype = ctypes.c_void_p
    __PyUnicode_Decode_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p,ctypes.c_char_p]
    __PyUnicode_Decode_tf.tfname = "$PyUnicode_Decode".encode()
    __PyUnicode_Decode_tf.type = vpiSysFunc
    __PyUnicode_Decode_fp = tf_func_t(__PyUnicode_Decode)
    __PyUnicode_Decode_tf.calltf = __PyUnicode_Decode_fp
    __PyUnicode_Decode_tf.sizetf = sizetf64_fp
    __PyUnicode_Decode_tf.userdata = None
    name = __PyUnicode_Decode_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Decode_tf))

    global __PyUnicode_DecodeASCII_fp, __PyUnicode_DecodeASCII_f, __PyUnicode_DecodeASCII_tf
    __PyUnicode_DecodeASCII_f = getattr(libpy, "PyUnicode_DecodeASCII")
    __PyUnicode_DecodeASCII_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeASCII_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p]
    __PyUnicode_DecodeASCII_tf.tfname = "$PyUnicode_DecodeASCII".encode()
    __PyUnicode_DecodeASCII_tf.type = vpiSysFunc
    __PyUnicode_DecodeASCII_fp = tf_func_t(__PyUnicode_DecodeASCII)
    __PyUnicode_DecodeASCII_tf.calltf = __PyUnicode_DecodeASCII_fp
    __PyUnicode_DecodeASCII_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeASCII_tf.userdata = None
    name = __PyUnicode_DecodeASCII_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeASCII_tf))

    global __PyUnicode_DecodeCharmap_fp, __PyUnicode_DecodeCharmap_f, __PyUnicode_DecodeCharmap_tf
    __PyUnicode_DecodeCharmap_f = getattr(libpy, "PyUnicode_DecodeCharmap")
    __PyUnicode_DecodeCharmap_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeCharmap_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_void_p,ctypes.c_char_p]
    __PyUnicode_DecodeCharmap_tf.tfname = "$PyUnicode_DecodeCharmap".encode()
    __PyUnicode_DecodeCharmap_tf.type = vpiSysFunc
    __PyUnicode_DecodeCharmap_fp = tf_func_t(__PyUnicode_DecodeCharmap)
    __PyUnicode_DecodeCharmap_tf.calltf = __PyUnicode_DecodeCharmap_fp
    __PyUnicode_DecodeCharmap_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeCharmap_tf.userdata = None
    name = __PyUnicode_DecodeCharmap_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeCharmap_tf))

    global __PyUnicode_DecodeFSDefault_fp, __PyUnicode_DecodeFSDefault_f, __PyUnicode_DecodeFSDefault_tf
    __PyUnicode_DecodeFSDefault_f = getattr(libpy, "PyUnicode_DecodeFSDefault")
    __PyUnicode_DecodeFSDefault_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeFSDefault_f.argtypes = [ctypes.c_char_p]
    __PyUnicode_DecodeFSDefault_tf.tfname = "$PyUnicode_DecodeFSDefault".encode()
    __PyUnicode_DecodeFSDefault_tf.type = vpiSysFunc
    __PyUnicode_DecodeFSDefault_fp = tf_func_t(__PyUnicode_DecodeFSDefault)
    __PyUnicode_DecodeFSDefault_tf.calltf = __PyUnicode_DecodeFSDefault_fp
    __PyUnicode_DecodeFSDefault_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeFSDefault_tf.userdata = None
    name = __PyUnicode_DecodeFSDefault_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeFSDefault_tf))

    global __PyUnicode_DecodeFSDefaultAndSize_fp, __PyUnicode_DecodeFSDefaultAndSize_f, __PyUnicode_DecodeFSDefaultAndSize_tf
    __PyUnicode_DecodeFSDefaultAndSize_f = getattr(libpy, "PyUnicode_DecodeFSDefaultAndSize")
    __PyUnicode_DecodeFSDefaultAndSize_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeFSDefaultAndSize_f.argtypes = [ctypes.c_char_p,ctypes.c_uint]
    __PyUnicode_DecodeFSDefaultAndSize_tf.tfname = "$PyUnicode_DecodeFSDefaultAndSize".encode()
    __PyUnicode_DecodeFSDefaultAndSize_tf.type = vpiSysFunc
    __PyUnicode_DecodeFSDefaultAndSize_fp = tf_func_t(__PyUnicode_DecodeFSDefaultAndSize)
    __PyUnicode_DecodeFSDefaultAndSize_tf.calltf = __PyUnicode_DecodeFSDefaultAndSize_fp
    __PyUnicode_DecodeFSDefaultAndSize_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeFSDefaultAndSize_tf.userdata = None
    name = __PyUnicode_DecodeFSDefaultAndSize_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeFSDefaultAndSize_tf))

    global __PyUnicode_DecodeLatin1_fp, __PyUnicode_DecodeLatin1_f, __PyUnicode_DecodeLatin1_tf
    __PyUnicode_DecodeLatin1_f = getattr(libpy, "PyUnicode_DecodeLatin1")
    __PyUnicode_DecodeLatin1_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeLatin1_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p]
    __PyUnicode_DecodeLatin1_tf.tfname = "$PyUnicode_DecodeLatin1".encode()
    __PyUnicode_DecodeLatin1_tf.type = vpiSysFunc
    __PyUnicode_DecodeLatin1_fp = tf_func_t(__PyUnicode_DecodeLatin1)
    __PyUnicode_DecodeLatin1_tf.calltf = __PyUnicode_DecodeLatin1_fp
    __PyUnicode_DecodeLatin1_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeLatin1_tf.userdata = None
    name = __PyUnicode_DecodeLatin1_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeLatin1_tf))

    global __PyUnicode_DecodeLocale_fp, __PyUnicode_DecodeLocale_f, __PyUnicode_DecodeLocale_tf
    __PyUnicode_DecodeLocale_f = getattr(libpy, "PyUnicode_DecodeLocale")
    __PyUnicode_DecodeLocale_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeLocale_f.argtypes = [ctypes.c_char_p,ctypes.c_char_p]
    __PyUnicode_DecodeLocale_tf.tfname = "$PyUnicode_DecodeLocale".encode()
    __PyUnicode_DecodeLocale_tf.type = vpiSysFunc
    __PyUnicode_DecodeLocale_fp = tf_func_t(__PyUnicode_DecodeLocale)
    __PyUnicode_DecodeLocale_tf.calltf = __PyUnicode_DecodeLocale_fp
    __PyUnicode_DecodeLocale_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeLocale_tf.userdata = None
    name = __PyUnicode_DecodeLocale_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeLocale_tf))

    global __PyUnicode_DecodeLocaleAndSize_fp, __PyUnicode_DecodeLocaleAndSize_f, __PyUnicode_DecodeLocaleAndSize_tf
    __PyUnicode_DecodeLocaleAndSize_f = getattr(libpy, "PyUnicode_DecodeLocaleAndSize")
    __PyUnicode_DecodeLocaleAndSize_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeLocaleAndSize_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p]
    __PyUnicode_DecodeLocaleAndSize_tf.tfname = "$PyUnicode_DecodeLocaleAndSize".encode()
    __PyUnicode_DecodeLocaleAndSize_tf.type = vpiSysFunc
    __PyUnicode_DecodeLocaleAndSize_fp = tf_func_t(__PyUnicode_DecodeLocaleAndSize)
    __PyUnicode_DecodeLocaleAndSize_tf.calltf = __PyUnicode_DecodeLocaleAndSize_fp
    __PyUnicode_DecodeLocaleAndSize_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeLocaleAndSize_tf.userdata = None
    name = __PyUnicode_DecodeLocaleAndSize_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeLocaleAndSize_tf))

    global __PyUnicode_DecodeRawUnicodeEscape_fp, __PyUnicode_DecodeRawUnicodeEscape_f, __PyUnicode_DecodeRawUnicodeEscape_tf
    __PyUnicode_DecodeRawUnicodeEscape_f = getattr(libpy, "PyUnicode_DecodeRawUnicodeEscape")
    __PyUnicode_DecodeRawUnicodeEscape_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeRawUnicodeEscape_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p]
    __PyUnicode_DecodeRawUnicodeEscape_tf.tfname = "$PyUnicode_DecodeRawUnicodeEscape".encode()
    __PyUnicode_DecodeRawUnicodeEscape_tf.type = vpiSysFunc
    __PyUnicode_DecodeRawUnicodeEscape_fp = tf_func_t(__PyUnicode_DecodeRawUnicodeEscape)
    __PyUnicode_DecodeRawUnicodeEscape_tf.calltf = __PyUnicode_DecodeRawUnicodeEscape_fp
    __PyUnicode_DecodeRawUnicodeEscape_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeRawUnicodeEscape_tf.userdata = None
    name = __PyUnicode_DecodeRawUnicodeEscape_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeRawUnicodeEscape_tf))

    global __PyUnicode_DecodeUTF16_fp, __PyUnicode_DecodeUTF16_f, __PyUnicode_DecodeUTF16_tf
    __PyUnicode_DecodeUTF16_f = getattr(libpy, "PyUnicode_DecodeUTF16")
    __PyUnicode_DecodeUTF16_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeUTF16_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p,ctypes.POINTER(ctypes.c_int)]
    __PyUnicode_DecodeUTF16_tf.tfname = "$PyUnicode_DecodeUTF16".encode()
    __PyUnicode_DecodeUTF16_tf.type = vpiSysFunc
    __PyUnicode_DecodeUTF16_fp = tf_func_t(__PyUnicode_DecodeUTF16)
    __PyUnicode_DecodeUTF16_tf.calltf = __PyUnicode_DecodeUTF16_fp
    __PyUnicode_DecodeUTF16_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeUTF16_tf.userdata = None
    name = __PyUnicode_DecodeUTF16_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeUTF16_tf))

    global __PyUnicode_DecodeUTF16Stateful_fp, __PyUnicode_DecodeUTF16Stateful_f, __PyUnicode_DecodeUTF16Stateful_tf
    __PyUnicode_DecodeUTF16Stateful_f = getattr(libpy, "PyUnicode_DecodeUTF16Stateful")
    __PyUnicode_DecodeUTF16Stateful_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeUTF16Stateful_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_uint)]
    __PyUnicode_DecodeUTF16Stateful_tf.tfname = "$PyUnicode_DecodeUTF16Stateful".encode()
    __PyUnicode_DecodeUTF16Stateful_tf.type = vpiSysFunc
    __PyUnicode_DecodeUTF16Stateful_fp = tf_func_t(__PyUnicode_DecodeUTF16Stateful)
    __PyUnicode_DecodeUTF16Stateful_tf.calltf = __PyUnicode_DecodeUTF16Stateful_fp
    __PyUnicode_DecodeUTF16Stateful_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeUTF16Stateful_tf.userdata = None
    name = __PyUnicode_DecodeUTF16Stateful_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeUTF16Stateful_tf))

    global __PyUnicode_DecodeUTF32_fp, __PyUnicode_DecodeUTF32_f, __PyUnicode_DecodeUTF32_tf
    __PyUnicode_DecodeUTF32_f = getattr(libpy, "PyUnicode_DecodeUTF32")
    __PyUnicode_DecodeUTF32_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeUTF32_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p,ctypes.POINTER(ctypes.c_int)]
    __PyUnicode_DecodeUTF32_tf.tfname = "$PyUnicode_DecodeUTF32".encode()
    __PyUnicode_DecodeUTF32_tf.type = vpiSysFunc
    __PyUnicode_DecodeUTF32_fp = tf_func_t(__PyUnicode_DecodeUTF32)
    __PyUnicode_DecodeUTF32_tf.calltf = __PyUnicode_DecodeUTF32_fp
    __PyUnicode_DecodeUTF32_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeUTF32_tf.userdata = None
    name = __PyUnicode_DecodeUTF32_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeUTF32_tf))

    global __PyUnicode_DecodeUTF32Stateful_fp, __PyUnicode_DecodeUTF32Stateful_f, __PyUnicode_DecodeUTF32Stateful_tf
    __PyUnicode_DecodeUTF32Stateful_f = getattr(libpy, "PyUnicode_DecodeUTF32Stateful")
    __PyUnicode_DecodeUTF32Stateful_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeUTF32Stateful_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_uint)]
    __PyUnicode_DecodeUTF32Stateful_tf.tfname = "$PyUnicode_DecodeUTF32Stateful".encode()
    __PyUnicode_DecodeUTF32Stateful_tf.type = vpiSysFunc
    __PyUnicode_DecodeUTF32Stateful_fp = tf_func_t(__PyUnicode_DecodeUTF32Stateful)
    __PyUnicode_DecodeUTF32Stateful_tf.calltf = __PyUnicode_DecodeUTF32Stateful_fp
    __PyUnicode_DecodeUTF32Stateful_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeUTF32Stateful_tf.userdata = None
    name = __PyUnicode_DecodeUTF32Stateful_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeUTF32Stateful_tf))

    global __PyUnicode_DecodeUTF7_fp, __PyUnicode_DecodeUTF7_f, __PyUnicode_DecodeUTF7_tf
    __PyUnicode_DecodeUTF7_f = getattr(libpy, "PyUnicode_DecodeUTF7")
    __PyUnicode_DecodeUTF7_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeUTF7_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p]
    __PyUnicode_DecodeUTF7_tf.tfname = "$PyUnicode_DecodeUTF7".encode()
    __PyUnicode_DecodeUTF7_tf.type = vpiSysFunc
    __PyUnicode_DecodeUTF7_fp = tf_func_t(__PyUnicode_DecodeUTF7)
    __PyUnicode_DecodeUTF7_tf.calltf = __PyUnicode_DecodeUTF7_fp
    __PyUnicode_DecodeUTF7_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeUTF7_tf.userdata = None
    name = __PyUnicode_DecodeUTF7_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeUTF7_tf))

    global __PyUnicode_DecodeUTF7Stateful_fp, __PyUnicode_DecodeUTF7Stateful_f, __PyUnicode_DecodeUTF7Stateful_tf
    __PyUnicode_DecodeUTF7Stateful_f = getattr(libpy, "PyUnicode_DecodeUTF7Stateful")
    __PyUnicode_DecodeUTF7Stateful_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeUTF7Stateful_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p,ctypes.POINTER(ctypes.c_uint)]
    __PyUnicode_DecodeUTF7Stateful_tf.tfname = "$PyUnicode_DecodeUTF7Stateful".encode()
    __PyUnicode_DecodeUTF7Stateful_tf.type = vpiSysFunc
    __PyUnicode_DecodeUTF7Stateful_fp = tf_func_t(__PyUnicode_DecodeUTF7Stateful)
    __PyUnicode_DecodeUTF7Stateful_tf.calltf = __PyUnicode_DecodeUTF7Stateful_fp
    __PyUnicode_DecodeUTF7Stateful_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeUTF7Stateful_tf.userdata = None
    name = __PyUnicode_DecodeUTF7Stateful_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeUTF7Stateful_tf))

    global __PyUnicode_DecodeUTF8_fp, __PyUnicode_DecodeUTF8_f, __PyUnicode_DecodeUTF8_tf
    __PyUnicode_DecodeUTF8_f = getattr(libpy, "PyUnicode_DecodeUTF8")
    __PyUnicode_DecodeUTF8_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeUTF8_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p]
    __PyUnicode_DecodeUTF8_tf.tfname = "$PyUnicode_DecodeUTF8".encode()
    __PyUnicode_DecodeUTF8_tf.type = vpiSysFunc
    __PyUnicode_DecodeUTF8_fp = tf_func_t(__PyUnicode_DecodeUTF8)
    __PyUnicode_DecodeUTF8_tf.calltf = __PyUnicode_DecodeUTF8_fp
    __PyUnicode_DecodeUTF8_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeUTF8_tf.userdata = None
    name = __PyUnicode_DecodeUTF8_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeUTF8_tf))

    global __PyUnicode_DecodeUTF8Stateful_fp, __PyUnicode_DecodeUTF8Stateful_f, __PyUnicode_DecodeUTF8Stateful_tf
    __PyUnicode_DecodeUTF8Stateful_f = getattr(libpy, "PyUnicode_DecodeUTF8Stateful")
    __PyUnicode_DecodeUTF8Stateful_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeUTF8Stateful_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p,ctypes.POINTER(ctypes.c_uint)]
    __PyUnicode_DecodeUTF8Stateful_tf.tfname = "$PyUnicode_DecodeUTF8Stateful".encode()
    __PyUnicode_DecodeUTF8Stateful_tf.type = vpiSysFunc
    __PyUnicode_DecodeUTF8Stateful_fp = tf_func_t(__PyUnicode_DecodeUTF8Stateful)
    __PyUnicode_DecodeUTF8Stateful_tf.calltf = __PyUnicode_DecodeUTF8Stateful_fp
    __PyUnicode_DecodeUTF8Stateful_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeUTF8Stateful_tf.userdata = None
    name = __PyUnicode_DecodeUTF8Stateful_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeUTF8Stateful_tf))

    global __PyUnicode_DecodeUnicodeEscape_fp, __PyUnicode_DecodeUnicodeEscape_f, __PyUnicode_DecodeUnicodeEscape_tf
    __PyUnicode_DecodeUnicodeEscape_f = getattr(libpy, "PyUnicode_DecodeUnicodeEscape")
    __PyUnicode_DecodeUnicodeEscape_f.restype = ctypes.c_void_p
    __PyUnicode_DecodeUnicodeEscape_f.argtypes = [ctypes.c_char_p,ctypes.c_uint,ctypes.c_char_p]
    __PyUnicode_DecodeUnicodeEscape_tf.tfname = "$PyUnicode_DecodeUnicodeEscape".encode()
    __PyUnicode_DecodeUnicodeEscape_tf.type = vpiSysFunc
    __PyUnicode_DecodeUnicodeEscape_fp = tf_func_t(__PyUnicode_DecodeUnicodeEscape)
    __PyUnicode_DecodeUnicodeEscape_tf.calltf = __PyUnicode_DecodeUnicodeEscape_fp
    __PyUnicode_DecodeUnicodeEscape_tf.sizetf = sizetf64_fp
    __PyUnicode_DecodeUnicodeEscape_tf.userdata = None
    name = __PyUnicode_DecodeUnicodeEscape_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_DecodeUnicodeEscape_tf))

    global __PyUnicode_EncodeFSDefault_fp, __PyUnicode_EncodeFSDefault_f, __PyUnicode_EncodeFSDefault_tf
    __PyUnicode_EncodeFSDefault_f = getattr(libpy, "PyUnicode_EncodeFSDefault")
    __PyUnicode_EncodeFSDefault_f.restype = ctypes.c_void_p
    __PyUnicode_EncodeFSDefault_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_EncodeFSDefault_tf.tfname = "$PyUnicode_EncodeFSDefault".encode()
    __PyUnicode_EncodeFSDefault_tf.type = vpiSysFunc
    __PyUnicode_EncodeFSDefault_fp = tf_func_t(__PyUnicode_EncodeFSDefault)
    __PyUnicode_EncodeFSDefault_tf.calltf = __PyUnicode_EncodeFSDefault_fp
    __PyUnicode_EncodeFSDefault_tf.sizetf = sizetf64_fp
    __PyUnicode_EncodeFSDefault_tf.userdata = None
    name = __PyUnicode_EncodeFSDefault_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_EncodeFSDefault_tf))

    global __PyUnicode_EncodeLocale_fp, __PyUnicode_EncodeLocale_f, __PyUnicode_EncodeLocale_tf
    __PyUnicode_EncodeLocale_f = getattr(libpy, "PyUnicode_EncodeLocale")
    __PyUnicode_EncodeLocale_f.restype = ctypes.c_void_p
    __PyUnicode_EncodeLocale_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
    __PyUnicode_EncodeLocale_tf.tfname = "$PyUnicode_EncodeLocale".encode()
    __PyUnicode_EncodeLocale_tf.type = vpiSysFunc
    __PyUnicode_EncodeLocale_fp = tf_func_t(__PyUnicode_EncodeLocale)
    __PyUnicode_EncodeLocale_tf.calltf = __PyUnicode_EncodeLocale_fp
    __PyUnicode_EncodeLocale_tf.sizetf = sizetf64_fp
    __PyUnicode_EncodeLocale_tf.userdata = None
    name = __PyUnicode_EncodeLocale_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_EncodeLocale_tf))

    global __PyUnicode_FSConverter_fp, __PyUnicode_FSConverter_f, __PyUnicode_FSConverter_tf
    __PyUnicode_FSConverter_f = getattr(libpy, "PyUnicode_FSConverter")
    __PyUnicode_FSConverter_f.restype = ctypes.c_int
    __PyUnicode_FSConverter_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_FSConverter_tf.tfname = "$PyUnicode_FSConverter".encode()
    __PyUnicode_FSConverter_tf.type = vpiSysFunc
    __PyUnicode_FSConverter_fp = tf_func_t(__PyUnicode_FSConverter)
    __PyUnicode_FSConverter_tf.calltf = __PyUnicode_FSConverter_fp
    __PyUnicode_FSConverter_tf.userdata = None
    name = __PyUnicode_FSConverter_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_FSConverter_tf))

    global __PyUnicode_FSDecoder_fp, __PyUnicode_FSDecoder_f, __PyUnicode_FSDecoder_tf
    __PyUnicode_FSDecoder_f = getattr(libpy, "PyUnicode_FSDecoder")
    __PyUnicode_FSDecoder_f.restype = ctypes.c_int
    __PyUnicode_FSDecoder_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_FSDecoder_tf.tfname = "$PyUnicode_FSDecoder".encode()
    __PyUnicode_FSDecoder_tf.type = vpiSysFunc
    __PyUnicode_FSDecoder_fp = tf_func_t(__PyUnicode_FSDecoder)
    __PyUnicode_FSDecoder_tf.calltf = __PyUnicode_FSDecoder_fp
    __PyUnicode_FSDecoder_tf.userdata = None
    name = __PyUnicode_FSDecoder_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_FSDecoder_tf))

    global __PyUnicode_Find_fp, __PyUnicode_Find_f, __PyUnicode_Find_tf
    __PyUnicode_Find_f = getattr(libpy, "PyUnicode_Find")
    __PyUnicode_Find_f.restype = ctypes.c_uint
    __PyUnicode_Find_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_uint,ctypes.c_uint,ctypes.c_int]
    __PyUnicode_Find_tf.tfname = "$PyUnicode_Find".encode()
    __PyUnicode_Find_tf.type = vpiSysFunc
    __PyUnicode_Find_fp = tf_func_t(__PyUnicode_Find)
    __PyUnicode_Find_tf.calltf = __PyUnicode_Find_fp
    __PyUnicode_Find_tf.userdata = None
    name = __PyUnicode_Find_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Find_tf))

    global __PyUnicode_Format_fp, __PyUnicode_Format_f, __PyUnicode_Format_tf
    __PyUnicode_Format_f = getattr(libpy, "PyUnicode_Format")
    __PyUnicode_Format_f.restype = ctypes.c_void_p
    __PyUnicode_Format_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_Format_tf.tfname = "$PyUnicode_Format".encode()
    __PyUnicode_Format_tf.type = vpiSysFunc
    __PyUnicode_Format_fp = tf_func_t(__PyUnicode_Format)
    __PyUnicode_Format_tf.calltf = __PyUnicode_Format_fp
    __PyUnicode_Format_tf.sizetf = sizetf64_fp
    __PyUnicode_Format_tf.userdata = None
    name = __PyUnicode_Format_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Format_tf))

    global __PyUnicode_FromEncodedObject_fp, __PyUnicode_FromEncodedObject_f, __PyUnicode_FromEncodedObject_tf
    __PyUnicode_FromEncodedObject_f = getattr(libpy, "PyUnicode_FromEncodedObject")
    __PyUnicode_FromEncodedObject_f.restype = ctypes.c_void_p
    __PyUnicode_FromEncodedObject_f.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
    __PyUnicode_FromEncodedObject_tf.tfname = "$PyUnicode_FromEncodedObject".encode()
    __PyUnicode_FromEncodedObject_tf.type = vpiSysFunc
    __PyUnicode_FromEncodedObject_fp = tf_func_t(__PyUnicode_FromEncodedObject)
    __PyUnicode_FromEncodedObject_tf.calltf = __PyUnicode_FromEncodedObject_fp
    __PyUnicode_FromEncodedObject_tf.sizetf = sizetf64_fp
    __PyUnicode_FromEncodedObject_tf.userdata = None
    name = __PyUnicode_FromEncodedObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_FromEncodedObject_tf))

    global __PyUnicode_FromObject_fp, __PyUnicode_FromObject_f, __PyUnicode_FromObject_tf
    __PyUnicode_FromObject_f = getattr(libpy, "PyUnicode_FromObject")
    __PyUnicode_FromObject_f.restype = ctypes.c_void_p
    __PyUnicode_FromObject_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_FromObject_tf.tfname = "$PyUnicode_FromObject".encode()
    __PyUnicode_FromObject_tf.type = vpiSysFunc
    __PyUnicode_FromObject_fp = tf_func_t(__PyUnicode_FromObject)
    __PyUnicode_FromObject_tf.calltf = __PyUnicode_FromObject_fp
    __PyUnicode_FromObject_tf.sizetf = sizetf64_fp
    __PyUnicode_FromObject_tf.userdata = None
    name = __PyUnicode_FromObject_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_FromObject_tf))

    global __PyUnicode_FromOrdinal_fp, __PyUnicode_FromOrdinal_f, __PyUnicode_FromOrdinal_tf
    __PyUnicode_FromOrdinal_f = getattr(libpy, "PyUnicode_FromOrdinal")
    __PyUnicode_FromOrdinal_f.restype = ctypes.c_void_p
    __PyUnicode_FromOrdinal_f.argtypes = [ctypes.c_int]
    __PyUnicode_FromOrdinal_tf.tfname = "$PyUnicode_FromOrdinal".encode()
    __PyUnicode_FromOrdinal_tf.type = vpiSysFunc
    __PyUnicode_FromOrdinal_fp = tf_func_t(__PyUnicode_FromOrdinal)
    __PyUnicode_FromOrdinal_tf.calltf = __PyUnicode_FromOrdinal_fp
    __PyUnicode_FromOrdinal_tf.sizetf = sizetf64_fp
    __PyUnicode_FromOrdinal_tf.userdata = None
    name = __PyUnicode_FromOrdinal_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_FromOrdinal_tf))

    global __PyUnicode_FromString_fp, __PyUnicode_FromString_f, __PyUnicode_FromString_tf
    __PyUnicode_FromString_f = getattr(libpy, "PyUnicode_FromString")
    __PyUnicode_FromString_f.restype = ctypes.c_void_p
    __PyUnicode_FromString_f.argtypes = [ctypes.c_char_p]
    __PyUnicode_FromString_tf.tfname = "$PyUnicode_FromString".encode()
    __PyUnicode_FromString_tf.type = vpiSysFunc
    __PyUnicode_FromString_fp = tf_func_t(__PyUnicode_FromString)
    __PyUnicode_FromString_tf.calltf = __PyUnicode_FromString_fp
    __PyUnicode_FromString_tf.sizetf = sizetf64_fp
    __PyUnicode_FromString_tf.userdata = None
    name = __PyUnicode_FromString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_FromString_tf))

    global __PyUnicode_FromStringAndSize_fp, __PyUnicode_FromStringAndSize_f, __PyUnicode_FromStringAndSize_tf
    __PyUnicode_FromStringAndSize_f = getattr(libpy, "PyUnicode_FromStringAndSize")
    __PyUnicode_FromStringAndSize_f.restype = ctypes.c_void_p
    __PyUnicode_FromStringAndSize_f.argtypes = [ctypes.c_char_p,ctypes.c_uint]
    __PyUnicode_FromStringAndSize_tf.tfname = "$PyUnicode_FromStringAndSize".encode()
    __PyUnicode_FromStringAndSize_tf.type = vpiSysFunc
    __PyUnicode_FromStringAndSize_fp = tf_func_t(__PyUnicode_FromStringAndSize)
    __PyUnicode_FromStringAndSize_tf.calltf = __PyUnicode_FromStringAndSize_fp
    __PyUnicode_FromStringAndSize_tf.sizetf = sizetf64_fp
    __PyUnicode_FromStringAndSize_tf.userdata = None
    name = __PyUnicode_FromStringAndSize_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_FromStringAndSize_tf))

    global __PyUnicode_GetDefaultEncoding_fp, __PyUnicode_GetDefaultEncoding_f, __PyUnicode_GetDefaultEncoding_tf
    __PyUnicode_GetDefaultEncoding_f = getattr(libpy, "PyUnicode_GetDefaultEncoding")
    __PyUnicode_GetDefaultEncoding_f.restype = ctypes.c_char_p
    __PyUnicode_GetDefaultEncoding_f.argtypes = []
    __PyUnicode_GetDefaultEncoding_tf.tfname = "$PyUnicode_GetDefaultEncoding".encode()
    __PyUnicode_GetDefaultEncoding_tf.type = vpiSysTask
    __PyUnicode_GetDefaultEncoding_fp = tf_func_t(__PyUnicode_GetDefaultEncoding)
    __PyUnicode_GetDefaultEncoding_tf.calltf = __PyUnicode_GetDefaultEncoding_fp
    __PyUnicode_GetDefaultEncoding_tf.userdata = None
    name = __PyUnicode_GetDefaultEncoding_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_GetDefaultEncoding_tf))

    global __PyUnicode_GetLength_fp, __PyUnicode_GetLength_f, __PyUnicode_GetLength_tf
    __PyUnicode_GetLength_f = getattr(libpy, "PyUnicode_GetLength")
    __PyUnicode_GetLength_f.restype = ctypes.c_uint
    __PyUnicode_GetLength_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_GetLength_tf.tfname = "$PyUnicode_GetLength".encode()
    __PyUnicode_GetLength_tf.type = vpiSysFunc
    __PyUnicode_GetLength_fp = tf_func_t(__PyUnicode_GetLength)
    __PyUnicode_GetLength_tf.calltf = __PyUnicode_GetLength_fp
    __PyUnicode_GetLength_tf.userdata = None
    name = __PyUnicode_GetLength_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_GetLength_tf))

    global __PyUnicode_GetSize_fp, __PyUnicode_GetSize_f, __PyUnicode_GetSize_tf
    __PyUnicode_GetSize_f = getattr(libpy, "PyUnicode_GetSize")
    __PyUnicode_GetSize_f.restype = ctypes.c_uint
    __PyUnicode_GetSize_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_GetSize_tf.tfname = "$PyUnicode_GetSize".encode()
    __PyUnicode_GetSize_tf.type = vpiSysFunc
    __PyUnicode_GetSize_fp = tf_func_t(__PyUnicode_GetSize)
    __PyUnicode_GetSize_tf.calltf = __PyUnicode_GetSize_fp
    __PyUnicode_GetSize_tf.userdata = None
    name = __PyUnicode_GetSize_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_GetSize_tf))

    global __PyUnicode_InternFromString_fp, __PyUnicode_InternFromString_f, __PyUnicode_InternFromString_tf
    __PyUnicode_InternFromString_f = getattr(libpy, "PyUnicode_InternFromString")
    __PyUnicode_InternFromString_f.restype = ctypes.c_void_p
    __PyUnicode_InternFromString_f.argtypes = [ctypes.c_char_p]
    __PyUnicode_InternFromString_tf.tfname = "$PyUnicode_InternFromString".encode()
    __PyUnicode_InternFromString_tf.type = vpiSysFunc
    __PyUnicode_InternFromString_fp = tf_func_t(__PyUnicode_InternFromString)
    __PyUnicode_InternFromString_tf.calltf = __PyUnicode_InternFromString_fp
    __PyUnicode_InternFromString_tf.sizetf = sizetf64_fp
    __PyUnicode_InternFromString_tf.userdata = None
    name = __PyUnicode_InternFromString_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_InternFromString_tf))

    global __PyUnicode_IsIdentifier_fp, __PyUnicode_IsIdentifier_f, __PyUnicode_IsIdentifier_tf
    __PyUnicode_IsIdentifier_f = getattr(libpy, "PyUnicode_IsIdentifier")
    __PyUnicode_IsIdentifier_f.restype = ctypes.c_int
    __PyUnicode_IsIdentifier_f.argtypes = [ctypes.c_void_p]
    __PyUnicode_IsIdentifier_tf.tfname = "$PyUnicode_IsIdentifier".encode()
    __PyUnicode_IsIdentifier_tf.type = vpiSysFunc
    __PyUnicode_IsIdentifier_fp = tf_func_t(__PyUnicode_IsIdentifier)
    __PyUnicode_IsIdentifier_tf.calltf = __PyUnicode_IsIdentifier_fp
    __PyUnicode_IsIdentifier_tf.userdata = None
    name = __PyUnicode_IsIdentifier_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_IsIdentifier_tf))

    global __PyUnicode_Join_fp, __PyUnicode_Join_f, __PyUnicode_Join_tf
    __PyUnicode_Join_f = getattr(libpy, "PyUnicode_Join")
    __PyUnicode_Join_f.restype = ctypes.c_void_p
    __PyUnicode_Join_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_Join_tf.tfname = "$PyUnicode_Join".encode()
    __PyUnicode_Join_tf.type = vpiSysFunc
    __PyUnicode_Join_fp = tf_func_t(__PyUnicode_Join)
    __PyUnicode_Join_tf.calltf = __PyUnicode_Join_fp
    __PyUnicode_Join_tf.sizetf = sizetf64_fp
    __PyUnicode_Join_tf.userdata = None
    name = __PyUnicode_Join_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Join_tf))

    global __PyUnicode_Partition_fp, __PyUnicode_Partition_f, __PyUnicode_Partition_tf
    __PyUnicode_Partition_f = getattr(libpy, "PyUnicode_Partition")
    __PyUnicode_Partition_f.restype = ctypes.c_void_p
    __PyUnicode_Partition_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_Partition_tf.tfname = "$PyUnicode_Partition".encode()
    __PyUnicode_Partition_tf.type = vpiSysFunc
    __PyUnicode_Partition_fp = tf_func_t(__PyUnicode_Partition)
    __PyUnicode_Partition_tf.calltf = __PyUnicode_Partition_fp
    __PyUnicode_Partition_tf.sizetf = sizetf64_fp
    __PyUnicode_Partition_tf.userdata = None
    name = __PyUnicode_Partition_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Partition_tf))

    global __PyUnicode_RPartition_fp, __PyUnicode_RPartition_f, __PyUnicode_RPartition_tf
    __PyUnicode_RPartition_f = getattr(libpy, "PyUnicode_RPartition")
    __PyUnicode_RPartition_f.restype = ctypes.c_void_p
    __PyUnicode_RPartition_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __PyUnicode_RPartition_tf.tfname = "$PyUnicode_RPartition".encode()
    __PyUnicode_RPartition_tf.type = vpiSysFunc
    __PyUnicode_RPartition_fp = tf_func_t(__PyUnicode_RPartition)
    __PyUnicode_RPartition_tf.calltf = __PyUnicode_RPartition_fp
    __PyUnicode_RPartition_tf.sizetf = sizetf64_fp
    __PyUnicode_RPartition_tf.userdata = None
    name = __PyUnicode_RPartition_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_RPartition_tf))

    global __PyUnicode_RSplit_fp, __PyUnicode_RSplit_f, __PyUnicode_RSplit_tf
    __PyUnicode_RSplit_f = getattr(libpy, "PyUnicode_RSplit")
    __PyUnicode_RSplit_f.restype = ctypes.c_void_p
    __PyUnicode_RSplit_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_uint]
    __PyUnicode_RSplit_tf.tfname = "$PyUnicode_RSplit".encode()
    __PyUnicode_RSplit_tf.type = vpiSysFunc
    __PyUnicode_RSplit_fp = tf_func_t(__PyUnicode_RSplit)
    __PyUnicode_RSplit_tf.calltf = __PyUnicode_RSplit_fp
    __PyUnicode_RSplit_tf.sizetf = sizetf64_fp
    __PyUnicode_RSplit_tf.userdata = None
    name = __PyUnicode_RSplit_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_RSplit_tf))

    global __PyUnicode_Replace_fp, __PyUnicode_Replace_f, __PyUnicode_Replace_tf
    __PyUnicode_Replace_f = getattr(libpy, "PyUnicode_Replace")
    __PyUnicode_Replace_f.restype = ctypes.c_void_p
    __PyUnicode_Replace_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_uint]
    __PyUnicode_Replace_tf.tfname = "$PyUnicode_Replace".encode()
    __PyUnicode_Replace_tf.type = vpiSysFunc
    __PyUnicode_Replace_fp = tf_func_t(__PyUnicode_Replace)
    __PyUnicode_Replace_tf.calltf = __PyUnicode_Replace_fp
    __PyUnicode_Replace_tf.sizetf = sizetf64_fp
    __PyUnicode_Replace_tf.userdata = None
    name = __PyUnicode_Replace_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Replace_tf))

    global __PyUnicode_RichCompare_fp, __PyUnicode_RichCompare_f, __PyUnicode_RichCompare_tf
    __PyUnicode_RichCompare_f = getattr(libpy, "PyUnicode_RichCompare")
    __PyUnicode_RichCompare_f.restype = ctypes.c_void_p
    __PyUnicode_RichCompare_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
    __PyUnicode_RichCompare_tf.tfname = "$PyUnicode_RichCompare".encode()
    __PyUnicode_RichCompare_tf.type = vpiSysFunc
    __PyUnicode_RichCompare_fp = tf_func_t(__PyUnicode_RichCompare)
    __PyUnicode_RichCompare_tf.calltf = __PyUnicode_RichCompare_fp
    __PyUnicode_RichCompare_tf.sizetf = sizetf64_fp
    __PyUnicode_RichCompare_tf.userdata = None
    name = __PyUnicode_RichCompare_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_RichCompare_tf))

    global __PyUnicode_Split_fp, __PyUnicode_Split_f, __PyUnicode_Split_tf
    __PyUnicode_Split_f = getattr(libpy, "PyUnicode_Split")
    __PyUnicode_Split_f.restype = ctypes.c_void_p
    __PyUnicode_Split_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_uint]
    __PyUnicode_Split_tf.tfname = "$PyUnicode_Split".encode()
    __PyUnicode_Split_tf.type = vpiSysFunc
    __PyUnicode_Split_fp = tf_func_t(__PyUnicode_Split)
    __PyUnicode_Split_tf.calltf = __PyUnicode_Split_fp
    __PyUnicode_Split_tf.sizetf = sizetf64_fp
    __PyUnicode_Split_tf.userdata = None
    name = __PyUnicode_Split_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Split_tf))

    global __PyUnicode_Splitlines_fp, __PyUnicode_Splitlines_f, __PyUnicode_Splitlines_tf
    __PyUnicode_Splitlines_f = getattr(libpy, "PyUnicode_Splitlines")
    __PyUnicode_Splitlines_f.restype = ctypes.c_void_p
    __PyUnicode_Splitlines_f.argtypes = [ctypes.c_void_p,ctypes.c_int]
    __PyUnicode_Splitlines_tf.tfname = "$PyUnicode_Splitlines".encode()
    __PyUnicode_Splitlines_tf.type = vpiSysFunc
    __PyUnicode_Splitlines_fp = tf_func_t(__PyUnicode_Splitlines)
    __PyUnicode_Splitlines_tf.calltf = __PyUnicode_Splitlines_fp
    __PyUnicode_Splitlines_tf.sizetf = sizetf64_fp
    __PyUnicode_Splitlines_tf.userdata = None
    name = __PyUnicode_Splitlines_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Splitlines_tf))

    global __PyUnicode_Substring_fp, __PyUnicode_Substring_f, __PyUnicode_Substring_tf
    __PyUnicode_Substring_f = getattr(libpy, "PyUnicode_Substring")
    __PyUnicode_Substring_f.restype = ctypes.c_void_p
    __PyUnicode_Substring_f.argtypes = [ctypes.c_void_p,ctypes.c_uint,ctypes.c_uint]
    __PyUnicode_Substring_tf.tfname = "$PyUnicode_Substring".encode()
    __PyUnicode_Substring_tf.type = vpiSysFunc
    __PyUnicode_Substring_fp = tf_func_t(__PyUnicode_Substring)
    __PyUnicode_Substring_tf.calltf = __PyUnicode_Substring_fp
    __PyUnicode_Substring_tf.sizetf = sizetf64_fp
    __PyUnicode_Substring_tf.userdata = None
    name = __PyUnicode_Substring_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Substring_tf))

    global __PyUnicode_Tailmatch_fp, __PyUnicode_Tailmatch_f, __PyUnicode_Tailmatch_tf
    __PyUnicode_Tailmatch_f = getattr(libpy, "PyUnicode_Tailmatch")
    __PyUnicode_Tailmatch_f.restype = ctypes.c_uint
    __PyUnicode_Tailmatch_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_uint,ctypes.c_uint,ctypes.c_int]
    __PyUnicode_Tailmatch_tf.tfname = "$PyUnicode_Tailmatch".encode()
    __PyUnicode_Tailmatch_tf.type = vpiSysFunc
    __PyUnicode_Tailmatch_fp = tf_func_t(__PyUnicode_Tailmatch)
    __PyUnicode_Tailmatch_tf.calltf = __PyUnicode_Tailmatch_fp
    __PyUnicode_Tailmatch_tf.userdata = None
    name = __PyUnicode_Tailmatch_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Tailmatch_tf))

    global __PyUnicode_Translate_fp, __PyUnicode_Translate_f, __PyUnicode_Translate_tf
    __PyUnicode_Translate_f = getattr(libpy, "PyUnicode_Translate")
    __PyUnicode_Translate_f.restype = ctypes.c_void_p
    __PyUnicode_Translate_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    __PyUnicode_Translate_tf.tfname = "$PyUnicode_Translate".encode()
    __PyUnicode_Translate_tf.type = vpiSysFunc
    __PyUnicode_Translate_fp = tf_func_t(__PyUnicode_Translate)
    __PyUnicode_Translate_tf.calltf = __PyUnicode_Translate_fp
    __PyUnicode_Translate_tf.sizetf = sizetf64_fp
    __PyUnicode_Translate_tf.userdata = None
    name = __PyUnicode_Translate_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__PyUnicode_Translate_tf))

    global __Py_DecRef_fp, __Py_DecRef_f, __Py_DecRef_tf
    __Py_DecRef_f = getattr(libpy, "Py_DecRef")
    __Py_DecRef_f.restype = None
    __Py_DecRef_f.argtypes = [ctypes.c_void_p]
    __Py_DecRef_tf.tfname = "$Py_DecRef".encode()
    __Py_DecRef_tf.type = vpiSysTask
    __Py_DecRef_fp = tf_func_t(__Py_DecRef)
    __Py_DecRef_tf.calltf = __Py_DecRef_fp
    __Py_DecRef_tf.userdata = None
    name = __Py_DecRef_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_DecRef_tf))

    global __Py_EnterRecursiveCall_fp, __Py_EnterRecursiveCall_f, __Py_EnterRecursiveCall_tf
    __Py_EnterRecursiveCall_f = getattr(libpy, "Py_EnterRecursiveCall")
    __Py_EnterRecursiveCall_f.restype = ctypes.c_int
    __Py_EnterRecursiveCall_f.argtypes = [ctypes.c_char_p]
    __Py_EnterRecursiveCall_tf.tfname = "$Py_EnterRecursiveCall".encode()
    __Py_EnterRecursiveCall_tf.type = vpiSysFunc
    __Py_EnterRecursiveCall_fp = tf_func_t(__Py_EnterRecursiveCall)
    __Py_EnterRecursiveCall_tf.calltf = __Py_EnterRecursiveCall_fp
    __Py_EnterRecursiveCall_tf.userdata = None
    name = __Py_EnterRecursiveCall_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_EnterRecursiveCall_tf))

    global __Py_Finalize_fp, __Py_Finalize_f, __Py_Finalize_tf
    __Py_Finalize_f = getattr(libpy, "Py_Finalize")
    __Py_Finalize_f.restype = None
    __Py_Finalize_f.argtypes = []
    __Py_Finalize_tf.tfname = "$Py_Finalize".encode()
    __Py_Finalize_tf.type = vpiSysTask
    __Py_Finalize_fp = tf_func_t(__Py_Finalize)
    __Py_Finalize_tf.calltf = __Py_Finalize_fp
    __Py_Finalize_tf.userdata = None
    name = __Py_Finalize_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_Finalize_tf))

    global __Py_FinalizeEx_fp, __Py_FinalizeEx_f, __Py_FinalizeEx_tf
    __Py_FinalizeEx_f = getattr(libpy, "Py_FinalizeEx")
    __Py_FinalizeEx_f.restype = ctypes.c_int
    __Py_FinalizeEx_f.argtypes = []
    __Py_FinalizeEx_tf.tfname = "$Py_FinalizeEx".encode()
    __Py_FinalizeEx_tf.type = vpiSysFunc
    __Py_FinalizeEx_fp = tf_func_t(__Py_FinalizeEx)
    __Py_FinalizeEx_tf.calltf = __Py_FinalizeEx_fp
    __Py_FinalizeEx_tf.userdata = None
    name = __Py_FinalizeEx_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_FinalizeEx_tf))

    global __Py_GenericAlias_fp, __Py_GenericAlias_f, __Py_GenericAlias_tf
    __Py_GenericAlias_f = getattr(libpy, "Py_GenericAlias")
    __Py_GenericAlias_f.restype = ctypes.c_void_p
    __Py_GenericAlias_f.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
    __Py_GenericAlias_tf.tfname = "$Py_GenericAlias".encode()
    __Py_GenericAlias_tf.type = vpiSysFunc
    __Py_GenericAlias_fp = tf_func_t(__Py_GenericAlias)
    __Py_GenericAlias_tf.calltf = __Py_GenericAlias_fp
    __Py_GenericAlias_tf.sizetf = sizetf64_fp
    __Py_GenericAlias_tf.userdata = None
    name = __Py_GenericAlias_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GenericAlias_tf))

    global __Py_GetBuildInfo_fp, __Py_GetBuildInfo_f, __Py_GetBuildInfo_tf
    __Py_GetBuildInfo_f = getattr(libpy, "Py_GetBuildInfo")
    __Py_GetBuildInfo_f.restype = ctypes.c_char_p
    __Py_GetBuildInfo_f.argtypes = []
    __Py_GetBuildInfo_tf.tfname = "$Py_GetBuildInfo".encode()
    __Py_GetBuildInfo_tf.type = vpiSysTask
    __Py_GetBuildInfo_fp = tf_func_t(__Py_GetBuildInfo)
    __Py_GetBuildInfo_tf.calltf = __Py_GetBuildInfo_fp
    __Py_GetBuildInfo_tf.userdata = None
    name = __Py_GetBuildInfo_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetBuildInfo_tf))

    global __Py_GetCompiler_fp, __Py_GetCompiler_f, __Py_GetCompiler_tf
    __Py_GetCompiler_f = getattr(libpy, "Py_GetCompiler")
    __Py_GetCompiler_f.restype = ctypes.c_char_p
    __Py_GetCompiler_f.argtypes = []
    __Py_GetCompiler_tf.tfname = "$Py_GetCompiler".encode()
    __Py_GetCompiler_tf.type = vpiSysTask
    __Py_GetCompiler_fp = tf_func_t(__Py_GetCompiler)
    __Py_GetCompiler_tf.calltf = __Py_GetCompiler_fp
    __Py_GetCompiler_tf.userdata = None
    name = __Py_GetCompiler_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetCompiler_tf))

    global __Py_GetCopyright_fp, __Py_GetCopyright_f, __Py_GetCopyright_tf
    __Py_GetCopyright_f = getattr(libpy, "Py_GetCopyright")
    __Py_GetCopyright_f.restype = ctypes.c_char_p
    __Py_GetCopyright_f.argtypes = []
    __Py_GetCopyright_tf.tfname = "$Py_GetCopyright".encode()
    __Py_GetCopyright_tf.type = vpiSysTask
    __Py_GetCopyright_fp = tf_func_t(__Py_GetCopyright)
    __Py_GetCopyright_tf.calltf = __Py_GetCopyright_fp
    __Py_GetCopyright_tf.userdata = None
    name = __Py_GetCopyright_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetCopyright_tf))

    global __Py_GetExecPrefix_fp, __Py_GetExecPrefix_f, __Py_GetExecPrefix_tf
    __Py_GetExecPrefix_f = getattr(libpy, "Py_GetExecPrefix")
    __Py_GetExecPrefix_f.restype = ctypes.c_char_p
    __Py_GetExecPrefix_f.argtypes = []
    __Py_GetExecPrefix_tf.tfname = "$Py_GetExecPrefix".encode()
    __Py_GetExecPrefix_tf.type = vpiSysTask
    __Py_GetExecPrefix_fp = tf_func_t(__Py_GetExecPrefix)
    __Py_GetExecPrefix_tf.calltf = __Py_GetExecPrefix_fp
    __Py_GetExecPrefix_tf.userdata = None
    name = __Py_GetExecPrefix_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetExecPrefix_tf))

    global __Py_GetPath_fp, __Py_GetPath_f, __Py_GetPath_tf
    __Py_GetPath_f = getattr(libpy, "Py_GetPath")
    __Py_GetPath_f.restype = ctypes.c_char_p
    __Py_GetPath_f.argtypes = []
    __Py_GetPath_tf.tfname = "$Py_GetPath".encode()
    __Py_GetPath_tf.type = vpiSysTask
    __Py_GetPath_fp = tf_func_t(__Py_GetPath)
    __Py_GetPath_tf.calltf = __Py_GetPath_fp
    __Py_GetPath_tf.userdata = None
    name = __Py_GetPath_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetPath_tf))

    global __Py_GetPlatform_fp, __Py_GetPlatform_f, __Py_GetPlatform_tf
    __Py_GetPlatform_f = getattr(libpy, "Py_GetPlatform")
    __Py_GetPlatform_f.restype = ctypes.c_char_p
    __Py_GetPlatform_f.argtypes = []
    __Py_GetPlatform_tf.tfname = "$Py_GetPlatform".encode()
    __Py_GetPlatform_tf.type = vpiSysTask
    __Py_GetPlatform_fp = tf_func_t(__Py_GetPlatform)
    __Py_GetPlatform_tf.calltf = __Py_GetPlatform_fp
    __Py_GetPlatform_tf.userdata = None
    name = __Py_GetPlatform_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetPlatform_tf))

    global __Py_GetPrefix_fp, __Py_GetPrefix_f, __Py_GetPrefix_tf
    __Py_GetPrefix_f = getattr(libpy, "Py_GetPrefix")
    __Py_GetPrefix_f.restype = ctypes.c_char_p
    __Py_GetPrefix_f.argtypes = []
    __Py_GetPrefix_tf.tfname = "$Py_GetPrefix".encode()
    __Py_GetPrefix_tf.type = vpiSysTask
    __Py_GetPrefix_fp = tf_func_t(__Py_GetPrefix)
    __Py_GetPrefix_tf.calltf = __Py_GetPrefix_fp
    __Py_GetPrefix_tf.userdata = None
    name = __Py_GetPrefix_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetPrefix_tf))

    global __Py_GetProgramFullPath_fp, __Py_GetProgramFullPath_f, __Py_GetProgramFullPath_tf
    __Py_GetProgramFullPath_f = getattr(libpy, "Py_GetProgramFullPath")
    __Py_GetProgramFullPath_f.restype = ctypes.c_char_p
    __Py_GetProgramFullPath_f.argtypes = []
    __Py_GetProgramFullPath_tf.tfname = "$Py_GetProgramFullPath".encode()
    __Py_GetProgramFullPath_tf.type = vpiSysTask
    __Py_GetProgramFullPath_fp = tf_func_t(__Py_GetProgramFullPath)
    __Py_GetProgramFullPath_tf.calltf = __Py_GetProgramFullPath_fp
    __Py_GetProgramFullPath_tf.userdata = None
    name = __Py_GetProgramFullPath_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetProgramFullPath_tf))

    global __Py_GetProgramName_fp, __Py_GetProgramName_f, __Py_GetProgramName_tf
    __Py_GetProgramName_f = getattr(libpy, "Py_GetProgramName")
    __Py_GetProgramName_f.restype = ctypes.c_char_p
    __Py_GetProgramName_f.argtypes = []
    __Py_GetProgramName_tf.tfname = "$Py_GetProgramName".encode()
    __Py_GetProgramName_tf.type = vpiSysTask
    __Py_GetProgramName_fp = tf_func_t(__Py_GetProgramName)
    __Py_GetProgramName_tf.calltf = __Py_GetProgramName_fp
    __Py_GetProgramName_tf.userdata = None
    name = __Py_GetProgramName_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetProgramName_tf))

    global __Py_GetPythonHome_fp, __Py_GetPythonHome_f, __Py_GetPythonHome_tf
    __Py_GetPythonHome_f = getattr(libpy, "Py_GetPythonHome")
    __Py_GetPythonHome_f.restype = ctypes.c_char_p
    __Py_GetPythonHome_f.argtypes = []
    __Py_GetPythonHome_tf.tfname = "$Py_GetPythonHome".encode()
    __Py_GetPythonHome_tf.type = vpiSysTask
    __Py_GetPythonHome_fp = tf_func_t(__Py_GetPythonHome)
    __Py_GetPythonHome_tf.calltf = __Py_GetPythonHome_fp
    __Py_GetPythonHome_tf.userdata = None
    name = __Py_GetPythonHome_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetPythonHome_tf))

    global __Py_GetRecursionLimit_fp, __Py_GetRecursionLimit_f, __Py_GetRecursionLimit_tf
    __Py_GetRecursionLimit_f = getattr(libpy, "Py_GetRecursionLimit")
    __Py_GetRecursionLimit_f.restype = ctypes.c_int
    __Py_GetRecursionLimit_f.argtypes = []
    __Py_GetRecursionLimit_tf.tfname = "$Py_GetRecursionLimit".encode()
    __Py_GetRecursionLimit_tf.type = vpiSysFunc
    __Py_GetRecursionLimit_fp = tf_func_t(__Py_GetRecursionLimit)
    __Py_GetRecursionLimit_tf.calltf = __Py_GetRecursionLimit_fp
    __Py_GetRecursionLimit_tf.userdata = None
    name = __Py_GetRecursionLimit_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetRecursionLimit_tf))

    global __Py_GetVersion_fp, __Py_GetVersion_f, __Py_GetVersion_tf
    __Py_GetVersion_f = getattr(libpy, "Py_GetVersion")
    __Py_GetVersion_f.restype = ctypes.c_char_p
    __Py_GetVersion_f.argtypes = []
    __Py_GetVersion_tf.tfname = "$Py_GetVersion".encode()
    __Py_GetVersion_tf.type = vpiSysTask
    __Py_GetVersion_fp = tf_func_t(__Py_GetVersion)
    __Py_GetVersion_tf.calltf = __Py_GetVersion_fp
    __Py_GetVersion_tf.userdata = None
    name = __Py_GetVersion_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_GetVersion_tf))

    global __Py_IncRef_fp, __Py_IncRef_f, __Py_IncRef_tf
    __Py_IncRef_f = getattr(libpy, "Py_IncRef")
    __Py_IncRef_f.restype = None
    __Py_IncRef_f.argtypes = [ctypes.c_void_p]
    __Py_IncRef_tf.tfname = "$Py_IncRef".encode()
    __Py_IncRef_tf.type = vpiSysTask
    __Py_IncRef_fp = tf_func_t(__Py_IncRef)
    __Py_IncRef_tf.calltf = __Py_IncRef_fp
    __Py_IncRef_tf.userdata = None
    name = __Py_IncRef_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_IncRef_tf))

    global __Py_Initialize_fp, __Py_Initialize_f, __Py_Initialize_tf
    __Py_Initialize_f = getattr(libpy, "Py_Initialize")
    __Py_Initialize_f.restype = None
    __Py_Initialize_f.argtypes = []
    __Py_Initialize_tf.tfname = "$Py_Initialize".encode()
    __Py_Initialize_tf.type = vpiSysTask
    __Py_Initialize_fp = tf_func_t(__Py_Initialize)
    __Py_Initialize_tf.calltf = __Py_Initialize_fp
    __Py_Initialize_tf.userdata = None
    name = __Py_Initialize_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_Initialize_tf))

    global __Py_InitializeEx_fp, __Py_InitializeEx_f, __Py_InitializeEx_tf
    __Py_InitializeEx_f = getattr(libpy, "Py_InitializeEx")
    __Py_InitializeEx_f.restype = None
    __Py_InitializeEx_f.argtypes = [ctypes.c_int]
    __Py_InitializeEx_tf.tfname = "$Py_InitializeEx".encode()
    __Py_InitializeEx_tf.type = vpiSysTask
    __Py_InitializeEx_fp = tf_func_t(__Py_InitializeEx)
    __Py_InitializeEx_tf.calltf = __Py_InitializeEx_fp
    __Py_InitializeEx_tf.userdata = None
    name = __Py_InitializeEx_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_InitializeEx_tf))

    global __Py_IsInitialized_fp, __Py_IsInitialized_f, __Py_IsInitialized_tf
    __Py_IsInitialized_f = getattr(libpy, "Py_IsInitialized")
    __Py_IsInitialized_f.restype = ctypes.c_int
    __Py_IsInitialized_f.argtypes = []
    __Py_IsInitialized_tf.tfname = "$Py_IsInitialized".encode()
    __Py_IsInitialized_tf.type = vpiSysFunc
    __Py_IsInitialized_fp = tf_func_t(__Py_IsInitialized)
    __Py_IsInitialized_tf.calltf = __Py_IsInitialized_fp
    __Py_IsInitialized_tf.userdata = None
    name = __Py_IsInitialized_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_IsInitialized_tf))

    global __Py_LeaveRecursiveCall_fp, __Py_LeaveRecursiveCall_f, __Py_LeaveRecursiveCall_tf
    __Py_LeaveRecursiveCall_f = getattr(libpy, "Py_LeaveRecursiveCall")
    __Py_LeaveRecursiveCall_f.restype = None
    __Py_LeaveRecursiveCall_f.argtypes = []
    __Py_LeaveRecursiveCall_tf.tfname = "$Py_LeaveRecursiveCall".encode()
    __Py_LeaveRecursiveCall_tf.type = vpiSysTask
    __Py_LeaveRecursiveCall_fp = tf_func_t(__Py_LeaveRecursiveCall)
    __Py_LeaveRecursiveCall_tf.calltf = __Py_LeaveRecursiveCall_fp
    __Py_LeaveRecursiveCall_tf.userdata = None
    name = __Py_LeaveRecursiveCall_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_LeaveRecursiveCall_tf))

    global __Py_MakePendingCalls_fp, __Py_MakePendingCalls_f, __Py_MakePendingCalls_tf
    __Py_MakePendingCalls_f = getattr(libpy, "Py_MakePendingCalls")
    __Py_MakePendingCalls_f.restype = ctypes.c_int
    __Py_MakePendingCalls_f.argtypes = []
    __Py_MakePendingCalls_tf.tfname = "$Py_MakePendingCalls".encode()
    __Py_MakePendingCalls_tf.type = vpiSysFunc
    __Py_MakePendingCalls_fp = tf_func_t(__Py_MakePendingCalls)
    __Py_MakePendingCalls_tf.calltf = __Py_MakePendingCalls_fp
    __Py_MakePendingCalls_tf.userdata = None
    name = __Py_MakePendingCalls_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_MakePendingCalls_tf))

    global __Py_ReprEnter_fp, __Py_ReprEnter_f, __Py_ReprEnter_tf
    __Py_ReprEnter_f = getattr(libpy, "Py_ReprEnter")
    __Py_ReprEnter_f.restype = ctypes.c_int
    __Py_ReprEnter_f.argtypes = [ctypes.c_void_p]
    __Py_ReprEnter_tf.tfname = "$Py_ReprEnter".encode()
    __Py_ReprEnter_tf.type = vpiSysFunc
    __Py_ReprEnter_fp = tf_func_t(__Py_ReprEnter)
    __Py_ReprEnter_tf.calltf = __Py_ReprEnter_fp
    __Py_ReprEnter_tf.userdata = None
    name = __Py_ReprEnter_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_ReprEnter_tf))

    global __Py_ReprLeave_fp, __Py_ReprLeave_f, __Py_ReprLeave_tf
    __Py_ReprLeave_f = getattr(libpy, "Py_ReprLeave")
    __Py_ReprLeave_f.restype = None
    __Py_ReprLeave_f.argtypes = [ctypes.c_void_p]
    __Py_ReprLeave_tf.tfname = "$Py_ReprLeave".encode()
    __Py_ReprLeave_tf.type = vpiSysTask
    __Py_ReprLeave_fp = tf_func_t(__Py_ReprLeave)
    __Py_ReprLeave_tf.calltf = __Py_ReprLeave_fp
    __Py_ReprLeave_tf.userdata = None
    name = __Py_ReprLeave_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_ReprLeave_tf))

    global __Py_RunMain_fp, __Py_RunMain_f, __Py_RunMain_tf
    __Py_RunMain_f = getattr(libpy, "Py_RunMain")
    __Py_RunMain_f.restype = ctypes.c_int
    __Py_RunMain_f.argtypes = []
    __Py_RunMain_tf.tfname = "$Py_RunMain".encode()
    __Py_RunMain_tf.type = vpiSysFunc
    __Py_RunMain_fp = tf_func_t(__Py_RunMain)
    __Py_RunMain_tf.calltf = __Py_RunMain_fp
    __Py_RunMain_tf.userdata = None
    name = __Py_RunMain_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_RunMain_tf))

    global __Py_SetRecursionLimit_fp, __Py_SetRecursionLimit_f, __Py_SetRecursionLimit_tf
    __Py_SetRecursionLimit_f = getattr(libpy, "Py_SetRecursionLimit")
    __Py_SetRecursionLimit_f.restype = None
    __Py_SetRecursionLimit_f.argtypes = [ctypes.c_int]
    __Py_SetRecursionLimit_tf.tfname = "$Py_SetRecursionLimit".encode()
    __Py_SetRecursionLimit_tf.type = vpiSysTask
    __Py_SetRecursionLimit_fp = tf_func_t(__Py_SetRecursionLimit)
    __Py_SetRecursionLimit_tf.calltf = __Py_SetRecursionLimit_fp
    __Py_SetRecursionLimit_tf.userdata = None
    name = __Py_SetRecursionLimit_tf.tfname.decode()
    ret = vpi_register_systf(ctypes.pointer(__Py_SetRecursionLimit_tf))
