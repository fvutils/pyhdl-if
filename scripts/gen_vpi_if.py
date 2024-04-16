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

file_header = """
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

ctype_m = {
    "double": "ctypes.c_double",
    "void": "None",
    "void*": "ctypes.c_void_p",
    "vpiHandle": "ctypes.c_void_p",
    "PLI_BYTE8*": "ctypes.c_char_p",
    "PLI_BYTE8": "ctypes.c_byte",
    "PLI_UBYTE8": "ctypes.c_ubyte",
    "PLI_INT16": "ctypes.c_short",
    "PLI_UINT16": "ctypes.c_ushort",
    "PLI_INT32": "ctypes.c_int",
    "PLI_UINT32": "ctypes.c_uint",
    "PLI_INT64": "ctypes.c_longlong",
    "PLI_UINT64": "ctypes.c_ulonglong"
}

class Preprocessor(pcpp.Preprocessor):
    
    def __init__(self):
        super().__init__()
        self._define_m = {}

    def on_include_not_found(self, is_malformed, is_system_include, curdir, includepath):
        raise pcpp.parser.OutputDirective(pcpp.parser.Action.IgnoreAndPassThrough)
        pass

    def on_directive_handle(self, directive, toks, ifpassthru, precedingtoks):
        if directive.value == "define":
            if len(toks) > 2 and toks[0].value.startswith("vpi"):
                key = toks[0].value
                if len(toks) == 3:
                    value = toks[2].value
                else:
                    value = ""
                    for t in toks[2:]:
                        value += t.value

                self._define_m[key] = value
        return super().on_directive_handle(directive, toks, ifpassthru, precedingtoks)

def gen_ctype(t):
    global ctype_m
    ts = t.format()

    if ts in ctype_m.keys():
        return ctype_m[ts]
    elif ts.endswith("*"):
        if ts.startswith("struct"):
            return "ctypes.POINTER(%s)" % gen_ctype(ts[len("struct "):-1])
        else:
            return "ctypes.POINTER(%s)" % gen_ctype(ts[:-1])
    else:
        return ts

def gen_vpi_defines(fp, defines):
    for key,val in defines.items():
        fp.write("%s = %s\n" % (key, val))

def gen_vpi_types(fp, structs, typedefs):
    for s in structs:
        fp.write("class %s(ctypes.Structure):\n" % s.class_decl.typename.segments[0].name)
        fp.write("    _fields_ = [")
        for i,f in enumerate(s.fields):
            fp.write("%s(\"%s\", %s)%s\n" % (
                "        " if i>0 else "",
                f.name,
                gen_ctype(f.type),
                "," if i+1 < len(s.fields) else ""
            ))
        fp.write("    ]\n")
        fp.write("\n")
    fp.write("\n")
    for t in typedefs:
        if isinstance(t.type, cxxt.Pointer) and t.name.startswith("p_"):
            fp.write("%s = ctypes.POINTER(%s)\n" % (
                t.name,
                t.type.ptr_to.typename.segments[0].name
            ))
        pass

def gen_vpi_api(fp, functions):

    exclude = ['vpi_mcd_vprintf', 'vpi_vprintf']

    # Define placeholder symbols for the functions
    for f in functions:

        fp.write("%s = None\n" % f.name.segments[0].name)

    fp.write("\n\n")

    fp.write("def load(lib):")
    for i,f in enumerate(functions):
        if (i%8) == 0:
            fp.write("\n    global ")
        else:
            fp.write(", ")
        fp.write(f.name.segments[0].name)
    fp.write("\n\n")
    for f in functions:
        if f.name.segments[0].name in exclude:
            continue
        fp.write("    %s = getattr(lib, \"%s\")\n" % (
            f.name.segments[0].name,
            f.name.segments[0].name))
        if f.return_type is None:
            fp.write("    %s.restype = None\n" % f.name.segments[0].name)
        else:
            fp.write("    %s.restype = %s\n" % (
                f.name.segments[0].name,
                gen_ctype(f.return_type)))
            
        fp.write("    %s.argtypes = [" % f.name.segments[0].name)
        for i,p in enumerate(f.parameters):
            if i > 0:
                fp.write(", ")
            fp.write("%s" % gen_ctype(p.type))
        fp.write("]\n")

    pass

def main():
    parser = argparse.ArgumentParser(prog="gen_py_if")
#    parser.add_argument("outdir", help="Specifies the output directory")

    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    vpi_pkg_dir = os.path.abspath(os.path.join(scripts_dir, "../python/hdl_pi_if/vpi"))

    args = parser.parse_args()

    pp_out = io.StringIO()
    pp = Preprocessor()
    with open(os.path.join(scripts_dir, "vpi_user.h"), "r") as fp:
        pp.parse(fp)

    pp.write(pp_out)

#    print("preproc:\n%s\n" % pp_out.getvalue())
    data = parse_string(pp_out.getvalue())

#    for s in data.namespace.classes:
#        print("Class: %s" % str(s))
#            print

    functions = []
    for f in data.namespace.functions:
        name = f.name.segments[0].name
        if name.startswith("vpi_"):
            functions.append(f)

    functions.sort(key=lambda f: f.name.segments[0].name)



    with open(os.path.join(vpi_pkg_dir, "api.py"), "w") as fp:
        fp.write(file_header % "api.py")
        fp.write("import ctypes\n")

        fp.write("\n\n")

        gen_vpi_defines(fp, pp._define_m)

        fp.write("\n\n")

        gen_vpi_types(fp, data.namespace.classes, data.namespace.typedefs)

        gen_vpi_api(fp, functions)


if __name__ == "__main__":
    main()
