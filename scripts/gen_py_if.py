#!/usr/bin/env python3
#*
#* gen_py_if.py
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
import argparse
import io
import os
import pcpp
import sys
from enum import Enum, auto
from cxxheaderparser.simple import parse_string
import cxxheaderparser.types as cxxt
import sysconfig

ctype_m = {
    "PyObject*" : "ctypes.c_void_p",
    "PyTypeObject*" : "ctypes.c_void_p",
    "long long" : "ctypes.c_longlong",
    "long": "ctypes.c_int",
    "int": "ctypes.c_int",
    "int*": "ctypes.POINTER(ctypes.c_int)",
    "size_t": "ctypes.c_uint",
    "size_t*": "ctypes.POINTER(ctypes.c_uint)",
    "Py_ssize_t": "ctypes.c_uint",
    "Py_ssize_t*": "ctypes.POINTER(ctypes.c_uint)",
    "char*": "ctypes.c_char_p",
    "char**": "ctypes.POINTER(ctypes.c_char_p)",
    "const char*": "ctypes.c_char_p",
    "double" : "ctypes.c_double",
    "float" : "ctypes.c_float",
    "unsigned long": "ctypes.c_uint",
    "unsigned long long": "ctypes.c_ulonglong",
    "void*" : "ctypes.c_void_p",
    "wchar_t*" : "ctypes.c_char_p",
    "void" : "None",
}

typew_m = {
    "PyObject*" : 64,
    "PyTypeObject*" : 64,
    "long long" : 64,
    "long": 32,
    "int": 32,
    "int*": 64,
    "size_t": 32,
    "size_t*": 64,
    "Py_ssize_t": 32,
    "Py_ssize_t*": None,
    "char*": None,
    "char**": None,
    "const char*": None,
    "double" : 64,
    "float" : 32,
    "unsigned long": 32,
    "unsigned long long": 64,
    "void*" : 64,
    "wchar_t*" : None,
    "void": 0
}

file_header_sv = """
/**
 * %s
 *
 * Copyright 2023 Matthew Ballance and Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may 
 * not use this file except in compliance with the License.  
 * You may obtain a copy of the License at:
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software 
 * distributed under the License is distributed on an "AS IS" BASIS, 
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
 * See the License for the specific language governing permissions and 
 * limitations under the License.
 *
 * Created on:
 *     Author: 
 */
"""

file_header_py = """
#****************************************************************************
#* %s
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
"""

class Dir(Enum):
    In = "input"
    Out = "output"
    InOut = "inout"

class Preprocessor(pcpp.Preprocessor):

    def on_include_not_found(self, is_malformed, is_system_include, curdir, includepath):
        raise pcpp.parser.OutputDirective(pcpp.parser.Action.IgnoreAndPassThrough)
        pass

def gen_type(t):
    ts = t.format()
    if isinstance(t, cxxt.Type):
        return t.format()
    else:
        return t.format()

def gen_dpi_rtype(type_m, t):
    ts = t.format()
    if ts in type_m.keys():
        return type_m[ts][0]
    else:
        return ts

def gen_dpi_ptype(type_m, t):
    ts = t.format()
    if ts in type_m.keys():
        return "%s %s" % (type_m[ts][1].value, type_m[ts][0])
    else:
        return "input %s" % ts
    
def gen_ctype_rtype(t):
    global ctype_m
    if t is None:
        return "None"
    else:
        ts = t.format()
        if ts in ctype_m.keys():
            return ctype_m[ts]
        else:
            return ts
        
def get_size_rtype(t):
    global typew_m
    if t is None:
        return 0
    else:
        ts = t.format()
        if ts in typew_m.keys():
            return typew_m[ts]
        else:
            return None
        
def mangle_pname(name):
    reserved = {"string", "begin", "end", "module", "table"}

    if name in reserved:
        return "_" + name
    else:
        return name

def gen_dpi_imports(fp, functions):
    fp.write(file_header_sv % "pyhdl_dpi_imports.svh")
    fp.write("\n")

    type_m = {
        "PyObject*" : ("PyObject", Dir.In),
        "PyTypeObject*" : ("PyTypeObject", Dir.In),
        "long long" : ("longint", Dir.In),
        "long": ("int", Dir.In),
        "int*": ("int", Dir.Out),
        "size_t": ("int unsigned", Dir.In),
        "size_t*": ("int unsigned", Dir.Out),
        "Py_ssize_t": ("int unsigned", Dir.In),
        "Py_ssize_t*": ("int unsigned", Dir.Out),
        "char*": ("string", Dir.InOut),
        "char**": ("chandle", Dir.Out),
        "const char*": ("string", Dir.In),
        "double" : ("real", Dir.In),
        "float" : ("shortreal", Dir.In),
        "unsigned int": ("int unsigned", Dir.In),
        "unsigned long": ("int unsigned", Dir.In),
        "unsigned long long": ("longint unsigned", Dir.In),
        "void*" : ("chandle", Dir.In),
        "wchar_t*" : ("string", Dir.In)
    }

    # First, create typedefs
    for obj_t in ("PyObject", "PyTypeObject"):
        fp.write("    typedef chandle %s;\n" % obj_t)

    fp.write("\n")

    for i,f in enumerate(functions):
        if i:
            fp.write("\n")

        fp.write("    import \"DPI-C\" context function ")

        if f.return_type is None:
            fp.write("void ")
        else:
            fp.write("%s " % gen_dpi_rtype(type_m, f.return_type))
        fp.write("%s(" % f.name.segments[0].name)
        for j,p in enumerate(f.parameters):
            if j > 0:
                fp.write(", ")
            if p.name is not None:
                pname = mangle_pname(p.name)
            else:
                pname = "p%d" % j
            fp.write("%s %s" % (gen_dpi_ptype(type_m, p.type), pname))
        fp.write(");\n")

def gen_vpi_tf(fp, functions):
    fp.write(file_header_py % "py_tf.py")
    fp.write("import ctypes\n")
    fp.write("import os\n")
    fp.write("import sysconfig\n")
    fp.write("from .api import t_vpi_systf_data, t_vpi_value\n")
    fp.write("from .api import vpi_free_object, vpi_handle, vpi_iterate, vpi_scan\n")
    fp.write("from .api import vpi_put_value\n")
    fp.write("from .api import vpiArgument, vpiIntVal, vpiSysFuncSized, vpiSysTfCall, vpiNoDelay\n")
    fp.write("\n")

    # First, emit some general-purpose callback functions
    fp.write("sizetf_f = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))\n")
    fp.write("\n")
    fp.write("def sizetf32(p):\n")
    fp.write("    return 32\n")
    fp.write("sizetf32_fp = sizetf_f(sizetf32)\n")
    fp.write("\n")
    fp.write("def sizetf64(p):\n")
    fp.write("    return 64\n")
    fp.write("sizetf64_fp = sizetf_f(sizetf64)\n")
    fp.write("\n")

    for i,f in enumerate(functions):
        if i:
            fp.write("\n")
        fp.write("__%s_fp = None\n" % f.name.segments[0].name)
        fp.write("__%s_f = None\n" % f.name.segments[0].name)
        fp.write("__%s_tf = t_vpi_systf_data()\n" % f.name.segments[0].name)
        fp.write("def __%s(ud):\n" % f.name.segments[0].name)
        fp.write("    print(\"Hello from %s\", flush=True)\n" % f.name.segments[0].name)
        fp.write("    __tf_h = vpi_handle(vpiSysTfCall, None)\n")
        if len(f.parameters) > 0:
            fp.write("    __arg_h = vpi_iterate(vpiArgument, __tf_h)\n")
            for j,p in enumerate(f.parameters):
                fp.write("    __t = vpi_scan(__arg_h)\n")
                name = mangle_pname(p.name) if p.name is not None else "p%d" % j

            fp.write("    vpi_free_object(__arg_h)\n")
        
        if gen_ctype_rtype(f.return_type) != "void":
            fp.write("    __rval = t_vpi_value()\n")
            fp.write("    __rval.format = vpiIntVal\n")
            fp.write("    __rval.value.integer = 20\n")
            fp.write("    vpi_put_value(__tf_h, ctypes.pointer(__rval), None, vpiNoDelay)\n")
        fp.write("    return 0\n")

        pass
    
    fp.write("def register_tf():\n")
    fp.write("    from .api import vpi_register_systf, t_vpi_systf_data, vpiSysFunc, vpiSysTask\n")
    fp.write("\n")
    fp.write("    libpy_path = os.path.join(\n")
    fp.write("        sysconfig.get_config_var(\"LIBDIR\"),\n")
    fp.write("        sysconfig.get_config_var(\"INSTSONAME\"))\n")
    fp.write("    libpy = ctypes.cdll.LoadLibrary(libpy_path)\n")
    fp.write("\n")
    fp.write("    tf_func_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))")
    fp.write("\n")

    for i,f in enumerate(functions):
        if i:
            fp.write("\n")

        fp.write("    global __%s_fp, __%s_f, __%s_tf\n" % (
            f.name.segments[0].name,
            f.name.segments[0].name,
            f.name.segments[0].name))
        fp.write("    __%s_f = getattr(libpy, \"%s\")\n" % (
            f.name.segments[0].name,
            f.name.segments[0].name))
        fp.write("    __%s_f.restype = %s\n" % (
            f.name.segments[0].name,
            gen_ctype_rtype(f.return_type)))
        fp.write("    __%s_f.argtypes = [%s]\n" % (
            f.name.segments[0].name,
            ",".join([gen_ctype_rtype(p.type) for p in f.parameters])))
        fp.write("    __%s_tf.tfname = \"$%s\".encode()\n" % (
            f.name.segments[0].name,
            f.name.segments[0].name))
        rsize = get_size_rtype(f.return_type)
        rtype_s = gen_ctype_rtype(f.return_type)
        if f.return_type is None or gen_ctype_rtype(f.return_type) == "None" or rsize is None:
            fp.write("    __%s_tf.type = vpiSysTask\n" % (
                f.name.segments[0].name,))
#        elif rsize > 32:
#            fp.write("    __%s_tf.type = vpiSysFuncSized\n" % (
#                f.name.segments[0].name,
#                ))
        else:
            fp.write("    __%s_tf.type = vpiSysFunc\n" % (
                f.name.segments[0].name,
                ))
        fp.write("    __%s_fp = tf_func_t(__%s)\n" % (
            f.name.segments[0].name,
            f.name.segments[0].name))
        fp.write("    __%s_tf.calltf = __%s_fp\n" % (
            f.name.segments[0].name,
            f.name.segments[0].name,
            ))
#        fp.write("    __%s_tf.compiletf = None\n" % (
#            f.name.segments[0].name,
#            ))
        if rsize is None or rsize <= 32:
#            fp.write("    __%s_tf.sizetf = None\n" % (
#                f.name.segments[0].name,
#                ))
            pass
        else:
            fp.write("    __%s_tf.sizetf = sizetf64_fp\n" % (
                f.name.segments[0].name,
                ))
        fp.write("    __%s_tf.userdata = None\n" %(
            f.name.segments[0].name,
            ))
        fp.write("    name = __%s_tf.tfname.decode()\n" % f.name.segments[0].name)
#        fp.write("    print(\"register %s: %s\" % (name, str(vpi_register_systf)))\n")
        fp.write("    ret = vpi_register_systf(ctypes.pointer(__%s_tf))\n" %(
            f.name.segments[0].name,
            ))
#        fp.write("    print(\"    ret=%s\" % str(ret))\n")
        
    pass

def main():
    parser = argparse.ArgumentParser(prog="gen_py_if")
#    parser.add_argument("outdir", help="Specifies the output directory")

    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    hdl_if_dir = os.path.abspath(os.path.join(scripts_dir, "../python/hdl_if"))
    share_dir = os.path.join(hdl_if_dir, "share")
    share_dpi_dir = os.path.join(share_dir, "dpi")

    args = parser.parse_args()

    include_pref = {"Py_", "PyEval_", "PyErr_", "PyImport_", "PyLong_", "PyObject_", 
                    "PyTuple_", "PyUnicode_"}
    exclude_pref = {
        "_", "PyAsyncGen_", "PyBuffer_", "PyCapsule_", "PyCode_", "PyComplex_", 
        "PyConfig_", "PyCFunction_", "PyCMethod_", "PyCoro_",
        "PyFile_", "PyFrame_", "PyFunction_", "PyGen_", "PyHash_", 
        "PyLineTable_",
        "PyMem_", "PyMember_", "PyMemoryView_", "PyModule_", "PyModuleDef_", 
        "PyPickleBuffer_",
        "PyPreConfig_", "PyRun_", "PyState_", "PyStatus_", "PySys_",
        "PyThread_", "PyTraceBack_", "PyTraceMalloc_", 
        "PyUnstable_", "PyWideStringList_",
        "PyGILState_", "PyInterpreterState_", "PySignal_", "PyThreadState_", "PyStructSequence_",
        "PyWeakref_",
        "PyDescr_" }
    exclude = {
        "Py_INCREF", "Py_DECREF", "Py_Exit", "PyInit__imp",
        "Py_SymtableString", "Py_SymtableStringObject",
        "PyModule_AddType",
        "PyFunction_SetVectorcall", "PyVectorcall_Function", 
        "PyVectorcall_NARGS",
        "PyBytes_AS_STRING", "PyBytes_GET_SIZE",
        "PyByteArray_AS_STRING", "PyByteArray_GET_SIZE",
        "PyCell_GET", "PyCell_SET",
        "PyDict_AddWatcher", "PyDict_GET_SIZE",
        "PyErr_Fetch", "PyErr_FormatV", "PyErr_GetExcInfo", "PyErr_NormalizeException",
        "PyEval_AcquireLock", # Deprecated
        "PyEval_CallObjectWithKeywords", # Deprecated
        "PyEval_InitThreads", # Deprecated
        "PyEval_ReleaseLock", # Deprecated
        "PyEval_ThreadsInitialized", # Deprecated
        "PyEval_CallFunction", # Deprecated
        "PyEval_SetProfile", "PyEval_SetProfileAllThreads", 
        "PyEval_SetTrace", "PyEval_SetTraceAllThreads",
        "PyEval_MergeCompilerFlags",
        "Py_NewInterpreter", "Py_EndInterpreter", "Py_NewInterpreterFromConfig",
        "PyEval_GetFrame", "PyEval_EvalCodeEx", "PyEval_EvalFrame", "PyEval_EvalFrameEx",
        "PyEval_SaveThread", "PyEval_RestoreThread", "PyEval_AcquireThread",
        "PyEval_ReleaseThread",
        "PyErr_BadInternalCall",
        "PyFloat_AS_DOUBLE",
        "PyImport_AddAuditHook", "PyImport_AppendInittab", "PyImport_ExtendInittab",
        "PyInstanceMethod_GET_FUNCTION",
        "PyIter_Send",
        "PyList_GET_SIZE", "PyList_SET_ITEM",
        "PyMapping_Length",
        "PyMethod_GET_FUNCTION", "PyMethod_GET_SELF",
        "PyObject_GetBuffer", "Py_SET_SIZE", 
        "PySequence_In", "PySequence_Length",
        "PySet_GET_SIZE",
        "PySlice_GetIndicesEx",
        "PyTuple_GET_SIZE", "PyTuple_SET_ITEM",
        "PyType_Check", "PyType_CheckExact",
        "PyType_FromSpec", "PyType_FromSpecWithBases",
        "PyType_FromModuleAndSpec", "PyType_FromMetaclass", "PyType_GetModuleByDef",
        "PyType_AddWatcher",
        "PyLong_FromUnicode", 
        "PyObject_AsCharBuffer", # Deprecated
        "PyObject_AsReadBuffer", # Deprecated
        "PyObject_AsWriteBuffer", # Deprecated
        "PyObject_CallMethodNoArgs", "PyObject_CallMethodOneArg",
        "PyObject_CheckReadBuffer", # Deprecated
        "PyObject_Hash", "PyObject_HashNotImplemented", "PyObject_InitVar",
        "PyObject_GetArenaAllocator", "PyObject_SetArenaAllocator", "PyObject_Length",
        "PyObject_Print", "PyObject_PrintObject",
        "PyObject_TypeCheck", "PyObject_GET_WEAKREFS_LISTPTR", "PyObject_GetTypeData",
        "PyObject_Vectorcall", "PyObject_VectorcallDict", "PyObject_VectorcallMethod",
        "Py_AtExit", 
        "Py_BytesMain", "Py_GetArgcArgv",
        "Py_CompileStringExFlags", "Py_CompileStringObject", "Py_FdIsInteractive",
        "Py_FrozenMain",
        "Py_DecodeLocale", "Py_EncodeLocale",
        "Py_Main",
        "Py_AddPendingCall", "Py_UniversalNewlineFgets", "Py_VaBuildValue",
        "Py_SetPath", # Deprecated
        "Py_SetProgramName", # Deprecated
        "Py_SetPythonHome", # Deprecated
        "Py_SetStandardStreamEncoding", # Deprecated
        "Py_CompileString", "Py_ExitStatusException", "Py_FatalError", "Py_IS_TYPE", "Py_Is",
        "Py_IsFalse", "Py_IsTrue", "Py_IsNone", "Py_NewRef", "Py_REFCNT", "Py_SET_REFCNT",
        "Py_SET_TYPE", "Py_SIZE", "Py_TYPE", "Py_XDECREF", "Py_XINCREF", "Py_XNewRef",
        "PyOS_AfterFork", # Deprecated
        "PyOS_getsig", "PyOS_setsig", "Py_PreInitialize",
        "Py_PreInitializeFromBytesArgs", "Py_PreInitializeFromArgs",
        "Py_InitializeFromConfig", "PyExitStatusException",
        "PyUnicode_Append", "PyUnicode_AppendAndDel", "PyUnicode_AsUCS4", "PyUnicode_AsUCS4Copy",
        "PyUnicode_Fill", "PyUnicode_FindChar", "PyUnicode_FromKindAndData", "PyUnicode_FromWideChar",
        "PyUnicode_FromFormatV", "PyUnicode_MAX_CHAR_VALUE", "PyUnicode_New", "PyUnicode_READ",
        "PyUnicode_READ_CHAR", "PyUnicode_ReadChar", "PyUnicode_WRITE", "PyUnicode_WriteChar",
        "PyUnicode_InternInPlace", "PyUnicode_Resize",
        "PyUnicode_AsUnicode", "PyUnicode_AsUnicodeAndSize", "PyUnicode_AsUnicodeCopy", "PyUnicode_Encode",
        "PyUnicode_EncodeASCII", "PyUnicode_EncodeCharmap", "PyUnicode_EncodeDecimal",
        "PyUnicode_EncodeLatin1", "PyUnicode_EncodeRawUnicodeEscape", "PyUnicode_EncodeUTF16",
        "PyUnicode_EncodeUTF32", "PyUnicode_EncodeUTF7", "PyUnicode_EncodeUTF8",
        "PyUnicode_TransformDecimalToASCII", "PyUnicode_TranslateCharmap", 
        "PyUnicode_EncodeUnicodeEscape", "PyUnicode_FromUnicode",
        "PyUnicode_GetMax", "PyUnicode_InternImmortal", 
        "Py_UNICODE_IS_SURROGATE", "Py_UNICODE_IS_HIGH_SURROGATE", "Py_UNICODE_IS_LOW_SURROGATE",
        "Py_UNICODE_JOIN_SURROGATES", "Py_UNICODE_HIGH_SURROGATE", "Py_UNICODE_LOW_SURROGATE",
        "Py_UNICODE_ISSPACE", "Py_UNICODE_ISALNUM",
        "Py_UNICODE_strcat", "Py_UNICODE_strchr", "Py_UNICODE_strcmp", "Py_UNICODE_strcpy",
        "Py_UNICODE_strlen", "Py_UNICODE_strncmp", "Py_UNICODE_strncpy", 
        "Py_UNICODE_strrchr"}
    paths = sysconfig.get_paths()
    py_incdir = paths["include"]
    pp_out = io.StringIO()
    pp = Preprocessor()
    pp.add_path(py_incdir)
    pp.define("UCHAR_MAX 255")
    with open(os.path.join(py_incdir, "Python.h"), "r") as fp:
        pp.parse(fp)

    pp.write(pp_out)

    data = parse_string(pp_out.getvalue())

    print("Namespace: %s" % data.namespace.name)

    functions = []
    for f in data.namespace.functions:
        name = f.name.segments[0].name
        first_under = name.find("_")
        prefix = name[:first_under+1]
#        print("name: %s" % name)
        include = prefix in include_pref and prefix not in exclude_pref and name not in exclude
        include &= not f.vararg
        include &= not f.inline

        if include:
#            print("function: %s" % name)
            functions.append(f)

    functions.sort(key=lambda f: f.name.segments[0].name)

    with open(os.path.join(share_dpi_dir, "pyhdl_dpi_imports.svh"), "w") as fp:
        gen_dpi_imports(fp, functions)
    
    with open(os.path.join(hdl_if_dir, "impl/pi/vpi/pytf.py"), "w") as fp:
        gen_vpi_tf(fp, functions)

    pass


if __name__ == "__main__":
    main()
