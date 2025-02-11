#!/usr/bin/env python3
#*
#* gen_py_if.py
#*
#* Copyright 2023-2024 Matthew Ballance and Contributors
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
    "long": "ctypes.c_long",
    "int": "ctypes.c_int",
    "int*": "ctypes.POINTER(ctypes.c_int)",
    "size_t": "ctypes.c_uint",
    "size_t*": "ctypes.POINTER(ctypes.c_uint)",
    "Py_ssize_t": "ctypes.c_uint64",
    "Py_ssize_t*": "ctypes.POINTER(ctypes.c_uint)",
    "char*": "ctypes.c_char_p",
    "char**": "ctypes.POINTER(ctypes.c_char_p)",
    "const char*": "ctypes.c_char_p",
    "double" : "ctypes.c_double",
    "float" : "ctypes.c_float",
    "unsigned long": "ctypes.c_ulong",
    "unsigned long long": "ctypes.c_ulonglong",
    "void*" : "ctypes.c_void_p",
    "wchar_t*" : "ctypes.c_char_p",
    "void" : "None",
}

typew_m = {
    "PyObject*" : 64,
    "PyTypeObject*" : 64,
    "long long" : 64,
    "long": 64,
    "int": 32,
    "int*": 64,
    "size_t": 32,
    "size_t*": 64,
    "Py_ssize_t": 64,
    "Py_ssize_t*": None,
    "char*": None,
    "char**": None,
    "const char*": None,
    "double" : 64,
    "float" : 32,
    "unsigned long": 64,
    "unsigned long long": 64,
    "void*" : 64,
    "wchar_t*" : None,
    "void": 0
}

file_header_sv = """
/**
 * %s
 *
 * Copyright 2023-2024 Matthew Ballance and Contributors
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
#* Copyright 2023-2024 Matthew Ballance and Contributors
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

def gen_c_rtype(t):
    if t is None:
        return "void"
    else:
        return t.format()

def gen_c_type(t):
    return t.format()
        
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
    reserved = {"string", "begin", "end", "map", "module", "set", "table"}

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
        "long": ("longint", Dir.In),
        "int*": ("int", Dir.Out),
        "size_t": ("int unsigned", Dir.In),
        "size_t*": ("int unsigned", Dir.Out),
        "Py_ssize_t": ("longint unsigned", Dir.In),
        "Py_ssize_t*": ("longint unsigned", Dir.Out),
        "char*": ("string", Dir.InOut),
        "char**": ("chandle", Dir.Out),
        "const char*": ("string", Dir.In),
        "double" : ("real", Dir.In),
        "float" : ("shortreal", Dir.In),
        "unsigned int": ("int unsigned", Dir.In),
        "unsigned long": ("longint unsigned", Dir.In),
        "unsigned long long": ("longint unsigned", Dir.In),
        "void*" : ("chandle", Dir.In),
        "wchar_t*" : ("string", Dir.In)
    }

    # First, create typedefs
    for obj_t in ("PyObject", "PyTypeObject"):
        fp.write("    typedef chandle %s;\n" % obj_t)
    for obj_t in ("PyGILState_STATE",):
        fp.write("    typedef int unsigned %s;\n" % obj_t)

    fp.write("\n")

    for i,f in enumerate(functions):
        if i:
            fp.write("\n")

        fp.write("    import \"DPI-C\" context function ")
        
        if f.return_type is None or f.return_type.format() == "void":
            fp.write("void ")
        else:
            fp.write("%s " % gen_dpi_rtype(type_m, f.return_type))

        fp.write("_pyhdl_if_%s(" % f.name.segments[0].name)
        for j,p in enumerate(f.parameters):
            if j > 0:
                fp.write(", ")
            if p.name is not None:
                pname = mangle_pname(p.name)
            else:
                pname = "p%d" % j
            fp.write("%s %s" % (gen_dpi_ptype(type_m, p.type), pname))
        fp.write(");\n")
        fp.write("\n")

        fp.write("    function ")

        if f.return_type is None or f.return_type.format() == "void":
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
        fp.write("        ")
        if f.return_type is not None and f.return_type.format() != "void":
            fp.write("return ")
        fp.write("_pyhdl_if_%s(" % f.name.segments[0].name)
        for j,p in enumerate(f.parameters):
            if j > 0:
                fp.write(", ")
            if p.name is not None:
                pname = mangle_pname(p.name)
            else:
                pname = "p%d" % j
            fp.write("%s" % pname)
        fp.write(");\n")
        fp.write("    endfunction\n")




def gen_py_if(fp, functions):

    fp.write(file_header_sv % "py_api_if.h")
    fp.write("#ifndef INCLUDED_PY_API_IF_H\n")
    fp.write("#define INCLUDED_PY_API_IF_H\n")
    fp.write("\n")
    fp.write("typedef struct PyObject_s *PyObject;\n")
    fp.write("typedef struct PyTypeObject_s *PyTypeObject;\n")
    fp.write("typedef uintptr_t Py_ssize_t;\n")
    fp.write("typedef int PyGILState_STATE;\n")
    fp.write("\n")
    gen_py_api_struct(fp, functions)
    fp.write("\n")
    fp.write("static py_api       prv_py_api;\n")
    fp.write("\n")
    gen_py_load_api_struct(fp, functions)
    fp.write("\n")
    fp.write("#endif /* INCLUDED_PY_API_IF_H */\n")
    pass

def gen_dpi_if(fp, functions):
    fp.write(file_header_sv % "py_dpi_if.h")
    fp.write("#ifndef INCLUDED_PY_DPI_IF_H\n")
    fp.write("#define INCLUDED_PY_DPI_IF_H\n")
    fp.write("\n")
    fp.write("typedef struct PyObject_s *PyObject;\n")
    fp.write("typedef struct PyTypeObject_s *PyTypeObject;\n")
    fp.write("typedef uintptr_t Py_ssize_t;\n")
    fp.write("typedef int PyGILState_STATE;\n")
    fp.write("\n")
    gen_py_dpi_trampoline(fp, functions)
    fp.write("\n")
    fp.write("#endif /* INCLUDED_PY_DPI_IF_H */\n")
    pass

def gen_vpi_tf(fp, functions):
    fp.write(file_header_sv % "py_vpi_if.h")
    fp.write("#ifndef INCLUDED_VPI_TF_IF_H\n")
    fp.write("#define INCLUDED_VPI_TF_IF_H\n")
    fp.write('#include "vpi_user.h"\n')
    fp.write('#include "py_api_if.h"\n')
    fp.write("\n")

    # First, emit some general-purpose callback functions
    # fp.write("sizetf_f = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))\n")
    # fp.write("\n")
    # fp.write("def sizetf32(p):\n")
    # fp.write("    return 32\n")
    # fp.write("sizetf32_fp = sizetf_f(sizetf32)\n")
    # fp.write("\n")
    # fp.write("def sizetf64(p):\n")
    # fp.write("    return 64\n")
    # fp.write("sizetf64_fp = sizetf_f(sizetf64)\n")
    # fp.write("\n")

    # Emit the API struct that we use to access VPI primitives internally
    gen_vpi_api_struct(fp)
    fp.write("\n")

    fp.write("static s_vpi_vecval prv_vecval[16];\n")
    fp.write("static vpi_api      prv_vpi_api;\n")
    fp.write("\n")

    # Next, emit reusable utility functions
    gen_vpi_utils(fp)
    fp.write("\n")

    fp.write("static PLI_INT32 sizetf64(PLI_BYTE8 *ud) {\n")
    #fp.write('    fprintf(stdout, "sizetf64\\n");\n')
    fp.write("    return 64;\n")
    fp.write("}\n")

    # Next, emit TF implementations
    gen_vpi_py_impl(fp, functions)
    fp.write("\n")

    gen_vpi_load_api_struct(fp)
    fp.write("\n")

    # Emit TF registration
    gen_vpi_tf_reg(fp, functions)
    fp.write("\n")

#     fp.write("def register_tf():\n")
#     fp.write("    from .api import vpi_register_systf, t_vpi_systf_data, vpiSysFunc, vpiSysTask\n")
#     fp.write("\n")
#     fp.write("    libpy_path = os.path.join(\n")
#     fp.write("        sysconfig.get_config_var(\"LIBDIR\"),\n")
#     fp.write("        sysconfig.get_config_var(\"INSTSONAME\"))\n")
#     fp.write("    libpy = ctypes.cdll.LoadLibrary(libpy_path)\n")
#     fp.write("\n")
#     fp.write("    tf_func_t = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))")
#     fp.write("\n")

#     for i,f in enumerate(functions):
#         if i:
#             fp.write("\n")

#         fp.write("    global __%s_fp, __%s_f, __%s_tf\n" % (
#             f.name.segments[0].name,
#             f.name.segments[0].name,
#             f.name.segments[0].name))
#         fp.write("    __%s_f = getattr(libpy, \"%s\")\n" % (
#             f.name.segments[0].name,
#             f.name.segments[0].name))
#         fp.write("    __%s_f.restype = %s\n" % (
#             f.name.segments[0].name,
#             gen_ctype_rtype(f.return_type)))
#         fp.write("    __%s_f.argtypes = [%s]\n" % (
#             f.name.segments[0].name,
#             ",".join([gen_ctype_rtype(p.type) for p in f.parameters])))
#         fp.write("    __%s_tf.tfname = \"$%s\".encode()\n" % (
#             f.name.segments[0].name,
#             f.name.segments[0].name))
#         rsize = get_size_rtype(f.return_type)
#         rtype_s = gen_ctype_rtype(f.return_type)
#         if f.return_type is None or gen_ctype_rtype(f.return_type) == "None" or rsize is None:
#             fp.write("    __%s_tf.type = vpiSysTask\n" % (
#                 f.name.segments[0].name,))
# #        elif rsize > 32:
# #            fp.write("    __%s_tf.type = vpiSysFuncSized\n" % (
# #                f.name.segments[0].name,
# #                ))
#         else:
#             fp.write("    __%s_tf.type = vpiSysFunc\n" % (
#                 f.name.segments[0].name,
#                 ))
#         fp.write("    __%s_fp = tf_func_t(__%s)\n" % (
#             f.name.segments[0].name,
#             f.name.segments[0].name))
#         fp.write("    __%s_tf.calltf = __%s_fp\n" % (
#             f.name.segments[0].name,
#             f.name.segments[0].name,
#             ))
# #        fp.write("    __%s_tf.compiletf = None\n" % (
# #            f.name.segments[0].name,
# #            ))
#         if rsize is None or rsize <= 32:
# #            fp.write("    __%s_tf.sizetf = None\n" % (
# #                f.name.segments[0].name,
# #                ))
#             pass
#         else:
#             fp.write("    __%s_tf.sizetf = &sizetf64\n" % (
#                 f.name.segments[0].name,
#                 ))
#         fp.write("    __%s_tf.user_data = None\n" %(
#             f.name.segments[0].name,
#             ))
#         fp.write("    name = __%s_tf.tfname.decode()\n" % f.name.segments[0].name)
# #        fp.write("    print(\"register %s: %s\" % (name, str(vpi_register_systf)))\n")
#         fp.write("    ret = vpi_register_systf(ctypes.pointer(__%s_tf))\n" %(
#             f.name.segments[0].name,
#             ))
# #        fp.write("    print(\"    ret=%s\" % str(ret))\n")
    fp.write("#endif /* INCLUDED_VPI_TF_IF_H */\n")
    pass

def gen_vpi_api_struct(fp):
    fp.write("typedef struct vpi_api_s {\n")
    fp.write("    PLI_INT32 (*vpi_get)(PLI_INT32 property, vpiHandle hndl);\n")
    fp.write("    vpiHandle (*vpi_handle)(PLI_INT32 type, vpiHandle hndl);\n")
    fp.write("    vpiHandle (*vpi_iterate)(PLI_INT32 type, vpiHandle hndl);\n")
    fp.write("    vpiHandle (*vpi_scan)(vpiHandle hndl);\n")
    fp.write("    vpiHandle (*vpi_register_systf)(s_vpi_systf_data *data);\n")
    fp.write("    void (*vpi_get_value)(vpiHandle, s_vpi_value *);\n")
    fp.write("    vpiHandle (*vpi_put_value)(vpiHandle, s_vpi_value *, s_vpi_time *, PLI_INT32);\n")
    fp.write("    void (*vpi_free_object)(vpiHandle);\n")
    fp.write("} vpi_api;\n")

def gen_vpi_load_api_struct(fp):
    fp.write("static int vpi_load_api_struct(void *lib_h) {\n")
    fp.write("    uint32_t i, ret=1;\n")
    fp.write("    struct ft_entry_s {\n")
    fp.write("        const char *name;\n")
    fp.write("        void **fpp;\n")
    fp.write("    } vpi_funcs[] = {\n")
    funcs = ("vpi_handle", "vpi_iterate", "vpi_scan", "vpi_register_systf",
             "vpi_get_value", "vpi_put_value", "vpi_free_object", "vpi_get")
    for i,fn in enumerate(funcs):
        fp.write("        {\"%s\", (void **)&prv_vpi_api.%s}%s\n" % (
            fn,
            fn,
            "," if i+1 < len(funcs) else ""))
    fp.write("    };\n")
    fp.write("    for (i=0; i<sizeof(vpi_funcs)/sizeof(struct ft_entry_s); i++) {\n")
    fp.write("        void *sym = dlsym(lib_h, vpi_funcs[i].name);\n");
    fp.write("        if (!sym) {\n")
    fp.write("            ret = 0;\n")
    fp.write('            fprintf(stdout, "Failed to find symbol %s\\n", vpi_funcs[i].name);\n');
    fp.write("        }\n")
    fp.write("        *vpi_funcs[i].fpp = sym;\n");
    fp.write("    }\n")
    fp.write("    return ret;\n")
    fp.write("}\n")

def gen_py_api_struct(fp, functions):
    fp.write("typedef struct py_api_s {\n")

    for i,f in enumerate(functions):
        if i:
            fp.write("\n")
        fp.write("    %s (*%s)(" % (
            gen_c_rtype(f.return_type),
            f.name.segments[0].name
        ))
        for i,p in enumerate(f.parameters):
            if i:
                fp.write(", ")
            name = "p%0d" % i if p.name is None else p.name
            fp.write("%s %s" % (p.type.format(), name))
        fp.write(");\n")
    fp.write("} py_api;\n")

def gen_py_dpi_trampoline(fp, functions):

    for i,f in enumerate(functions):
        if i:
            fp.write("\n")
        fp.write("%s _pyhdl_if_%s(" % (
            gen_c_rtype(f.return_type),
            f.name.segments[0].name
        ))
        for i,p in enumerate(f.parameters):
            if i:
                fp.write(", ")
            name = "p%0d" % i if p.name is None else p.name
            fp.write("%s %s" % (p.type.format(), name))
        fp.write(") {\n")
        fp.write("    ")
#        fp.write('fprintf(stdout, "== %s\\n"); fflush(stdout);\n' % f.name.segments[0].name)
        if gen_c_rtype(f.return_type) != "void":
            fp.write("return ")
        fp.write("prv_py_api.%s(" % f.name.segments[0].name)
        for i,p in enumerate(f.parameters):
            if i:
                fp.write(", ")
            fp.write("p%0d" % i if p.name is None else p.name)
        fp.write(");\n")

        fp.write("}\n")

def gen_py_load_api_struct(fp, functions):
    fp.write("static int py_load_api_struct(void *lib_h) {\n")
    fp.write("    int ret = 1;\n")
    fp.write("    uint32_t i;\n")
    fp.write("    struct fp_entry_s {\n")
    fp.write("        const char *name;\n")
    fp.write("        void **fp;\n")
    fp.write("    } py_funcs[] = {\n")
    for i,fn in enumerate(functions):
        fp.write("        {\"%s\", (void **)&prv_py_api.%s}%s\n" % (
            fn.name.segments[0].name,
            fn.name.segments[0].name,
            "," if i+1 < len(functions) else ""
        ))
    fp.write("    };\n")
    fp.write("    for (i=0; i<sizeof(py_funcs)/sizeof(struct fp_entry_s); i++) {\n")
    fp.write("        void *sym = dlsym(lib_h, py_funcs[i].name);\n")
    fp.write("        if (!sym) {\n")
    fp.write("        fprintf(stdout, \"pyhdl-if: Failed to find symbol %s\\n\", py_funcs[i].name);\n")
    fp.write("            ret = 0;\n")
    fp.write("        }\n")
    fp.write("        *(py_funcs[i].fp) = sym;\n")
    fp.write("    }\n")
    fp.write("    return ret;\n")
    fp.write("}\n")

def gen_vpi_utils(fp):
    fp.write("static double vpi_get_pval_double(vpiHandle arg_it) {\n")
    fp.write("    vpiHandle pval = prv_vpi_api.vpi_scan(arg_it);\n")
    fp.write("    s_vpi_value val_s;\n")
    #fp.write('    fprintf(stdout, "get_pval_int: pval=%p\\n", pval);\n')
    fp.write("    val_s.format = vpiIntVal;\n")
    fp.write("    prv_vpi_api.vpi_get_value(pval, &val_s);\n")
    fp.write("    return 0.0;\n")
#    fp.write("    return val_s.value.integer;\n")
    fp.write("}\n")
    fp.write("static int32_t vpi_get_pval_int(vpiHandle arg_it) {\n")
    fp.write("    vpiHandle pval = prv_vpi_api.vpi_scan(arg_it);\n")
    fp.write("    s_vpi_value val_s;\n")
    #fp.write('    fprintf(stdout, "get_pval_int: pval=%p\\n", pval);\n')
    fp.write("    val_s.format = vpiIntVal;\n")
    fp.write("    prv_vpi_api.vpi_get_value(pval, &val_s);\n")
    fp.write("    return val_s.value.integer;\n")
    fp.write("}\n")
    fp.write("static int64_t vpi_get_pval_int64(vpiHandle arg_it) {\n")
    fp.write("    vpiHandle pval = prv_vpi_api.vpi_scan(arg_it);\n")
    fp.write("    s_vpi_value val_s;\n")
    #fp.write('    fprintf(stdout, "get_pval_int: pval=%p\\n", pval);\n')
    fp.write("    val_s.format = vpiIntVal;\n")
    fp.write("    prv_vpi_api.vpi_get_value(pval, &val_s);\n")
    fp.write("    return val_s.value.integer;\n")
    fp.write("}\n")
    fp.write("\n")
    fp.write("static uintptr_t vpi_get_pval_ptr(vpiHandle arg_it) {\n")
    fp.write("    vpiHandle pval = prv_vpi_api.vpi_scan(arg_it);\n")
    fp.write("    uintptr_t ptr_ival;\n")
    fp.write("    s_vpi_value val_s;\n")
    #fp.write('    fprintf(stdout, "get_pval_ptr: pval=%p %d\\n", pval, prv_vpi_api.vpi_get(vpiType, pval));\n')
    #fp.write('    fflush(stdout);')
    fp.write("    val_s.format = vpiVectorVal;\n")
    fp.write("    prv_vpi_api.vpi_get_value(pval, &val_s);\n")
    fp.write("    ptr_ival = val_s.value.vector[0].bval;\n")
    fp.write("    ptr_ival <<= 32;\n")
    fp.write("    ptr_ival |= val_s.value.vector[0].aval;\n")
    fp.write('    DEBUG("ptr_ival: 0x%08llx", ptr_ival);\n')
    fp.write("    return ptr_ival;\n")
    fp.write("}\n")
    fp.write("\n")
    fp.write("static const char *vpi_get_pval_str(vpiHandle arg_it) {\n")
    fp.write("    vpiHandle pval = prv_vpi_api.vpi_scan(arg_it);\n")
    fp.write("    s_vpi_value val_s;\n")
    fp.write("    val_s.format = vpiStringVal;\n")
    fp.write("    prv_vpi_api.vpi_get_value(pval, &val_s);\n")
    #fp.write('    fprintf(stdout, "pval_str: %s\\n", val_s.value.str);\n')
    #fp.write('    fflush(stdout);\n')
    fp.write("    return val_s.value.str;\n")
    fp.write("}\n")
    fp.write("\n")
    # Setters
    fp.write("static void vpi_set_val_double(vpiHandle val_h, double val) {\n")
    fp.write("    s_vpi_value val_s;\n")
    fp.write("    val_s.format = vpiIntVal;\n")
    fp.write("    val_s.value.integer = val;\n")
    #fp.write('    fprintf(stdout, "val=%d\\n", val);\n')
    fp.write("    prv_vpi_api.vpi_put_value(val_h, &val_s, 0, vpiNoDelay);\n")
    fp.write("}\n")
    fp.write("static void vpi_set_val_int(vpiHandle val_h, int32_t val) {\n")
    fp.write("    s_vpi_value val_s;\n")
    fp.write("    val_s.format = vpiIntVal;\n")
    fp.write("    val_s.value.integer = val;\n")
    #fp.write('    fprintf(stdout, "val=%d\\n", val);\n')
    fp.write("    prv_vpi_api.vpi_put_value(val_h, &val_s, 0, vpiNoDelay);\n")
    fp.write("}\n")
    fp.write("static void vpi_set_val_int64(vpiHandle val_h, int32_t val) {\n")
    fp.write("    s_vpi_value val_s;\n")
    fp.write("    val_s.format = vpiIntVal;\n")
    fp.write("    val_s.value.integer = val;\n")
    #fp.write('    fprintf(stdout, "val=%d\\n", val);\n')
    fp.write("    prv_vpi_api.vpi_put_value(val_h, &val_s, 0, vpiNoDelay);\n")
    fp.write("}\n")
    fp.write("\n")
    fp.write("static void vpi_set_val_ptr(vpiHandle val_h, uintptr_t val) {\n")
    fp.write("    s_vpi_value val_s;\n")
    fp.write("    val_s.format = vpiVectorVal;\n")
    fp.write("    val_s.value.vector = prv_vecval;\n")
    fp.write('    DEBUG("set_ptr: ptr=0x%08llx", val);\n')
    fp.write("    prv_vecval[0].aval = val;\n")
    fp.write("    val >>= 32;\n")
    fp.write("    prv_vecval[0].bval = val;\n")
    fp.write('    DEBUG("set_ptr: ptr=0x%08llx ptr_ival={0x%08x,0x%08x}", val, prv_vecval[1].aval, prv_vecval[0].aval);\n')
    fp.write("    prv_vpi_api.vpi_put_value(val_h, &val_s, 0, vpiNoDelay);\n")
    fp.write("}\n")
    fp.write("\n")
    fp.write("static void vpi_set_val_str(vpiHandle val_h, const char *val) {\n")
    fp.write("    s_vpi_value val_s;\n")
    fp.write("    val_s.format = vpiStringVal;\n")
    fp.write("    val_s.value.str = (char *)val;\n")
    fp.write("    prv_vpi_api.vpi_put_value(val_h, &val_s, 0, vpiNoDelay);\n")
    fp.write("}\n")
    fp.write("\n")

vpi_ftype_m = {
    "PyObject*" : "vpiSizedFunc",
    "PyTypeObject*" : "vpiSizedFunc",
    "long long" : "vpiSizedFunc",
    "long": "vpiIntFunc",
    "int": "vpiIntFunc",
    "int*": "vpiSizedFunc",
    "size_t": "vpiIntFunc",
    "size_t*": "vpiSizedFunc",
    "Py_ssize_t": "vpiIntFunc",
    "Py_ssize_t*": None,
    "char*": None,
    "char**": None,
    "const char*": None,
    "double" : 64,
    "float" : 32,
    "unsigned long": "vpiIntFunc",
    "unsigned long long": "vpiSizedFunc",
    "void*" : "vpiSizedFunc",
    "wchar_t*" : None,
    "void": 0
}

def gen_vpi_functype(t):
    if t.format() in vpi_ftype_m.keys():
        return vpi_ftype_m[t.format()]
    else:
        raise Exception("Unsupported VPI return type %s" % t.format())

def gen_vpi_py_impl(fp, functions):
    for i,f in enumerate(functions):
        if i:
            fp.write("\n")
        fp.write("static int _%s_tf(PLI_BYTE8 *ud) {\n" % f.name.segments[0].name)
        if f.return_type is not None and f.return_type.format() != "void":
            fp.write("    %s __rval;\n" % gen_c_type(f.return_type))
        if len(f.parameters) > 0 or (f.return_type is not None and f.return_type.format() != "void"):
            fp.write("    vpiHandle __tf_h = prv_vpi_api.vpi_handle(vpiSysTfCall, 0);\n")
        if len(f.parameters) > 0:
            fp.write("    vpiHandle __arg_h = prv_vpi_api.vpi_iterate(vpiArgument, __tf_h);\n")
            try:
                for j,p in enumerate(f.parameters):
                    name = mangle_pname(p.name) if p.name is not None else "p%d" % j
                    fp.write("    %s __%s = %s;\n" % (
                        gen_c_type(p.type),
                        name,
                        gen_vpi_get_param("__arg_h", p.type)))
            except Exception as e:
                raise Exception("Parameter generation failed in %s (%s)" % (
                    f.name.segments[0].name,
                    str(e)))

            fp.write("    prv_vpi_api.vpi_free_object(__arg_h);\n")
        fp.write("    ")
        if f.return_type is not None and f.return_type.format() != "void":
            fp.write("__rval = ")
        
        # Generate function call
        fp.write("prv_py_api.%s" % f.name.segments[0].name)

        if len(f.parameters) == 0:
            fp.write("();")
        else:
            fp.write("(")
            for j,p in enumerate(f.parameters):
                name = mangle_pname(p.name) if p.name is not None else "p%d" % j
                if j:
                    fp.write(", ")
                fp.write("__%s" % name)
            fp.write(");")
        fp.write("\n")

        if f.return_type is not None and f.return_type.format() != "void":
            fp.write("    %s;\n" % gen_vpi_set('__tf_h', '__rval', f.return_type))
        fp.write("    return 0;\n")
        fp.write("}\n")

        pass
    
def gen_vpi_tf_reg(fp, functions):
    fp.write("static void vpi_register_python_tf() {\n")
    fp.write("    s_vpi_systf_data *tf;\n")
    fp.write('    DEBUG("vpi_register_python_tf()");\n')
    for i,f in enumerate(functions):
        fp.write("\n")

        fp.write("    tf = (s_vpi_systf_data *)malloc(sizeof(s_vpi_systf_data));\n")

        fp.write("    tf->tfname = \"$%s\";\n" % f.name.segments[0].name)
        rsize = get_size_rtype(f.return_type)
        rtype_s = gen_ctype_rtype(f.return_type)
        if f.return_type is None or gen_ctype_rtype(f.return_type) == "None" or rsize is None:
            fp.write("    tf->type = vpiSysTask;\n")
        else:
            fp.write("    tf->type = vpiSysFunc;\n")
            fp.write("    tf->sysfunctype = %s;\n" % gen_vpi_functype(f.return_type))

        fp.write("    tf->calltf = &_%s_tf;\n" % f.name.segments[0].name)
        fp.write("    tf->compiletf = 0;\n")
        if rsize is None or rsize <= 32:
            fp.write("    tf->sizetf = 0;\n")
#            fp.write("    __%s_tf.sizetf = None\n" % (
#                f.name.segments[0].name,
#                ))
            pass
        else:
            fp.write("    tf->sizetf = &sizetf64;\n")
        fp.write("    tf->user_data = 0;\n")
        fp.write("    if (!prv_vpi_api.vpi_register_systf(tf)) {\n")
        fp.write('        DEBUG("failed to register %s");\n' % f.name.segments[0].name)
        fp.write("    } else {\n")
        fp.write('        DEBUG("registered %s");\n' % f.name.segments[0].name)
        fp.write("    }\n")
    fp.write("}")
    pass


vpi_get_param_tm = {
    "PyObject*" : "vpi_get_pval_ptr",
    "PyTypeObject*" : "vpi_get_pval_ptr",
    "long long" : "vpi_get_pval_int64",
    "long": "vpi_get_pval_int",
    "int": "vpi_get_pval_int",
    "int*": "vpi_get_pval_ptr",
    "size_t": "vpi_get_pval_int",
    "size_t*": "vpi_get_pval_ptr",
    "Py_ssize_t": "vpi_get_pval_int",
    "Py_ssize_t*": "vpi_get_pval_ptr",
    "char*": "vpi_get_pval_str",
    "char**": "vpi_get_pval_ptr",
    "const char*": "vpi_get_pval_str",
    "double" : "vpi_get_pval_double",
    "float" : "vpi_get_pval_double",
    "unsigned long": "vpi_get_pval_int",
    "unsigned long long": "vpi_get_pval_int64",
    "void*" : "vpi_get_pval_ptr",
    "wchar_t*" : "vpi_get_pval_str",
    "PyGILState_STATE": "vpi_get_pval_int",
    # "void": 0
}

vpi_set_param_tm = {
    "PyObject*" : "vpi_set_val_ptr",
    "PyTypeObject*" : "vpi_set_val_ptr",
    "long long" : "vpi_set_val_int64",
    "long": "vpi_set_val_int",
    "int": "vpi_set_val_int",
    "int*": "vpi_set_val_ptr",
    "size_t": "vpi_set_val_int",
    "size_t*": "vpi_set_val_ptr",
    "Py_ssize_t": "vpi_set_val_int",
    "Py_ssize_t*": "vpi_set_val_ptr",
    "char*": "vpi_set_val_str",
    "char**": "vpi_set_val_ptr",
    "const char*": "vpi_set_val_str",
    "double" : "vpi_set_val_double",
    "float" : "vpi_set_val_double",
    "unsigned long": "vpi_set_val_int",
    "unsigned long long": "vpi_set_val_int64",
    "void*" : "vpi_set_val_ptr",
    "wchar_t*" : "vpi_set_val_ptr",
    "PyGILState_STATE": "vpi_set_val_int",
    # "void": 0
}

def gen_vpi_get_param(it_name, ptype):
    tname = ptype.format()

    if tname in vpi_get_param_tm.keys():
        if vpi_get_param_tm[tname] == "vpi_get_pval_ptr":
            return "(%s)" % tname + vpi_get_param_tm[tname] + "(%s)" % it_name
        else:
            return vpi_get_param_tm[tname] + "(%s)" % it_name
    else:
        raise Exception("parameter type %s is not supported" % ptype.format())

def gen_vpi_set(val_h_name, val_name, ptype):
    tname = ptype.format()

    if tname in vpi_set_param_tm.keys():
        if vpi_set_param_tm[tname] == "vpi_set_val_ptr":
            return vpi_set_param_tm[tname] + "(%s, (uintptr_t)%s)" % (val_h_name, val_name)
        else:
            return vpi_set_param_tm[tname] + "(%s, %s)" % (val_h_name, val_name)
    else:
        raise Exception("value type %s is not supported" % ptype.format())

def gen_py2ctypes(val_h_name, ptype):
    tname = ptype.format()

    if tname in ("char*", "const char*"):
        return "%s.encode()" % val_h_name
    else:
        return val_h_name

  

def main():
    parser = argparse.ArgumentParser(prog="gen_py_if")
#    parser.add_argument("outdir", help="Specifies the output directory")

    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    hdl_if_dir = os.path.abspath(os.path.join(scripts_dir, "../src/hdl_if"))
    build_dir = os.path.abspath(os.path.join(scripts_dir, "../build"))
    share_dir = os.path.join(hdl_if_dir, "share")
    share_dpi_dir = os.path.join(share_dir, "dpi")

    args = parser.parse_args()

    include_pref = {"Py_", "PyDict_", "PyEval_", "PyErr_", "PyImport_", 
                    "PyIter_", "PyList_", 
                    "PyLong_", "PyObject_", "PySet_",
                    "PyTuple_", "PyUnicode_", "PyGILState_"}
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
        "PyInterpreterState_", "PySignal_", "PyThreadState_", "PyStructSequence_",
        "PyWeakref_",
        "PyDescr_" }
    exclude = {
        "Py_INCREF", "Py_DECREF", "Py_Exit", "PyInit__imp",
        "PyDict_Merge", "PyDict_MergeFromSeq2", "PyDict_Next",
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
        "PyGILState_GetThisThreadState",
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
        "PyUnicode_AsWideChar",
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
    # Limit API to what was present in 3.8
#    pp.define("Py_LIMITED_API 0x03080000")
#    pp.define("Py_LIMITED_API");
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

    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    with open(os.path.join(build_dir, "py_api_if.h"), "w") as fp:
        gen_py_if(fp, functions)
    
    with open(os.path.join(build_dir, "py_vpi_if.h"), "w") as fp:
        gen_vpi_tf(fp, functions)

    with open(os.path.join(build_dir, "py_dpi_if.h"), "w") as fp:
        gen_dpi_if(fp, functions)

    pass


if __name__ == "__main__":
    print("gen_py_if main")
    main()
