#****************************************************************************
#* gen_sv_class.py
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
from .api_def import ApiDef
from .method_def import MethodDef, MethodKind

class GenSVClass(object):

    def __init__(self, out, ind="", uvm=False):
        self._out = out
        self._ind = ind
        self._uvm = uvm
        self._have_imp = False
        pass

    def gen(self, api : ApiDef):

        self._have_imp = False
        for m in api.methods:
            if m.kind in [MethodKind.ImpFunc, MethodKind.ImpTask]:
                self._have_imp = True
                break

        # First, generate the interface class
        self.gen_class_interface(api)

        self.println()

        self.gen_class_creator(api)

        self.println()

        self.gen_class_wrapper(api)

    def gen_class_interface(self, api : ApiDef):
        self.println("interface class I%s extends pyhdl_if::ICallApi;" % api.name)
        self.inc_ind()
        self.println()

        for m in api.methods:
            self.gen_pure_virtual(m)

        self.println()
        self.dec_ind()
        self.println("endclass")

    def gen_class_creator(self, api : ApiDef):
        self.println("%sclass %s #(type BASE_T=%s%s) extends BASE_T implements I%s;" % (
            "virtual " if self._have_imp else "",
            api.name,
            "uvm_object" if self._uvm else "pyhdl_if::CallEmptyBase",
            ", bit CREATE=1" if self._uvm else "",
            api.name))
        self.inc_ind()
        self.println()
        self.println("pyhdl_if::PyObject       m_obj;")
        self.println()

        if len(api.init_params) == 0 or self._uvm:
            self.println("function new(%s);" % (
                "string name=\"%s\"" % api.name if self._uvm else "",
            ))
        elif len(api.init_params) == 1:
            self.println("function new(%s %s);" % (
                self.svtype(api.init_params[0][1]),
                api.init_params[0][0]
            ))
        else:
            self.println("function new(")
            self.inc_ind()
            for i,p in enumerate(api.init_params):
                self.println("%s %s%s" % (
                    self.svtype(p[1]),
                    p[0],
                    "," if (i+1<len(api.init_params)) else ");"
                ))
            self.dec_ind()
        self.inc_ind()

        if len(api.init_params) == 0:
            if self._uvm:
                self.println("super.new(name);")
                self.println("if (CREATE) begin")
                self.inc_ind()
            self.println("m_obj = create_pyobj();")
            self.println("pyhdl_if::pyhdl_if_connectObject(m_obj, this);")
            if self._uvm:
                self.dec_ind()
                self.println("end")
        elif not self._uvm:
            self.write("%sm_obj = create_pyobj(" % self.ind())
            for i,p in enumerate(api.init_params):
                self.write("%s%s" % (", " if i else "", p[0]))
            self.write(");\n")
            self.println("pyhdl_if::pyhdl_if_connectObject(m_obj, this);")

        self.dec_ind()
        self.println("endfunction")

        self.println()
        self.gen_create_pyobj(api)
        self.println()

        self.gen_init(api)
        self.println()

        for m in api.methods:
            self.gen_tf_impl(m)

        self.println()
        self.gen_task_dispatch(api)
        self.println()
        self.gen_func_dispatch(api)
        self.println()
        self.dec_ind()
        self.println("endclass")

    def gen_create_pyobj(self, api : ApiDef):
        module_name = api.fullname
        last_dot = module_name.rfind('.')
        if last_dot != -1:
            module_name = module_name[:last_dot]

        if len(api.init_params) == 0:
            self.println("static function pyhdl_if::PyObject create_pyobj(string modname=\"%s\", string clsname=\"%s\");" % (
                module_name,
                api.name
            ))
        elif len(api.init_params) == 1:
            self.println("function pyhdl_if::PyObject create_pyobj(%s %s, string modname=\"%s\", string clsname=\"%s\");" % (
                self.svtype(api.init_params[0][1]),
                api.init_params[0][0],
                module_name,
                api.name
            ))
        else:
            self.println("function pyhdl_if::PyObject create_pyobj(")
            self.inc_ind()
            for i,p in enumerate(api.init_params):
                self.println("%s %s," % (
                    self.svtype(p[1]),
                    p[0]
                ))
            self.println("string modname=\"%s\"," % module_name)
            self.println("string clsname=\"%s\");" % api.name)
            self.dec_ind()

        self.inc_ind()
        self.println("pyhdl_if::PyObject __args, __cls_m, __cls_t, __obj;")
        self.println("pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();")
        self.println("__args = pyhdl_if::PyTuple_New(%d);" % len(api.init_params))
        self.println("__cls_m = pyhdl_if::PyImport_ImportModule(modname);")
        self.println()
        self.println("if (__cls_m == null) begin")
        self.inc_ind()
        self.println("pyhdl_if::PyErr_Print();")
        self.println("$display(\"Fatal Error: Failed to find module %%s\", modname);")
        self.println("$finish;")
        self.println("pyhdl_if::PyGILState_Release(state);")
        self.println("return null;")
        self.dec_ind()
        self.println("end")
        self.println()

        for i,p in enumerate(api.init_params):
            self.println("void'(PyTuple_SetItem(__args, %d, %s));" % (
                i,
                self.sv2py_func(p[1], p[0])))
        if len(api.init_params):
            self.println()

        self.println("__cls_t = pyhdl_if::PyObject_GetAttrString(__cls_m, clsname);")
        self.println("if (__cls_t == null) begin")
        self.inc_ind()
        self.println("pyhdl_if::PyErr_Print();")
        self.println("$display(\"Fatal Error: Failed to find class %%s\", clsname);")
        self.println("$finish;")
        self.println("pyhdl_if::PyGILState_Release(state);")
        self.println("return null;")
        self.dec_ind()
        self.println("end")
        self.println()

        self.println("__obj = pyhdl_if::PyObject_Call(__cls_t, __args, null);")
        self.println("if (__obj == null) begin")
        self.inc_ind()
        self.println("pyhdl_if::PyErr_Print();")
        self.println("$display(\"Fatal Error: Failed to construct class %s\");" % api.name)
        self.println("$finish;")
        self.println("pyhdl_if::PyGILState_Release(state);")
        self.println("return null;")
        self.dec_ind()
        self.println("end")
        self.println()
        self.println("pyhdl_if::PyGILState_Release(state);")
        self.println()
        self.println("return __obj;")
        self.dec_ind()
        self.println("endfunction")
        self.println()

    def gen_class_wrapper(self, api : ApiDef):
        self.println("%sclass %s_wrap #(type BASE_T=pyhdl_if::CallEmptyBase) extends BASE_T implements I%s;" % (
            "virtual " if self._have_imp else "",
            api.name,
            api.name))
        self.inc_ind()
        self.println()
        self.println("pyhdl_if::PyObject       m_obj;")
        self.println()

        self.println("function new(%s);" % (
            "string name=\"%s\"" if self._uvm else "pyhdl_if::PyObject obj=null",
        ))
        self.inc_ind()
        if self._uvm:
            self.println("super.new(name);")
        else:
            self.println("if (obj != null) begin")
            self.inc_ind()
            self.println("init(obj);")
            self.dec_ind()
            self.println("end")
        self.dec_ind()
        self.println("endfunction")

        self.println()
        self.gen_init(api)
        self.println()

        self.gen_create_pyobj(api)
        self.println()

        for m in api.methods:
            self.gen_tf_impl(m)

        self.println()
        self.gen_task_dispatch(api)
        self.println()
        self.gen_func_dispatch(api)
        self.println()
        self.dec_ind()
        self.println("endclass")

    def gen_init(self, api):
        self.println("function void init(pyhdl_if::PyObject obj);")
        self.inc_ind()
        self.println("pyhdl_if::pyhdl_if_connectObject(obj, this);");
        self.println("m_obj = obj;")
        self.dec_ind()
        self.println("endfunction")

    def gen_pure_virtual(self, m : MethodDef):
        task_rtype = m.rtype if m.kind in [MethodKind.ImpTask, MethodKind.ExpTask] else None
        self.write("%spure virtual %s " % (
            self.ind,
            "task" if m.kind in [MethodKind.ImpTask, MethodKind.ExpTask] else "function"))
        if m.kind in [MethodKind.ImpFunc, MethodKind.ExpFunc]:
            if m.rtype is None:
                self.write("void ")
            else:
                self.write("%s " % self.svtype(m.rtype))

        if len(m.params) == 0:
            self.write("%s(%s);\n" % (
                m.name,
                ("output %s retval" % self.svtype(m.rtype)) if task_rtype is not None else ""))
        elif len(m.params) == 1:
            self.write("%s(%s" % (
                m.name,
                ("output %s retval, " % self.svtype(m.rtype)) if task_rtype is not None else ""))
            self.write("input %s %s);\n" % (
                self.svtype(m.params[0][1]),
                m.params[0][0]
            ))
        else:
            self.write("%s(\n" % m.name)
            self.inc_ind()
            if task_rtype is not None:
                self.println("output %s retval," % self.svtype(m.rtype))
            for i,p in enumerate(m.params):
                self.println("input %s %s%s" % (
                    self.svtype(p[1]),
                    p[0],
                    "," if (i+1<len(m.params)) else ""
                ))
            self.dec_ind()
            self.println(");")
            self.println()

    def gen_tf_impl(self, m : MethodDef):
        if m.kind in [MethodKind.ImpFunc, MethodKind.ImpTask]:
            ind = self._ind
            self._ind = ""
#            self.println("// Note: as of 5.024, Verilator has issues with unimplemented methods")
#            self.println("`ifdef VERILATOR")
            self._ind = ind

        task_rtype = m.rtype if m.kind in [MethodKind.ImpTask, MethodKind.ExpTask] else None
        self.write("%svirtual %s " % (
            self.ind,
            "task" if m.kind in [MethodKind.ImpTask, MethodKind.ExpTask] else "function"))
        if m.kind in [MethodKind.ImpFunc, MethodKind.ExpFunc]:
            if m.rtype is None:
                self.write("void ")
            else:
                self.write("%s " % self.svtype(m.rtype))

        if len(m.params) == 0:
            self.write("%s(%s);\n" % (
                m.name,
                ("output %s retval" % self.svtype(m.rtype)) if task_rtype is not None else ""))
        elif len(m.params) == 1:
            self.write("%s(%s" % (
                m.name,
                ("output %s retval, " % self.svtype(m.rtype)) if task_rtype is not None else ""))
            self.write("input %s %s);\n" % (
                self.svtype(m.params[0][1]),
                m.params[0][0]
            ))
        else:
            self.write("%s(\n" % m.name)
            self.inc_ind()
            if task_rtype is not None:
                self.println("output %s retval," % self.svtype(m.rtype))
            for i,p in enumerate(m.params):
                self.println("input %s %s%s" % (
                    self.svtype(p[1]),
                    p[0],
                    "," if (i+1<len(m.params)) else ""
                ))
            self.dec_ind()
            self.println(");")
            self.println()

        self.inc_ind()
        if m.kind in [MethodKind.ImpFunc, MethodKind.ImpTask]:
            # Generate backstop logic
            pass
        else:
            self.println("pyhdl_if::PyObject __res;")
            self.println("pyhdl_if::PyObject __args = pyhdl_if::PyTuple_New(%d);" % len(m.params))
            for i,p in enumerate(m.params):
                self.println("void'(pyhdl_if::PyTuple_SetItem(__args, %d, %s));" % (
                    i,
                    self.sv2py_func(p[1], p[0])))
            if m.kind == MethodKind.ExpTask:
                self.println("pyhdl_if::pyhdl_if_invokePyTask(__res, m_obj, \"%s\", __args);" % (
                    m.name,))
            else:
                self.println("__res = pyhdl_if::pyhdl_if_invokePyFunc(m_obj, \"%s\", __args);" % (
                    m.name,))
                self.println("return %s(__res);" % self.py2sv_func(m.rtype))

        self.dec_ind()


        self.println("end%s" % (
            "task" if m.kind in [MethodKind.ImpTask, MethodKind.ExpTask] else "function",))
        if m.kind in [MethodKind.ImpFunc, MethodKind.ImpTask]:
            ind = self._ind
            self._ind = ""
#            self.println("`endif /* VERILATOR */")
            self._ind = ind
        self.println()

    def gen_task_dispatch(self, api):
        self.println("virtual task invokeTask(")
        self.inc_ind()
        self.println("output pyhdl_if::PyObject retval,")
        self.println("input string method,")
        self.println("input pyhdl_if::PyObject args);")
        self.dec_ind()
        self.println()
        self.inc_ind()
        self.println("retval = pyhdl_if::None;");
        self.println()
        self.println("case (method)")
        self.inc_ind()
        for m in api.methods:
            if m.kind == MethodKind.ImpTask:
                self.println("\"%s\": begin" % m.name)
                self.inc_ind()
                if m.rtype is not None:
                    self.println("%s __retval;" % self.svtype(m.rtype))
                for i,p in enumerate(m.params):
                    self.println("%s __%s = %s(pyhdl_if::PyTuple_GetItem(args, %d));" % (
                        self.svtype(p[1]),
                        p[0],
                        self.py2sv_func(p[1]),
                        i
                    ))
                self.write("%s" % self._ind)
                self.write("%s" % m.name)
                if len(m.params) == 0:
                    self.write("(%s);\n" % ("__retval" if m.rtype is not None else ""))
                elif len(m.params) == 1:
                    self.write("(%s__%s);\n" % (
                        "__retval, " if m.rtype is not None else "",
                        m.params[0][0]))
                else:
                    self.write("(\n")
                    self.inc_ind()
                    if m.rtype is not None:
                        self.println("__retval,")
                    for i,p in enumerate(m.params):
                        self.println("__%s%s" % (
                            p[0],
                            "," if (i+1 < len(m.params)) else ");"
                        ))
                    self.dec_ind()
                if m.rtype is not None:
                    self.println("retval = %s;" % self.sv2py_func(m.rtype, "__retval"))
                self.dec_ind()
                self.println("end")
        self.println("default: begin")
        self.inc_ind()
        self.println("$display(\"Fatal: unsupported method call %0s\", method);")
        self.dec_ind()
        self.println("end")

        self.dec_ind()
        self.println("endcase")
        self.dec_ind()
        self.println("endtask")

    def gen_func_dispatch(self, api):
        self.println("virtual function pyhdl_if::PyObject invokeFunc(string method, pyhdl_if::PyObject args);")
        self.inc_ind()
        self.println("pyhdl_if::PyObject __ret = pyhdl_if::None;")
        self.println("case (method)")
        self.inc_ind()
        for m in api.methods:
            if m.kind == MethodKind.ImpFunc:
                self.println("\"%s\": begin" % m.name)
                self.inc_ind()
                if m.rtype is not None:
                    self.println("%s __rval;" % self.svtype(m.rtype))
                for i,p in enumerate(m.params):
                    self.println("%s __%s = %s(pyhdl_if::PyTuple_GetItem(args, %d));" % (
                        self.svtype(p[1]),
                        p[0],
                        self.py2sv_func(p[1]),
                        i
                    ))
                self.write("%s" % self._ind)
                if m.rtype is not None:
                    self.write("__rval = ")
                self.write("%s" % m.name)
                if len(m.params) == 0:
                    self.write("();\n")
                elif len(m.params) == 1:
                    self.write("(__%s);\n" % m.params[0][0])
                else:
                    self.write("(\n")
                    self.inc_ind()
                    for i,p in enumerate(m.params):
                        self.println("__%s%s" % (
                            p[0],
                            "," if (i+1 < len(m.params)) else ");"
                        ))
                    self.dec_ind()

                if m.rtype is not None:
                    self.println("__ret = %s;" % self.sv2py_func(m.rtype, "__rval"))
                self.dec_ind()
                self.println("end")
        self.println("default: begin")
        self.inc_ind()
        self.println("$display(\"Fatal: unsupported method call %0s\", method);")
        self.dec_ind()
        self.println("end")

        self.dec_ind()
        self.println("endcase")
        self.println()
        self.println("return __ret;")
        self.dec_ind()
        self.println("endfunction")

    def py2sv_func(self, type):
        type_m = {
            ctypes.c_bool : "PyLong_AsLong",
            ctypes.c_byte : "PyLong_AsLong",
            ctypes.c_char : "PyLong_AsLong",
            ctypes.c_double : "real",
            ctypes.c_int : "PyLong_AsLong",
            ctypes.c_int8 : "PyLong_AsLong",
            ctypes.c_int16 : "PyLong_AsLong",
            ctypes.c_int32 : "PyLong_AsLong",
            ctypes.c_int64 : "PyLong_AsLongLong",
            ctypes.c_uint8 : "PyLong_AsLong",
            ctypes.c_uint16 : "PyLong_AsLong",
            ctypes.c_uint32 : "PyLong_AsLong",
            ctypes.c_uint64 : "PyLong_AsUnsignedLongLong",
            str : "string",
            ctypes.py_object : ""
        }
        if type not in type_m.keys():
            raise Exception("Unsupported type %s" % str(type))
        return "pyhdl_if::" + type_m[type]

    def sv2py_func(self, type, var):
        type_m = {
            ctypes.c_bool : "PyLong_FromLong",
            ctypes.c_byte : "PyLong_FromLong",
            ctypes.c_char : "PyLong_FromLong",
            ctypes.c_double : "real",
            ctypes.c_int : "PyLong_FromLong",
            ctypes.c_int8 : "PyLong_FromLong",
            ctypes.c_int16 : "PyLong_FromLong",
            ctypes.c_int32 : "PyLong_FromLong",
            ctypes.c_int64 : "PyLong_FromLongLong",
            ctypes.c_uint8 : "PyLong_FromLong",
            ctypes.c_uint16 : "PyLong_FromLong",
            ctypes.c_uint32 : "PyLong_FromLong",
            ctypes.c_uint64 : "PyLong_FromUnsignedLongLong",
            str : "string"
        }
        if type in type_m.keys():
            return "pyhdl_if::%s(%s)" % (type_m[type], var)
        elif type == ctypes.py_object:
            return var
        else:
            raise Exception("Unsupported type %s" % str(type))

    def svtype(self, type):
        type_m = {
            ctypes.c_bool : "bit",
            ctypes.c_byte : "byte",
            ctypes.c_char : "byte",
            ctypes.c_double : "real",
            ctypes.c_int : "int",
            ctypes.c_int8 : "byte",
            ctypes.c_int16 : "shortint",
            ctypes.c_int32 : "int",
            ctypes.c_int64 : "longint",
            ctypes.c_uint8 : "byte unsigned",
            ctypes.c_uint16 : "shortint unsigned",
            ctypes.c_uint32 : "int unsigned",
            ctypes.c_uint64 : "longint unsigned",
            str : "string",
            ctypes.py_object : "pyhdl_if::PyObject"
        }
        if type in type_m.keys():
            return type_m[type]
        else:
            raise Exception("Unsupported type %s" % str(type))

    def println(self, ln=None):
        if ln is None:
            self._out.write("\n")
        else:
            self._out.write("%s%s\n" % (self._ind, ln))

    def write(self, s):
        self._out.write(s)

    def inc_ind(self):
        self._ind += "    "

    @property
    def ind(self):
        return self._ind

    def dec_ind(self):
        if len(self._ind) > 4:
            self._ind = self._ind[4:]
        else:
            self._ind = ""
