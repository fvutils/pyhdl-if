
/**
 * pyhdl_dpi_imports.svh
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

    typedef chandle PyObject;
    typedef chandle PyTypeObject;
    typedef int unsigned PyGILState_STATE;

    import "DPI-C" context function int _pyhdl_if_PyErr_BadArgument();

    function int PyErr_BadArgument();
        return _pyhdl_if_PyErr_BadArgument();
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyErr_CheckSignals();

    function int PyErr_CheckSignals();
        return _pyhdl_if_PyErr_CheckSignals();
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_Clear();

    function void PyErr_Clear();
        _pyhdl_if_PyErr_Clear();
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_Display(input PyObject p0, input PyObject p1, input PyObject p2);

    function void PyErr_Display(input PyObject p0, input PyObject p1, input PyObject p2);
        _pyhdl_if_PyErr_Display(p0, p1, p2);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_DisplayException(input PyObject p0);

    function void PyErr_DisplayException(input PyObject p0);
        _pyhdl_if_PyErr_DisplayException(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyErr_ExceptionMatches(input PyObject p0);

    function int PyErr_ExceptionMatches(input PyObject p0);
        return _pyhdl_if_PyErr_ExceptionMatches(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_GetHandledException();

    function PyObject PyErr_GetHandledException();
        return _pyhdl_if_PyErr_GetHandledException();
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_GetRaisedException();

    function PyObject PyErr_GetRaisedException();
        return _pyhdl_if_PyErr_GetRaisedException();
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyErr_GivenExceptionMatches(input PyObject p0, input PyObject p1);

    function int PyErr_GivenExceptionMatches(input PyObject p0, input PyObject p1);
        return _pyhdl_if_PyErr_GivenExceptionMatches(p0, p1);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_NewException(input string name, input PyObject base, input PyObject dict);

    function PyObject PyErr_NewException(input string name, input PyObject base, input PyObject dict);
        return _pyhdl_if_PyErr_NewException(name, base, dict);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_NewExceptionWithDoc(input string name, input string doc, input PyObject base, input PyObject dict);

    function PyObject PyErr_NewExceptionWithDoc(input string name, input string doc, input PyObject base, input PyObject dict);
        return _pyhdl_if_PyErr_NewExceptionWithDoc(name, doc, base, dict);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_NoMemory();

    function PyObject PyErr_NoMemory();
        return _pyhdl_if_PyErr_NoMemory();
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_Occurred();

    function PyObject PyErr_Occurred();
        return _pyhdl_if_PyErr_Occurred();
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_Print();

    function void PyErr_Print();
        _pyhdl_if_PyErr_Print();
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_PrintEx(input int p0);

    function void PyErr_PrintEx(input int p0);
        _pyhdl_if_PyErr_PrintEx(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_ProgramText(input string filename, input int lineno);

    function PyObject PyErr_ProgramText(input string filename, input int lineno);
        return _pyhdl_if_PyErr_ProgramText(filename, lineno);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_ProgramTextObject(input PyObject filename, input int lineno);

    function PyObject PyErr_ProgramTextObject(input PyObject filename, input int lineno);
        return _pyhdl_if_PyErr_ProgramTextObject(filename, lineno);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_RangedSyntaxLocationObject(input PyObject filename, input int lineno, input int col_offset, input int end_lineno, input int end_col_offset);

    function void PyErr_RangedSyntaxLocationObject(input PyObject filename, input int lineno, input int col_offset, input int end_lineno, input int end_col_offset);
        _pyhdl_if_PyErr_RangedSyntaxLocationObject(filename, lineno, col_offset, end_lineno, end_col_offset);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_Restore(input PyObject p0, input PyObject p1, input PyObject p2);

    function void PyErr_Restore(input PyObject p0, input PyObject p1, input PyObject p2);
        _pyhdl_if_PyErr_Restore(p0, p1, p2);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SetExcInfo(input PyObject p0, input PyObject p1, input PyObject p2);

    function void PyErr_SetExcInfo(input PyObject p0, input PyObject p1, input PyObject p2);
        _pyhdl_if_PyErr_SetExcInfo(p0, p1, p2);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_SetFromErrno(input PyObject p0);

    function PyObject PyErr_SetFromErrno(input PyObject p0);
        return _pyhdl_if_PyErr_SetFromErrno(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_SetFromErrnoWithFilename(input PyObject exc, input string filename);

    function PyObject PyErr_SetFromErrnoWithFilename(input PyObject exc, input string filename);
        return _pyhdl_if_PyErr_SetFromErrnoWithFilename(exc, filename);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_SetFromErrnoWithFilenameObject(input PyObject p0, input PyObject p1);

    function PyObject PyErr_SetFromErrnoWithFilenameObject(input PyObject p0, input PyObject p1);
        return _pyhdl_if_PyErr_SetFromErrnoWithFilenameObject(p0, p1);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_SetFromErrnoWithFilenameObjects(input PyObject p0, input PyObject p1, input PyObject p2);

    function PyObject PyErr_SetFromErrnoWithFilenameObjects(input PyObject p0, input PyObject p1, input PyObject p2);
        return _pyhdl_if_PyErr_SetFromErrnoWithFilenameObjects(p0, p1, p2);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SetHandledException(input PyObject p0);

    function void PyErr_SetHandledException(input PyObject p0);
        _pyhdl_if_PyErr_SetHandledException(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_SetImportError(input PyObject p0, input PyObject p1, input PyObject p2);

    function PyObject PyErr_SetImportError(input PyObject p0, input PyObject p1, input PyObject p2);
        return _pyhdl_if_PyErr_SetImportError(p0, p1, p2);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyErr_SetImportErrorSubclass(input PyObject p0, input PyObject p1, input PyObject p2, input PyObject p3);

    function PyObject PyErr_SetImportErrorSubclass(input PyObject p0, input PyObject p1, input PyObject p2, input PyObject p3);
        return _pyhdl_if_PyErr_SetImportErrorSubclass(p0, p1, p2, p3);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SetInterrupt();

    function void PyErr_SetInterrupt();
        _pyhdl_if_PyErr_SetInterrupt();
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyErr_SetInterruptEx(input int signum);

    function int PyErr_SetInterruptEx(input int signum);
        return _pyhdl_if_PyErr_SetInterruptEx(signum);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SetNone(input PyObject p0);

    function void PyErr_SetNone(input PyObject p0);
        _pyhdl_if_PyErr_SetNone(p0);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SetObject(input PyObject p0, input PyObject p1);

    function void PyErr_SetObject(input PyObject p0, input PyObject p1);
        _pyhdl_if_PyErr_SetObject(p0, p1);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SetRaisedException(input PyObject p0);

    function void PyErr_SetRaisedException(input PyObject p0);
        _pyhdl_if_PyErr_SetRaisedException(p0);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SetString(input PyObject exception, input string _string);

    function void PyErr_SetString(input PyObject exception, input string _string);
        _pyhdl_if_PyErr_SetString(exception, _string);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SyntaxLocation(input string filename, input int lineno);

    function void PyErr_SyntaxLocation(input string filename, input int lineno);
        _pyhdl_if_PyErr_SyntaxLocation(filename, lineno);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SyntaxLocationEx(input string filename, input int lineno, input int col_offset);

    function void PyErr_SyntaxLocationEx(input string filename, input int lineno, input int col_offset);
        _pyhdl_if_PyErr_SyntaxLocationEx(filename, lineno, col_offset);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_SyntaxLocationObject(input PyObject filename, input int lineno, input int col_offset);

    function void PyErr_SyntaxLocationObject(input PyObject filename, input int lineno, input int col_offset);
        _pyhdl_if_PyErr_SyntaxLocationObject(filename, lineno, col_offset);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyErr_WarnEx(input PyObject category, input string message, input longint unsigned stack_level);

    function int PyErr_WarnEx(input PyObject category, input string message, input longint unsigned stack_level);
        return _pyhdl_if_PyErr_WarnEx(category, message, stack_level);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyErr_WarnExplicit(input PyObject category, input string message, input string filename, input int lineno, input string _module, input PyObject registry);

    function int PyErr_WarnExplicit(input PyObject category, input string message, input string filename, input int lineno, input string _module, input PyObject registry);
        return _pyhdl_if_PyErr_WarnExplicit(category, message, filename, lineno, _module, registry);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyErr_WarnExplicitObject(input PyObject category, input PyObject message, input PyObject filename, input int lineno, input PyObject _module, input PyObject registry);

    function int PyErr_WarnExplicitObject(input PyObject category, input PyObject message, input PyObject filename, input int lineno, input PyObject _module, input PyObject registry);
        return _pyhdl_if_PyErr_WarnExplicitObject(category, message, filename, lineno, _module, registry);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyErr_WriteUnraisable(input PyObject p0);

    function void PyErr_WriteUnraisable(input PyObject p0);
        _pyhdl_if_PyErr_WriteUnraisable(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyEval_EvalCode(input PyObject p0, input PyObject p1, input PyObject p2);

    function PyObject PyEval_EvalCode(input PyObject p0, input PyObject p1, input PyObject p2);
        return _pyhdl_if_PyEval_EvalCode(p0, p1, p2);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyEval_GetBuiltins();

    function PyObject PyEval_GetBuiltins();
        return _pyhdl_if_PyEval_GetBuiltins();
    endfunction

    import "DPI-C" context function string _pyhdl_if_PyEval_GetFuncDesc(input PyObject p0);

    function string PyEval_GetFuncDesc(input PyObject p0);
        return _pyhdl_if_PyEval_GetFuncDesc(p0);
    endfunction

    import "DPI-C" context function string _pyhdl_if_PyEval_GetFuncName(input PyObject p0);

    function string PyEval_GetFuncName(input PyObject p0);
        return _pyhdl_if_PyEval_GetFuncName(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyEval_GetGlobals();

    function PyObject PyEval_GetGlobals();
        return _pyhdl_if_PyEval_GetGlobals();
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyEval_GetLocals();

    function PyObject PyEval_GetLocals();
        return _pyhdl_if_PyEval_GetLocals();
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyGILState_Check();

    function int PyGILState_Check();
        return _pyhdl_if_PyGILState_Check();
    endfunction

    import "DPI-C" context function PyGILState_STATE _pyhdl_if_PyGILState_Ensure();

    function PyGILState_STATE PyGILState_Ensure();
        return _pyhdl_if_PyGILState_Ensure();
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyGILState_Release(input PyGILState_STATE p0);

    function void PyGILState_Release(input PyGILState_STATE p0);
        _pyhdl_if_PyGILState_Release(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_AddModule(input string name);

    function PyObject PyImport_AddModule(input string name);
        return _pyhdl_if_PyImport_AddModule(name);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_AddModuleObject(input PyObject name);

    function PyObject PyImport_AddModuleObject(input PyObject name);
        return _pyhdl_if_PyImport_AddModuleObject(name);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_ExecCodeModule(input string name, input PyObject co);

    function PyObject PyImport_ExecCodeModule(input string name, input PyObject co);
        return _pyhdl_if_PyImport_ExecCodeModule(name, co);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_ExecCodeModuleEx(input string name, input PyObject co, input string pathname);

    function PyObject PyImport_ExecCodeModuleEx(input string name, input PyObject co, input string pathname);
        return _pyhdl_if_PyImport_ExecCodeModuleEx(name, co, pathname);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_ExecCodeModuleObject(input PyObject name, input PyObject co, input PyObject pathname, input PyObject cpathname);

    function PyObject PyImport_ExecCodeModuleObject(input PyObject name, input PyObject co, input PyObject pathname, input PyObject cpathname);
        return _pyhdl_if_PyImport_ExecCodeModuleObject(name, co, pathname, cpathname);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_ExecCodeModuleWithPathnames(input string name, input PyObject co, input string pathname, input string cpathname);

    function PyObject PyImport_ExecCodeModuleWithPathnames(input string name, input PyObject co, input string pathname, input string cpathname);
        return _pyhdl_if_PyImport_ExecCodeModuleWithPathnames(name, co, pathname, cpathname);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_GetImporter(input PyObject path);

    function PyObject PyImport_GetImporter(input PyObject path);
        return _pyhdl_if_PyImport_GetImporter(path);
    endfunction

    import "DPI-C" context function longint _pyhdl_if_PyImport_GetMagicNumber();

    function longint PyImport_GetMagicNumber();
        return _pyhdl_if_PyImport_GetMagicNumber();
    endfunction

    import "DPI-C" context function string _pyhdl_if_PyImport_GetMagicTag();

    function string PyImport_GetMagicTag();
        return _pyhdl_if_PyImport_GetMagicTag();
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_GetModule(input PyObject name);

    function PyObject PyImport_GetModule(input PyObject name);
        return _pyhdl_if_PyImport_GetModule(name);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_GetModuleDict();

    function PyObject PyImport_GetModuleDict();
        return _pyhdl_if_PyImport_GetModuleDict();
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_Import(input PyObject name);

    function PyObject PyImport_Import(input PyObject name);
        return _pyhdl_if_PyImport_Import(name);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyImport_ImportFrozenModule(input string name);

    function int PyImport_ImportFrozenModule(input string name);
        return _pyhdl_if_PyImport_ImportFrozenModule(name);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyImport_ImportFrozenModuleObject(input PyObject name);

    function int PyImport_ImportFrozenModuleObject(input PyObject name);
        return _pyhdl_if_PyImport_ImportFrozenModuleObject(name);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_ImportModule(input string name);

    function PyObject PyImport_ImportModule(input string name);
        return _pyhdl_if_PyImport_ImportModule(name);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_ImportModuleLevel(input string name, input PyObject globals, input PyObject locals, input PyObject fromlist, input int level);

    function PyObject PyImport_ImportModuleLevel(input string name, input PyObject globals, input PyObject locals, input PyObject fromlist, input int level);
        return _pyhdl_if_PyImport_ImportModuleLevel(name, globals, locals, fromlist, level);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_ImportModuleLevelObject(input PyObject name, input PyObject globals, input PyObject locals, input PyObject fromlist, input int level);

    function PyObject PyImport_ImportModuleLevelObject(input PyObject name, input PyObject globals, input PyObject locals, input PyObject fromlist, input int level);
        return _pyhdl_if_PyImport_ImportModuleLevelObject(name, globals, locals, fromlist, level);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_ImportModuleNoBlock(input string name);

    function PyObject PyImport_ImportModuleNoBlock(input string name);
        return _pyhdl_if_PyImport_ImportModuleNoBlock(name);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyImport_ReloadModule(input PyObject m);

    function PyObject PyImport_ReloadModule(input PyObject m);
        return _pyhdl_if_PyImport_ReloadModule(m);
    endfunction

    import "DPI-C" context function real _pyhdl_if_PyLong_AsDouble(input PyObject p0);

    function real PyLong_AsDouble(input PyObject p0);
        return _pyhdl_if_PyLong_AsDouble(p0);
    endfunction

    import "DPI-C" context function longint _pyhdl_if_PyLong_AsLong(input PyObject p0);

    function longint PyLong_AsLong(input PyObject p0);
        return _pyhdl_if_PyLong_AsLong(p0);
    endfunction

    import "DPI-C" context function longint _pyhdl_if_PyLong_AsLongAndOverflow(input PyObject p0, output int p1);

    function longint PyLong_AsLongAndOverflow(input PyObject p0, output int p1);
        return _pyhdl_if_PyLong_AsLongAndOverflow(p0, p1);
    endfunction

    import "DPI-C" context function longint _pyhdl_if_PyLong_AsLongLong(input PyObject p0);

    function longint PyLong_AsLongLong(input PyObject p0);
        return _pyhdl_if_PyLong_AsLongLong(p0);
    endfunction

    import "DPI-C" context function longint _pyhdl_if_PyLong_AsLongLongAndOverflow(input PyObject p0, output int p1);

    function longint PyLong_AsLongLongAndOverflow(input PyObject p0, output int p1);
        return _pyhdl_if_PyLong_AsLongLongAndOverflow(p0, p1);
    endfunction

    import "DPI-C" context function int unsigned _pyhdl_if_PyLong_AsSize_t(input PyObject p0);

    function int unsigned PyLong_AsSize_t(input PyObject p0);
        return _pyhdl_if_PyLong_AsSize_t(p0);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyLong_AsSsize_t(input PyObject p0);

    function longint unsigned PyLong_AsSsize_t(input PyObject p0);
        return _pyhdl_if_PyLong_AsSsize_t(p0);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyLong_AsUnsignedLong(input PyObject p0);

    function longint unsigned PyLong_AsUnsignedLong(input PyObject p0);
        return _pyhdl_if_PyLong_AsUnsignedLong(p0);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyLong_AsUnsignedLongLong(input PyObject p0);

    function longint unsigned PyLong_AsUnsignedLongLong(input PyObject p0);
        return _pyhdl_if_PyLong_AsUnsignedLongLong(p0);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyLong_AsUnsignedLongLongMask(input PyObject p0);

    function longint unsigned PyLong_AsUnsignedLongLongMask(input PyObject p0);
        return _pyhdl_if_PyLong_AsUnsignedLongLongMask(p0);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyLong_AsUnsignedLongMask(input PyObject p0);

    function longint unsigned PyLong_AsUnsignedLongMask(input PyObject p0);
        return _pyhdl_if_PyLong_AsUnsignedLongMask(p0);
    endfunction

    import "DPI-C" context function chandle _pyhdl_if_PyLong_AsVoidPtr(input PyObject p0);

    function chandle PyLong_AsVoidPtr(input PyObject p0);
        return _pyhdl_if_PyLong_AsVoidPtr(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromDouble(input real p0);

    function PyObject PyLong_FromDouble(input real p0);
        return _pyhdl_if_PyLong_FromDouble(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromLong(input longint p0);

    function PyObject PyLong_FromLong(input longint p0);
        return _pyhdl_if_PyLong_FromLong(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromLongLong(input longint p0);

    function PyObject PyLong_FromLongLong(input longint p0);
        return _pyhdl_if_PyLong_FromLongLong(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromSize_t(input int unsigned p0);

    function PyObject PyLong_FromSize_t(input int unsigned p0);
        return _pyhdl_if_PyLong_FromSize_t(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromSsize_t(input longint unsigned p0);

    function PyObject PyLong_FromSsize_t(input longint unsigned p0);
        return _pyhdl_if_PyLong_FromSsize_t(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromString(input string p0, output chandle p1, input int p2);

    function PyObject PyLong_FromString(input string p0, output chandle p1, input int p2);
        return _pyhdl_if_PyLong_FromString(p0, p1, p2);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromUnicodeObject(input PyObject u, input int base);

    function PyObject PyLong_FromUnicodeObject(input PyObject u, input int base);
        return _pyhdl_if_PyLong_FromUnicodeObject(u, base);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromUnsignedLong(input longint unsigned p0);

    function PyObject PyLong_FromUnsignedLong(input longint unsigned p0);
        return _pyhdl_if_PyLong_FromUnsignedLong(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromUnsignedLongLong(input longint unsigned p0);

    function PyObject PyLong_FromUnsignedLongLong(input longint unsigned p0);
        return _pyhdl_if_PyLong_FromUnsignedLongLong(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_FromVoidPtr(input chandle p0);

    function PyObject PyLong_FromVoidPtr(input chandle p0);
        return _pyhdl_if_PyLong_FromVoidPtr(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyLong_GetInfo();

    function PyObject PyLong_GetInfo();
        return _pyhdl_if_PyLong_GetInfo();
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_ASCII(input PyObject p0);

    function PyObject PyObject_ASCII(input PyObject p0);
        return _pyhdl_if_PyObject_ASCII(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_AsFileDescriptor(input PyObject p0);

    function int PyObject_AsFileDescriptor(input PyObject p0);
        return _pyhdl_if_PyObject_AsFileDescriptor(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_Bytes(input PyObject p0);

    function PyObject PyObject_Bytes(input PyObject p0);
        return _pyhdl_if_PyObject_Bytes(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_Call(input PyObject callable, input PyObject args, input PyObject kwargs);

    function PyObject PyObject_Call(input PyObject callable, input PyObject args, input PyObject kwargs);
        return _pyhdl_if_PyObject_Call(callable, args, kwargs);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyObject_CallFinalizer(input PyObject p0);

    function void PyObject_CallFinalizer(input PyObject p0);
        _pyhdl_if_PyObject_CallFinalizer(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_CallFinalizerFromDealloc(input PyObject p0);

    function int PyObject_CallFinalizerFromDealloc(input PyObject p0);
        return _pyhdl_if_PyObject_CallFinalizerFromDealloc(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_CallNoArgs(input PyObject func);

    function PyObject PyObject_CallNoArgs(input PyObject func);
        return _pyhdl_if_PyObject_CallNoArgs(func);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_CallObject(input PyObject callable, input PyObject args);

    function PyObject PyObject_CallObject(input PyObject callable, input PyObject args);
        return _pyhdl_if_PyObject_CallObject(callable, args);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_CallOneArg(input PyObject func, input PyObject arg);

    function PyObject PyObject_CallOneArg(input PyObject func, input PyObject arg);
        return _pyhdl_if_PyObject_CallOneArg(func, arg);
    endfunction

    import "DPI-C" context function chandle _pyhdl_if_PyObject_Calloc(input int unsigned nelem, input int unsigned elsize);

    function chandle PyObject_Calloc(input int unsigned nelem, input int unsigned elsize);
        return _pyhdl_if_PyObject_Calloc(nelem, elsize);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_CheckBuffer(input PyObject obj);

    function int PyObject_CheckBuffer(input PyObject obj);
        return _pyhdl_if_PyObject_CheckBuffer(obj);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyObject_ClearWeakRefs(input PyObject p0);

    function void PyObject_ClearWeakRefs(input PyObject p0);
        _pyhdl_if_PyObject_ClearWeakRefs(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_CopyData(input PyObject dest, input PyObject src);

    function int PyObject_CopyData(input PyObject dest, input PyObject src);
        return _pyhdl_if_PyObject_CopyData(dest, src);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_DelItem(input PyObject o, input PyObject key);

    function int PyObject_DelItem(input PyObject o, input PyObject key);
        return _pyhdl_if_PyObject_DelItem(o, key);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_DelItemString(input PyObject o, input string key);

    function int PyObject_DelItemString(input PyObject o, input string key);
        return _pyhdl_if_PyObject_DelItemString(o, key);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_Dir(input PyObject p0);

    function PyObject PyObject_Dir(input PyObject p0);
        return _pyhdl_if_PyObject_Dir(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_Format(input PyObject obj, input PyObject format_spec);

    function PyObject PyObject_Format(input PyObject obj, input PyObject format_spec);
        return _pyhdl_if_PyObject_Format(obj, format_spec);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyObject_Free(input chandle ptr);

    function void PyObject_Free(input chandle ptr);
        _pyhdl_if_PyObject_Free(ptr);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyObject_GC_Del(input chandle p0);

    function void PyObject_GC_Del(input chandle p0);
        _pyhdl_if_PyObject_GC_Del(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_GC_IsFinalized(input PyObject p0);

    function int PyObject_GC_IsFinalized(input PyObject p0);
        return _pyhdl_if_PyObject_GC_IsFinalized(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_GC_IsTracked(input PyObject p0);

    function int PyObject_GC_IsTracked(input PyObject p0);
        return _pyhdl_if_PyObject_GC_IsTracked(p0);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyObject_GC_Track(input chandle p0);

    function void PyObject_GC_Track(input chandle p0);
        _pyhdl_if_PyObject_GC_Track(p0);
    endfunction

    import "DPI-C" context function void _pyhdl_if_PyObject_GC_UnTrack(input chandle p0);

    function void PyObject_GC_UnTrack(input chandle p0);
        _pyhdl_if_PyObject_GC_UnTrack(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_GenericGetAttr(input PyObject p0, input PyObject p1);

    function PyObject PyObject_GenericGetAttr(input PyObject p0, input PyObject p1);
        return _pyhdl_if_PyObject_GenericGetAttr(p0, p1);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_GenericGetDict(input PyObject p0, input chandle p1);

    function PyObject PyObject_GenericGetDict(input PyObject p0, input chandle p1);
        return _pyhdl_if_PyObject_GenericGetDict(p0, p1);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_GenericSetAttr(input PyObject p0, input PyObject p1, input PyObject p2);

    function int PyObject_GenericSetAttr(input PyObject p0, input PyObject p1, input PyObject p2);
        return _pyhdl_if_PyObject_GenericSetAttr(p0, p1, p2);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_GenericSetDict(input PyObject p0, input PyObject p1, input chandle p2);

    function int PyObject_GenericSetDict(input PyObject p0, input PyObject p1, input chandle p2);
        return _pyhdl_if_PyObject_GenericSetDict(p0, p1, p2);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_GetAIter(input PyObject p0);

    function PyObject PyObject_GetAIter(input PyObject p0);
        return _pyhdl_if_PyObject_GetAIter(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_GetAttr(input PyObject p0, input PyObject p1);

    function PyObject PyObject_GetAttr(input PyObject p0, input PyObject p1);
        return _pyhdl_if_PyObject_GetAttr(p0, p1);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_GetAttrString(input PyObject p0, input string p1);

    function PyObject PyObject_GetAttrString(input PyObject p0, input string p1);
        return _pyhdl_if_PyObject_GetAttrString(p0, p1);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_GetItem(input PyObject o, input PyObject key);

    function PyObject PyObject_GetItem(input PyObject o, input PyObject key);
        return _pyhdl_if_PyObject_GetItem(o, key);
    endfunction

    import "DPI-C" context function chandle _pyhdl_if_PyObject_GetItemData(input PyObject obj);

    function chandle PyObject_GetItemData(input PyObject obj);
        return _pyhdl_if_PyObject_GetItemData(obj);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_GetIter(input PyObject p0);

    function PyObject PyObject_GetIter(input PyObject p0);
        return _pyhdl_if_PyObject_GetIter(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_HasAttr(input PyObject p0, input PyObject p1);

    function int PyObject_HasAttr(input PyObject p0, input PyObject p1);
        return _pyhdl_if_PyObject_HasAttr(p0, p1);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_HasAttrString(input PyObject p0, input string p1);

    function int PyObject_HasAttrString(input PyObject p0, input string p1);
        return _pyhdl_if_PyObject_HasAttrString(p0, p1);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_IS_GC(input PyObject obj);

    function int PyObject_IS_GC(input PyObject obj);
        return _pyhdl_if_PyObject_IS_GC(obj);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_Init(input PyObject p0, input PyTypeObject p1);

    function PyObject PyObject_Init(input PyObject p0, input PyTypeObject p1);
        return _pyhdl_if_PyObject_Init(p0, p1);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_IsInstance(input PyObject object, input PyObject typeorclass);

    function int PyObject_IsInstance(input PyObject object, input PyObject typeorclass);
        return _pyhdl_if_PyObject_IsInstance(object, typeorclass);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_IsSubclass(input PyObject object, input PyObject typeorclass);

    function int PyObject_IsSubclass(input PyObject object, input PyObject typeorclass);
        return _pyhdl_if_PyObject_IsSubclass(object, typeorclass);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_IsTrue(input PyObject p0);

    function int PyObject_IsTrue(input PyObject p0);
        return _pyhdl_if_PyObject_IsTrue(p0);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyObject_LengthHint(input PyObject o, input longint unsigned p1);

    function longint unsigned PyObject_LengthHint(input PyObject o, input longint unsigned p1);
        return _pyhdl_if_PyObject_LengthHint(o, p1);
    endfunction

    import "DPI-C" context function chandle _pyhdl_if_PyObject_Malloc(input int unsigned size);

    function chandle PyObject_Malloc(input int unsigned size);
        return _pyhdl_if_PyObject_Malloc(size);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_Not(input PyObject p0);

    function int PyObject_Not(input PyObject p0);
        return _pyhdl_if_PyObject_Not(p0);
    endfunction

    import "DPI-C" context function chandle _pyhdl_if_PyObject_Realloc(input chandle ptr, input int unsigned new_size);

    function chandle PyObject_Realloc(input chandle ptr, input int unsigned new_size);
        return _pyhdl_if_PyObject_Realloc(ptr, new_size);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_Repr(input PyObject p0);

    function PyObject PyObject_Repr(input PyObject p0);
        return _pyhdl_if_PyObject_Repr(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_RichCompare(input PyObject p0, input PyObject p1, input int p2);

    function PyObject PyObject_RichCompare(input PyObject p0, input PyObject p1, input int p2);
        return _pyhdl_if_PyObject_RichCompare(p0, p1, p2);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_RichCompareBool(input PyObject p0, input PyObject p1, input int p2);

    function int PyObject_RichCompareBool(input PyObject p0, input PyObject p1, input int p2);
        return _pyhdl_if_PyObject_RichCompareBool(p0, p1, p2);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_SelfIter(input PyObject p0);

    function PyObject PyObject_SelfIter(input PyObject p0);
        return _pyhdl_if_PyObject_SelfIter(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_SetAttr(input PyObject p0, input PyObject p1, input PyObject p2);

    function int PyObject_SetAttr(input PyObject p0, input PyObject p1, input PyObject p2);
        return _pyhdl_if_PyObject_SetAttr(p0, p1, p2);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_SetAttrString(input PyObject p0, input string p1, input PyObject p2);

    function int PyObject_SetAttrString(input PyObject p0, input string p1, input PyObject p2);
        return _pyhdl_if_PyObject_SetAttrString(p0, p1, p2);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyObject_SetItem(input PyObject o, input PyObject key, input PyObject v);

    function int PyObject_SetItem(input PyObject o, input PyObject key, input PyObject v);
        return _pyhdl_if_PyObject_SetItem(o, key, v);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyObject_Size(input PyObject o);

    function longint unsigned PyObject_Size(input PyObject o);
        return _pyhdl_if_PyObject_Size(o);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_Str(input PyObject p0);

    function PyObject PyObject_Str(input PyObject p0);
        return _pyhdl_if_PyObject_Str(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyObject_Type(input PyObject o);

    function PyObject PyObject_Type(input PyObject o);
        return _pyhdl_if_PyObject_Type(o);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyTuple_GetItem(input PyObject p0, input longint unsigned p1);

    function PyObject PyTuple_GetItem(input PyObject p0, input longint unsigned p1);
        return _pyhdl_if_PyTuple_GetItem(p0, p1);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyTuple_GetSlice(input PyObject p0, input longint unsigned p1, input longint unsigned p2);

    function PyObject PyTuple_GetSlice(input PyObject p0, input longint unsigned p1, input longint unsigned p2);
        return _pyhdl_if_PyTuple_GetSlice(p0, p1, p2);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyTuple_New(input longint unsigned size);

    function PyObject PyTuple_New(input longint unsigned size);
        return _pyhdl_if_PyTuple_New(size);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyTuple_SetItem(input PyObject p0, input longint unsigned p1, input PyObject p2);

    function int PyTuple_SetItem(input PyObject p0, input longint unsigned p1, input PyObject p2);
        return _pyhdl_if_PyTuple_SetItem(p0, p1, p2);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyTuple_Size(input PyObject p0);

    function longint unsigned PyTuple_Size(input PyObject p0);
        return _pyhdl_if_PyTuple_Size(p0);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsASCIIString(input PyObject unicode);

    function PyObject PyUnicode_AsASCIIString(input PyObject unicode);
        return _pyhdl_if_PyUnicode_AsASCIIString(unicode);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsCharmapString(input PyObject unicode, input PyObject mapping);

    function PyObject PyUnicode_AsCharmapString(input PyObject unicode, input PyObject mapping);
        return _pyhdl_if_PyUnicode_AsCharmapString(unicode, mapping);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsDecodedObject(input PyObject unicode, input string encoding, input string errors);

    function PyObject PyUnicode_AsDecodedObject(input PyObject unicode, input string encoding, input string errors);
        return _pyhdl_if_PyUnicode_AsDecodedObject(unicode, encoding, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsDecodedUnicode(input PyObject unicode, input string encoding, input string errors);

    function PyObject PyUnicode_AsDecodedUnicode(input PyObject unicode, input string encoding, input string errors);
        return _pyhdl_if_PyUnicode_AsDecodedUnicode(unicode, encoding, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsEncodedObject(input PyObject unicode, input string encoding, input string errors);

    function PyObject PyUnicode_AsEncodedObject(input PyObject unicode, input string encoding, input string errors);
        return _pyhdl_if_PyUnicode_AsEncodedObject(unicode, encoding, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsEncodedString(input PyObject unicode, input string encoding, input string errors);

    function PyObject PyUnicode_AsEncodedString(input PyObject unicode, input string encoding, input string errors);
        return _pyhdl_if_PyUnicode_AsEncodedString(unicode, encoding, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsEncodedUnicode(input PyObject unicode, input string encoding, input string errors);

    function PyObject PyUnicode_AsEncodedUnicode(input PyObject unicode, input string encoding, input string errors);
        return _pyhdl_if_PyUnicode_AsEncodedUnicode(unicode, encoding, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsLatin1String(input PyObject unicode);

    function PyObject PyUnicode_AsLatin1String(input PyObject unicode);
        return _pyhdl_if_PyUnicode_AsLatin1String(unicode);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsRawUnicodeEscapeString(input PyObject unicode);

    function PyObject PyUnicode_AsRawUnicodeEscapeString(input PyObject unicode);
        return _pyhdl_if_PyUnicode_AsRawUnicodeEscapeString(unicode);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsUTF16String(input PyObject unicode);

    function PyObject PyUnicode_AsUTF16String(input PyObject unicode);
        return _pyhdl_if_PyUnicode_AsUTF16String(unicode);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsUTF32String(input PyObject unicode);

    function PyObject PyUnicode_AsUTF32String(input PyObject unicode);
        return _pyhdl_if_PyUnicode_AsUTF32String(unicode);
    endfunction

    import "DPI-C" context function string _pyhdl_if_PyUnicode_AsUTF8(input PyObject unicode);

    function string PyUnicode_AsUTF8(input PyObject unicode);
        return _pyhdl_if_PyUnicode_AsUTF8(unicode);
    endfunction

    import "DPI-C" context function string _pyhdl_if_PyUnicode_AsUTF8AndSize(input PyObject unicode, output longint unsigned size);

    function string PyUnicode_AsUTF8AndSize(input PyObject unicode, output longint unsigned size);
        return _pyhdl_if_PyUnicode_AsUTF8AndSize(unicode, size);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsUTF8String(input PyObject unicode);

    function PyObject PyUnicode_AsUTF8String(input PyObject unicode);
        return _pyhdl_if_PyUnicode_AsUTF8String(unicode);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_AsUnicodeEscapeString(input PyObject unicode);

    function PyObject PyUnicode_AsUnicodeEscapeString(input PyObject unicode);
        return _pyhdl_if_PyUnicode_AsUnicodeEscapeString(unicode);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyUnicode_AsWideChar(input PyObject unicode, input string w, input longint unsigned size);

    function longint unsigned PyUnicode_AsWideChar(input PyObject unicode, input string w, input longint unsigned size);
        return _pyhdl_if_PyUnicode_AsWideChar(unicode, w, size);
    endfunction

    import "DPI-C" context function string _pyhdl_if_PyUnicode_AsWideCharString(input PyObject unicode, output longint unsigned size);

    function string PyUnicode_AsWideCharString(input PyObject unicode, output longint unsigned size);
        return _pyhdl_if_PyUnicode_AsWideCharString(unicode, size);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_BuildEncodingMap(input PyObject _string);

    function PyObject PyUnicode_BuildEncodingMap(input PyObject _string);
        return _pyhdl_if_PyUnicode_BuildEncodingMap(_string);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyUnicode_Compare(input PyObject left, input PyObject right);

    function int PyUnicode_Compare(input PyObject left, input PyObject right);
        return _pyhdl_if_PyUnicode_Compare(left, right);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyUnicode_CompareWithASCIIString(input PyObject left, input string right);

    function int PyUnicode_CompareWithASCIIString(input PyObject left, input string right);
        return _pyhdl_if_PyUnicode_CompareWithASCIIString(left, right);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Concat(input PyObject left, input PyObject right);

    function PyObject PyUnicode_Concat(input PyObject left, input PyObject right);
        return _pyhdl_if_PyUnicode_Concat(left, right);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyUnicode_Contains(input PyObject container, input PyObject element);

    function int PyUnicode_Contains(input PyObject container, input PyObject element);
        return _pyhdl_if_PyUnicode_Contains(container, element);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyUnicode_CopyCharacters(input PyObject to, input longint unsigned to_start, input PyObject from, input longint unsigned from_start, input longint unsigned how_many);

    function longint unsigned PyUnicode_CopyCharacters(input PyObject to, input longint unsigned to_start, input PyObject from, input longint unsigned from_start, input longint unsigned how_many);
        return _pyhdl_if_PyUnicode_CopyCharacters(to, to_start, from, from_start, how_many);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyUnicode_Count(input PyObject str, input PyObject substr, input longint unsigned start, input longint unsigned _end);

    function longint unsigned PyUnicode_Count(input PyObject str, input PyObject substr, input longint unsigned start, input longint unsigned _end);
        return _pyhdl_if_PyUnicode_Count(str, substr, start, _end);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Decode(input string s, input longint unsigned size, input string encoding, input string errors);

    function PyObject PyUnicode_Decode(input string s, input longint unsigned size, input string encoding, input string errors);
        return _pyhdl_if_PyUnicode_Decode(s, size, encoding, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeASCII(input string _string, input longint unsigned length, input string errors);

    function PyObject PyUnicode_DecodeASCII(input string _string, input longint unsigned length, input string errors);
        return _pyhdl_if_PyUnicode_DecodeASCII(_string, length, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeCharmap(input string _string, input longint unsigned length, input PyObject mapping, input string errors);

    function PyObject PyUnicode_DecodeCharmap(input string _string, input longint unsigned length, input PyObject mapping, input string errors);
        return _pyhdl_if_PyUnicode_DecodeCharmap(_string, length, mapping, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeFSDefault(input string s);

    function PyObject PyUnicode_DecodeFSDefault(input string s);
        return _pyhdl_if_PyUnicode_DecodeFSDefault(s);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeFSDefaultAndSize(input string s, input longint unsigned size);

    function PyObject PyUnicode_DecodeFSDefaultAndSize(input string s, input longint unsigned size);
        return _pyhdl_if_PyUnicode_DecodeFSDefaultAndSize(s, size);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeLatin1(input string _string, input longint unsigned length, input string errors);

    function PyObject PyUnicode_DecodeLatin1(input string _string, input longint unsigned length, input string errors);
        return _pyhdl_if_PyUnicode_DecodeLatin1(_string, length, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeLocale(input string str, input string errors);

    function PyObject PyUnicode_DecodeLocale(input string str, input string errors);
        return _pyhdl_if_PyUnicode_DecodeLocale(str, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeLocaleAndSize(input string str, input longint unsigned len, input string errors);

    function PyObject PyUnicode_DecodeLocaleAndSize(input string str, input longint unsigned len, input string errors);
        return _pyhdl_if_PyUnicode_DecodeLocaleAndSize(str, len, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeRawUnicodeEscape(input string _string, input longint unsigned length, input string errors);

    function PyObject PyUnicode_DecodeRawUnicodeEscape(input string _string, input longint unsigned length, input string errors);
        return _pyhdl_if_PyUnicode_DecodeRawUnicodeEscape(_string, length, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeUTF16(input string _string, input longint unsigned length, input string errors, output int byteorder);

    function PyObject PyUnicode_DecodeUTF16(input string _string, input longint unsigned length, input string errors, output int byteorder);
        return _pyhdl_if_PyUnicode_DecodeUTF16(_string, length, errors, byteorder);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeUTF16Stateful(input string _string, input longint unsigned length, input string errors, output int byteorder, output longint unsigned consumed);

    function PyObject PyUnicode_DecodeUTF16Stateful(input string _string, input longint unsigned length, input string errors, output int byteorder, output longint unsigned consumed);
        return _pyhdl_if_PyUnicode_DecodeUTF16Stateful(_string, length, errors, byteorder, consumed);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeUTF32(input string _string, input longint unsigned length, input string errors, output int byteorder);

    function PyObject PyUnicode_DecodeUTF32(input string _string, input longint unsigned length, input string errors, output int byteorder);
        return _pyhdl_if_PyUnicode_DecodeUTF32(_string, length, errors, byteorder);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeUTF32Stateful(input string _string, input longint unsigned length, input string errors, output int byteorder, output longint unsigned consumed);

    function PyObject PyUnicode_DecodeUTF32Stateful(input string _string, input longint unsigned length, input string errors, output int byteorder, output longint unsigned consumed);
        return _pyhdl_if_PyUnicode_DecodeUTF32Stateful(_string, length, errors, byteorder, consumed);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeUTF7(input string _string, input longint unsigned length, input string errors);

    function PyObject PyUnicode_DecodeUTF7(input string _string, input longint unsigned length, input string errors);
        return _pyhdl_if_PyUnicode_DecodeUTF7(_string, length, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeUTF7Stateful(input string _string, input longint unsigned length, input string errors, output longint unsigned consumed);

    function PyObject PyUnicode_DecodeUTF7Stateful(input string _string, input longint unsigned length, input string errors, output longint unsigned consumed);
        return _pyhdl_if_PyUnicode_DecodeUTF7Stateful(_string, length, errors, consumed);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeUTF8(input string _string, input longint unsigned length, input string errors);

    function PyObject PyUnicode_DecodeUTF8(input string _string, input longint unsigned length, input string errors);
        return _pyhdl_if_PyUnicode_DecodeUTF8(_string, length, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeUTF8Stateful(input string _string, input longint unsigned length, input string errors, output longint unsigned consumed);

    function PyObject PyUnicode_DecodeUTF8Stateful(input string _string, input longint unsigned length, input string errors, output longint unsigned consumed);
        return _pyhdl_if_PyUnicode_DecodeUTF8Stateful(_string, length, errors, consumed);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_DecodeUnicodeEscape(input string _string, input longint unsigned length, input string errors);

    function PyObject PyUnicode_DecodeUnicodeEscape(input string _string, input longint unsigned length, input string errors);
        return _pyhdl_if_PyUnicode_DecodeUnicodeEscape(_string, length, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_EncodeFSDefault(input PyObject unicode);

    function PyObject PyUnicode_EncodeFSDefault(input PyObject unicode);
        return _pyhdl_if_PyUnicode_EncodeFSDefault(unicode);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_EncodeLocale(input PyObject unicode, input string errors);

    function PyObject PyUnicode_EncodeLocale(input PyObject unicode, input string errors);
        return _pyhdl_if_PyUnicode_EncodeLocale(unicode, errors);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyUnicode_FSConverter(input PyObject p0, input chandle p1);

    function int PyUnicode_FSConverter(input PyObject p0, input chandle p1);
        return _pyhdl_if_PyUnicode_FSConverter(p0, p1);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyUnicode_FSDecoder(input PyObject p0, input chandle p1);

    function int PyUnicode_FSDecoder(input PyObject p0, input chandle p1);
        return _pyhdl_if_PyUnicode_FSDecoder(p0, p1);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyUnicode_Find(input PyObject str, input PyObject substr, input longint unsigned start, input longint unsigned _end, input int direction);

    function longint unsigned PyUnicode_Find(input PyObject str, input PyObject substr, input longint unsigned start, input longint unsigned _end, input int direction);
        return _pyhdl_if_PyUnicode_Find(str, substr, start, _end, direction);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Format(input PyObject format, input PyObject args);

    function PyObject PyUnicode_Format(input PyObject format, input PyObject args);
        return _pyhdl_if_PyUnicode_Format(format, args);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_FromEncodedObject(input PyObject obj, input string encoding, input string errors);

    function PyObject PyUnicode_FromEncodedObject(input PyObject obj, input string encoding, input string errors);
        return _pyhdl_if_PyUnicode_FromEncodedObject(obj, encoding, errors);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_FromObject(input PyObject obj);

    function PyObject PyUnicode_FromObject(input PyObject obj);
        return _pyhdl_if_PyUnicode_FromObject(obj);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_FromOrdinal(input int ordinal);

    function PyObject PyUnicode_FromOrdinal(input int ordinal);
        return _pyhdl_if_PyUnicode_FromOrdinal(ordinal);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_FromString(input string u);

    function PyObject PyUnicode_FromString(input string u);
        return _pyhdl_if_PyUnicode_FromString(u);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_FromStringAndSize(input string u, input longint unsigned size);

    function PyObject PyUnicode_FromStringAndSize(input string u, input longint unsigned size);
        return _pyhdl_if_PyUnicode_FromStringAndSize(u, size);
    endfunction

    import "DPI-C" context function string _pyhdl_if_PyUnicode_GetDefaultEncoding();

    function string PyUnicode_GetDefaultEncoding();
        return _pyhdl_if_PyUnicode_GetDefaultEncoding();
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyUnicode_GetLength(input PyObject unicode);

    function longint unsigned PyUnicode_GetLength(input PyObject unicode);
        return _pyhdl_if_PyUnicode_GetLength(unicode);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_InternFromString(input string u);

    function PyObject PyUnicode_InternFromString(input string u);
        return _pyhdl_if_PyUnicode_InternFromString(u);
    endfunction

    import "DPI-C" context function int _pyhdl_if_PyUnicode_IsIdentifier(input PyObject s);

    function int PyUnicode_IsIdentifier(input PyObject s);
        return _pyhdl_if_PyUnicode_IsIdentifier(s);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Join(input PyObject separator, input PyObject seq);

    function PyObject PyUnicode_Join(input PyObject separator, input PyObject seq);
        return _pyhdl_if_PyUnicode_Join(separator, seq);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Partition(input PyObject s, input PyObject sep);

    function PyObject PyUnicode_Partition(input PyObject s, input PyObject sep);
        return _pyhdl_if_PyUnicode_Partition(s, sep);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_RPartition(input PyObject s, input PyObject sep);

    function PyObject PyUnicode_RPartition(input PyObject s, input PyObject sep);
        return _pyhdl_if_PyUnicode_RPartition(s, sep);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_RSplit(input PyObject s, input PyObject sep, input longint unsigned maxsplit);

    function PyObject PyUnicode_RSplit(input PyObject s, input PyObject sep, input longint unsigned maxsplit);
        return _pyhdl_if_PyUnicode_RSplit(s, sep, maxsplit);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Replace(input PyObject str, input PyObject substr, input PyObject replstr, input longint unsigned maxcount);

    function PyObject PyUnicode_Replace(input PyObject str, input PyObject substr, input PyObject replstr, input longint unsigned maxcount);
        return _pyhdl_if_PyUnicode_Replace(str, substr, replstr, maxcount);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_RichCompare(input PyObject left, input PyObject right, input int op);

    function PyObject PyUnicode_RichCompare(input PyObject left, input PyObject right, input int op);
        return _pyhdl_if_PyUnicode_RichCompare(left, right, op);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Split(input PyObject s, input PyObject sep, input longint unsigned maxsplit);

    function PyObject PyUnicode_Split(input PyObject s, input PyObject sep, input longint unsigned maxsplit);
        return _pyhdl_if_PyUnicode_Split(s, sep, maxsplit);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Splitlines(input PyObject s, input int keepends);

    function PyObject PyUnicode_Splitlines(input PyObject s, input int keepends);
        return _pyhdl_if_PyUnicode_Splitlines(s, keepends);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Substring(input PyObject str, input longint unsigned start, input longint unsigned _end);

    function PyObject PyUnicode_Substring(input PyObject str, input longint unsigned start, input longint unsigned _end);
        return _pyhdl_if_PyUnicode_Substring(str, start, _end);
    endfunction

    import "DPI-C" context function longint unsigned _pyhdl_if_PyUnicode_Tailmatch(input PyObject str, input PyObject substr, input longint unsigned start, input longint unsigned _end, input int direction);

    function longint unsigned PyUnicode_Tailmatch(input PyObject str, input PyObject substr, input longint unsigned start, input longint unsigned _end, input int direction);
        return _pyhdl_if_PyUnicode_Tailmatch(str, substr, start, _end, direction);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_PyUnicode_Translate(input PyObject str, input PyObject _table, input string errors);

    function PyObject PyUnicode_Translate(input PyObject str, input PyObject _table, input string errors);
        return _pyhdl_if_PyUnicode_Translate(str, _table, errors);
    endfunction

    import "DPI-C" context function void _pyhdl_if_Py_DecRef(input PyObject p0);

    function void Py_DecRef(input PyObject p0);
        _pyhdl_if_Py_DecRef(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_Py_EnterRecursiveCall(input string where);

    function int Py_EnterRecursiveCall(input string where);
        return _pyhdl_if_Py_EnterRecursiveCall(where);
    endfunction

    import "DPI-C" context function void _pyhdl_if_Py_Finalize();

    function void Py_Finalize();
        _pyhdl_if_Py_Finalize();
    endfunction

    import "DPI-C" context function int _pyhdl_if_Py_FinalizeEx();

    function int Py_FinalizeEx();
        return _pyhdl_if_Py_FinalizeEx();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GETENV(input string name);

    function string Py_GETENV(input string name);
        return _pyhdl_if_Py_GETENV(name);
    endfunction

    import "DPI-C" context function PyObject _pyhdl_if_Py_GenericAlias(input PyObject p0, input PyObject p1);

    function PyObject Py_GenericAlias(input PyObject p0, input PyObject p1);
        return _pyhdl_if_Py_GenericAlias(p0, p1);
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetBuildInfo();

    function string Py_GetBuildInfo();
        return _pyhdl_if_Py_GetBuildInfo();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetCompiler();

    function string Py_GetCompiler();
        return _pyhdl_if_Py_GetCompiler();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetCopyright();

    function string Py_GetCopyright();
        return _pyhdl_if_Py_GetCopyright();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetExecPrefix();

    function string Py_GetExecPrefix();
        return _pyhdl_if_Py_GetExecPrefix();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetPath();

    function string Py_GetPath();
        return _pyhdl_if_Py_GetPath();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetPlatform();

    function string Py_GetPlatform();
        return _pyhdl_if_Py_GetPlatform();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetPrefix();

    function string Py_GetPrefix();
        return _pyhdl_if_Py_GetPrefix();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetProgramFullPath();

    function string Py_GetProgramFullPath();
        return _pyhdl_if_Py_GetProgramFullPath();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetProgramName();

    function string Py_GetProgramName();
        return _pyhdl_if_Py_GetProgramName();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetPythonHome();

    function string Py_GetPythonHome();
        return _pyhdl_if_Py_GetPythonHome();
    endfunction

    import "DPI-C" context function int _pyhdl_if_Py_GetRecursionLimit();

    function int Py_GetRecursionLimit();
        return _pyhdl_if_Py_GetRecursionLimit();
    endfunction

    import "DPI-C" context function string _pyhdl_if_Py_GetVersion();

    function string Py_GetVersion();
        return _pyhdl_if_Py_GetVersion();
    endfunction

    import "DPI-C" context function void _pyhdl_if_Py_IncRef(input PyObject p0);

    function void Py_IncRef(input PyObject p0);
        _pyhdl_if_Py_IncRef(p0);
    endfunction

    import "DPI-C" context function void _pyhdl_if_Py_Initialize();

    function void Py_Initialize();
        _pyhdl_if_Py_Initialize();
    endfunction

    import "DPI-C" context function void _pyhdl_if_Py_InitializeEx(input int p0);

    function void Py_InitializeEx(input int p0);
        _pyhdl_if_Py_InitializeEx(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_Py_IsInitialized();

    function int Py_IsInitialized();
        return _pyhdl_if_Py_IsInitialized();
    endfunction

    import "DPI-C" context function void _pyhdl_if_Py_LeaveRecursiveCall();

    function void Py_LeaveRecursiveCall();
        _pyhdl_if_Py_LeaveRecursiveCall();
    endfunction

    import "DPI-C" context function int _pyhdl_if_Py_MakePendingCalls();

    function int Py_MakePendingCalls();
        return _pyhdl_if_Py_MakePendingCalls();
    endfunction

    import "DPI-C" context function int _pyhdl_if_Py_ReprEnter(input PyObject p0);

    function int Py_ReprEnter(input PyObject p0);
        return _pyhdl_if_Py_ReprEnter(p0);
    endfunction

    import "DPI-C" context function void _pyhdl_if_Py_ReprLeave(input PyObject p0);

    function void Py_ReprLeave(input PyObject p0);
        _pyhdl_if_Py_ReprLeave(p0);
    endfunction

    import "DPI-C" context function int _pyhdl_if_Py_RunMain();

    function int Py_RunMain();
        return _pyhdl_if_Py_RunMain();
    endfunction

    import "DPI-C" context function void _pyhdl_if_Py_SetRecursionLimit(input int p0);

    function void Py_SetRecursionLimit(input int p0);
        _pyhdl_if_Py_SetRecursionLimit(p0);
    endfunction
