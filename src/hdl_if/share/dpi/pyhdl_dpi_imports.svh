
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

    import "DPI-C" context function int PyErr_BadArgument();

    import "DPI-C" context function int PyErr_CheckSignals();

    import "DPI-C" context function void PyErr_Clear();

    import "DPI-C" context function void PyErr_Display(input PyObject p0, input PyObject p1, input PyObject p2);

    import "DPI-C" context function void PyErr_DisplayException(input PyObject p0);

    import "DPI-C" context function int PyErr_ExceptionMatches(input PyObject p0);

    import "DPI-C" context function PyObject PyErr_GetHandledException();

    import "DPI-C" context function PyObject PyErr_GetRaisedException();

    import "DPI-C" context function int PyErr_GivenExceptionMatches(input PyObject p0, input PyObject p1);

    import "DPI-C" context function PyObject PyErr_NewException(input string name, input PyObject base, input PyObject dict);

    import "DPI-C" context function PyObject PyErr_NewExceptionWithDoc(input string name, input string doc, input PyObject base, input PyObject dict);

    import "DPI-C" context function PyObject PyErr_NoMemory();

    import "DPI-C" context function PyObject PyErr_Occurred();

    import "DPI-C" context function void PyErr_Print();

    import "DPI-C" context function void PyErr_PrintEx(input int p0);

    import "DPI-C" context function PyObject PyErr_ProgramText(input string filename, input int lineno);

    import "DPI-C" context function PyObject PyErr_ProgramTextObject(input PyObject filename, input int lineno);

    import "DPI-C" context function void PyErr_RangedSyntaxLocationObject(input PyObject filename, input int lineno, input int col_offset, input int end_lineno, input int end_col_offset);

    import "DPI-C" context function void PyErr_Restore(input PyObject p0, input PyObject p1, input PyObject p2);

    import "DPI-C" context function void PyErr_SetExcInfo(input PyObject p0, input PyObject p1, input PyObject p2);

    import "DPI-C" context function PyObject PyErr_SetFromErrno(input PyObject p0);

    import "DPI-C" context function PyObject PyErr_SetFromErrnoWithFilename(input PyObject exc, input string filename);

    import "DPI-C" context function PyObject PyErr_SetFromErrnoWithFilenameObject(input PyObject p0, input PyObject p1);

    import "DPI-C" context function PyObject PyErr_SetFromErrnoWithFilenameObjects(input PyObject p0, input PyObject p1, input PyObject p2);

    import "DPI-C" context function void PyErr_SetHandledException(input PyObject p0);

    import "DPI-C" context function PyObject PyErr_SetImportError(input PyObject p0, input PyObject p1, input PyObject p2);

    import "DPI-C" context function PyObject PyErr_SetImportErrorSubclass(input PyObject p0, input PyObject p1, input PyObject p2, input PyObject p3);

    import "DPI-C" context function void PyErr_SetInterrupt();

    import "DPI-C" context function int PyErr_SetInterruptEx(input int signum);

    import "DPI-C" context function void PyErr_SetNone(input PyObject p0);

    import "DPI-C" context function void PyErr_SetObject(input PyObject p0, input PyObject p1);

    import "DPI-C" context function void PyErr_SetRaisedException(input PyObject p0);

    import "DPI-C" context function void PyErr_SetString(input PyObject exception, input string _string);

    import "DPI-C" context function void PyErr_SyntaxLocation(input string filename, input int lineno);

    import "DPI-C" context function void PyErr_SyntaxLocationEx(input string filename, input int lineno, input int col_offset);

    import "DPI-C" context function void PyErr_SyntaxLocationObject(input PyObject filename, input int lineno, input int col_offset);

    import "DPI-C" context function int PyErr_WarnEx(input PyObject category, input string message, input int unsigned stack_level);

    import "DPI-C" context function int PyErr_WarnExplicit(input PyObject category, input string message, input string filename, input int lineno, input string _module, input PyObject registry);

    import "DPI-C" context function int PyErr_WarnExplicitObject(input PyObject category, input PyObject message, input PyObject filename, input int lineno, input PyObject _module, input PyObject registry);

    import "DPI-C" context function void PyErr_WriteUnraisable(input PyObject p0);

    import "DPI-C" context function PyObject PyEval_EvalCode(input PyObject p0, input PyObject p1, input PyObject p2);

    import "DPI-C" context function PyObject PyEval_GetBuiltins();

    import "DPI-C" context function string PyEval_GetFuncDesc(input PyObject p0);

    import "DPI-C" context function string PyEval_GetFuncName(input PyObject p0);

    import "DPI-C" context function PyObject PyEval_GetGlobals();

    import "DPI-C" context function PyObject PyEval_GetLocals();

    import "DPI-C" context function int PyGILState_Check();

    import "DPI-C" context function PyGILState_STATE PyGILState_Ensure();

    import "DPI-C" context function void PyGILState_Release(input PyGILState_STATE p0);

    import "DPI-C" context function PyObject PyImport_AddModule(input string name);

    import "DPI-C" context function PyObject PyImport_AddModuleObject(input PyObject name);

    import "DPI-C" context function PyObject PyImport_ExecCodeModule(input string name, input PyObject co);

    import "DPI-C" context function PyObject PyImport_ExecCodeModuleEx(input string name, input PyObject co, input string pathname);

    import "DPI-C" context function PyObject PyImport_ExecCodeModuleObject(input PyObject name, input PyObject co, input PyObject pathname, input PyObject cpathname);

    import "DPI-C" context function PyObject PyImport_ExecCodeModuleWithPathnames(input string name, input PyObject co, input string pathname, input string cpathname);

    import "DPI-C" context function PyObject PyImport_GetImporter(input PyObject path);

    import "DPI-C" context function int PyImport_GetMagicNumber();

    import "DPI-C" context function string PyImport_GetMagicTag();

    import "DPI-C" context function PyObject PyImport_GetModule(input PyObject name);

    import "DPI-C" context function PyObject PyImport_GetModuleDict();

    import "DPI-C" context function PyObject PyImport_Import(input PyObject name);

    import "DPI-C" context function int PyImport_ImportFrozenModule(input string name);

    import "DPI-C" context function int PyImport_ImportFrozenModuleObject(input PyObject name);

    import "DPI-C" context function PyObject PyImport_ImportModule(input string name);

    import "DPI-C" context function PyObject PyImport_ImportModuleLevel(input string name, input PyObject globals, input PyObject locals, input PyObject fromlist, input int level);

    import "DPI-C" context function PyObject PyImport_ImportModuleLevelObject(input PyObject name, input PyObject globals, input PyObject locals, input PyObject fromlist, input int level);

    import "DPI-C" context function PyObject PyImport_ImportModuleNoBlock(input string name);

    import "DPI-C" context function PyObject PyImport_ReloadModule(input PyObject m);

    import "DPI-C" context function real PyLong_AsDouble(input PyObject p0);

    import "DPI-C" context function int PyLong_AsLong(input PyObject p0);

    import "DPI-C" context function int PyLong_AsLongAndOverflow(input PyObject p0, output int p1);

    import "DPI-C" context function longint PyLong_AsLongLong(input PyObject p0);

    import "DPI-C" context function longint PyLong_AsLongLongAndOverflow(input PyObject p0, output int p1);

    import "DPI-C" context function int unsigned PyLong_AsSize_t(input PyObject p0);

    import "DPI-C" context function int unsigned PyLong_AsSsize_t(input PyObject p0);

    import "DPI-C" context function int unsigned PyLong_AsUnsignedLong(input PyObject p0);

    import "DPI-C" context function longint unsigned PyLong_AsUnsignedLongLong(input PyObject p0);

    import "DPI-C" context function longint unsigned PyLong_AsUnsignedLongLongMask(input PyObject p0);

    import "DPI-C" context function int unsigned PyLong_AsUnsignedLongMask(input PyObject p0);

    import "DPI-C" context function chandle PyLong_AsVoidPtr(input PyObject p0);

    import "DPI-C" context function PyObject PyLong_FromDouble(input real p0);

    import "DPI-C" context function PyObject PyLong_FromLong(input int p0);

    import "DPI-C" context function PyObject PyLong_FromLongLong(input longint p0);

    import "DPI-C" context function PyObject PyLong_FromSize_t(input int unsigned p0);

    import "DPI-C" context function PyObject PyLong_FromSsize_t(input int unsigned p0);

    import "DPI-C" context function PyObject PyLong_FromString(input string p0, output chandle p1, input int p2);

    import "DPI-C" context function PyObject PyLong_FromUnicodeObject(input PyObject u, input int base);

    import "DPI-C" context function PyObject PyLong_FromUnsignedLong(input int unsigned p0);

    import "DPI-C" context function PyObject PyLong_FromUnsignedLongLong(input longint unsigned p0);

    import "DPI-C" context function PyObject PyLong_FromVoidPtr(input chandle p0);

    import "DPI-C" context function PyObject PyLong_GetInfo();

    import "DPI-C" context function PyObject PyObject_ASCII(input PyObject p0);

    import "DPI-C" context function int PyObject_AsFileDescriptor(input PyObject p0);

    import "DPI-C" context function PyObject PyObject_Bytes(input PyObject p0);

    import "DPI-C" context function PyObject PyObject_Call(input PyObject callable, input PyObject args, input PyObject kwargs);

    import "DPI-C" context function void PyObject_CallFinalizer(input PyObject p0);

    import "DPI-C" context function int PyObject_CallFinalizerFromDealloc(input PyObject p0);

    import "DPI-C" context function PyObject PyObject_CallNoArgs(input PyObject func);

    import "DPI-C" context function PyObject PyObject_CallObject(input PyObject callable, input PyObject args);

    import "DPI-C" context function PyObject PyObject_CallOneArg(input PyObject func, input PyObject arg);

    import "DPI-C" context function chandle PyObject_Calloc(input int unsigned nelem, input int unsigned elsize);

    import "DPI-C" context function int PyObject_CheckBuffer(input PyObject obj);

    import "DPI-C" context function void PyObject_ClearWeakRefs(input PyObject p0);

    import "DPI-C" context function int PyObject_CopyData(input PyObject dest, input PyObject src);

    import "DPI-C" context function int PyObject_DelItem(input PyObject o, input PyObject key);

    import "DPI-C" context function int PyObject_DelItemString(input PyObject o, input string key);

    import "DPI-C" context function PyObject PyObject_Dir(input PyObject p0);

    import "DPI-C" context function PyObject PyObject_Format(input PyObject obj, input PyObject format_spec);

    import "DPI-C" context function void PyObject_Free(input chandle ptr);

    import "DPI-C" context function void PyObject_GC_Del(input chandle p0);

    import "DPI-C" context function int PyObject_GC_IsFinalized(input PyObject p0);

    import "DPI-C" context function int PyObject_GC_IsTracked(input PyObject p0);

    import "DPI-C" context function void PyObject_GC_Track(input chandle p0);

    import "DPI-C" context function void PyObject_GC_UnTrack(input chandle p0);

    import "DPI-C" context function PyObject PyObject_GenericGetAttr(input PyObject p0, input PyObject p1);

    import "DPI-C" context function PyObject PyObject_GenericGetDict(input PyObject p0, input chandle p1);

    import "DPI-C" context function int PyObject_GenericSetAttr(input PyObject p0, input PyObject p1, input PyObject p2);

    import "DPI-C" context function int PyObject_GenericSetDict(input PyObject p0, input PyObject p1, input chandle p2);

    import "DPI-C" context function PyObject PyObject_GetAIter(input PyObject p0);

    import "DPI-C" context function PyObject PyObject_GetAttr(input PyObject p0, input PyObject p1);

    import "DPI-C" context function PyObject PyObject_GetAttrString(input PyObject p0, input string p1);

    import "DPI-C" context function PyObject PyObject_GetItem(input PyObject o, input PyObject key);

    import "DPI-C" context function chandle PyObject_GetItemData(input PyObject obj);

    import "DPI-C" context function PyObject PyObject_GetIter(input PyObject p0);

    import "DPI-C" context function int PyObject_HasAttr(input PyObject p0, input PyObject p1);

    import "DPI-C" context function int PyObject_HasAttrString(input PyObject p0, input string p1);

    import "DPI-C" context function int PyObject_IS_GC(input PyObject obj);

    import "DPI-C" context function PyObject PyObject_Init(input PyObject p0, input PyTypeObject p1);

    import "DPI-C" context function int PyObject_IsInstance(input PyObject object, input PyObject typeorclass);

    import "DPI-C" context function int PyObject_IsSubclass(input PyObject object, input PyObject typeorclass);

    import "DPI-C" context function int PyObject_IsTrue(input PyObject p0);

    import "DPI-C" context function int unsigned PyObject_LengthHint(input PyObject o, input int unsigned p1);

    import "DPI-C" context function chandle PyObject_Malloc(input int unsigned size);

    import "DPI-C" context function int PyObject_Not(input PyObject p0);

    import "DPI-C" context function chandle PyObject_Realloc(input chandle ptr, input int unsigned new_size);

    import "DPI-C" context function PyObject PyObject_Repr(input PyObject p0);

    import "DPI-C" context function PyObject PyObject_RichCompare(input PyObject p0, input PyObject p1, input int p2);

    import "DPI-C" context function int PyObject_RichCompareBool(input PyObject p0, input PyObject p1, input int p2);

    import "DPI-C" context function PyObject PyObject_SelfIter(input PyObject p0);

    import "DPI-C" context function int PyObject_SetAttr(input PyObject p0, input PyObject p1, input PyObject p2);

    import "DPI-C" context function int PyObject_SetAttrString(input PyObject p0, input string p1, input PyObject p2);

    import "DPI-C" context function int PyObject_SetItem(input PyObject o, input PyObject key, input PyObject v);

    import "DPI-C" context function int unsigned PyObject_Size(input PyObject o);

    import "DPI-C" context function PyObject PyObject_Str(input PyObject p0);

    import "DPI-C" context function PyObject PyObject_Type(input PyObject o);

    import "DPI-C" context function PyObject PyTuple_GetItem(input PyObject p0, input int unsigned p1);

    import "DPI-C" context function PyObject PyTuple_GetSlice(input PyObject p0, input int unsigned p1, input int unsigned p2);

    import "DPI-C" context function PyObject PyTuple_New(input int unsigned size);

    import "DPI-C" context function int PyTuple_SetItem(input PyObject p0, input int unsigned p1, input PyObject p2);

    import "DPI-C" context function int unsigned PyTuple_Size(input PyObject p0);

    import "DPI-C" context function PyObject PyUnicode_AsASCIIString(input PyObject unicode);

    import "DPI-C" context function PyObject PyUnicode_AsCharmapString(input PyObject unicode, input PyObject mapping);

    import "DPI-C" context function PyObject PyUnicode_AsDecodedObject(input PyObject unicode, input string encoding, input string errors);

    import "DPI-C" context function PyObject PyUnicode_AsDecodedUnicode(input PyObject unicode, input string encoding, input string errors);

    import "DPI-C" context function PyObject PyUnicode_AsEncodedObject(input PyObject unicode, input string encoding, input string errors);

    import "DPI-C" context function PyObject PyUnicode_AsEncodedString(input PyObject unicode, input string encoding, input string errors);

    import "DPI-C" context function PyObject PyUnicode_AsEncodedUnicode(input PyObject unicode, input string encoding, input string errors);

    import "DPI-C" context function PyObject PyUnicode_AsLatin1String(input PyObject unicode);

    import "DPI-C" context function PyObject PyUnicode_AsRawUnicodeEscapeString(input PyObject unicode);

    import "DPI-C" context function PyObject PyUnicode_AsUTF16String(input PyObject unicode);

    import "DPI-C" context function PyObject PyUnicode_AsUTF32String(input PyObject unicode);

    import "DPI-C" context function string PyUnicode_AsUTF8(input PyObject unicode);

    import "DPI-C" context function string PyUnicode_AsUTF8AndSize(input PyObject unicode, output int unsigned size);

    import "DPI-C" context function PyObject PyUnicode_AsUTF8String(input PyObject unicode);

    import "DPI-C" context function PyObject PyUnicode_AsUnicodeEscapeString(input PyObject unicode);

    import "DPI-C" context function int unsigned PyUnicode_AsWideChar(input PyObject unicode, input string w, input int unsigned size);

    import "DPI-C" context function string PyUnicode_AsWideCharString(input PyObject unicode, output int unsigned size);

    import "DPI-C" context function PyObject PyUnicode_BuildEncodingMap(input PyObject _string);

    import "DPI-C" context function int PyUnicode_Compare(input PyObject left, input PyObject right);

    import "DPI-C" context function int PyUnicode_CompareWithASCIIString(input PyObject left, input string right);

    import "DPI-C" context function PyObject PyUnicode_Concat(input PyObject left, input PyObject right);

    import "DPI-C" context function int PyUnicode_Contains(input PyObject container, input PyObject element);

    import "DPI-C" context function int unsigned PyUnicode_CopyCharacters(input PyObject to, input int unsigned to_start, input PyObject from, input int unsigned from_start, input int unsigned how_many);

    import "DPI-C" context function int unsigned PyUnicode_Count(input PyObject str, input PyObject substr, input int unsigned start, input int unsigned _end);

    import "DPI-C" context function PyObject PyUnicode_Decode(input string s, input int unsigned size, input string encoding, input string errors);

    import "DPI-C" context function PyObject PyUnicode_DecodeASCII(input string _string, input int unsigned length, input string errors);

    import "DPI-C" context function PyObject PyUnicode_DecodeCharmap(input string _string, input int unsigned length, input PyObject mapping, input string errors);

    import "DPI-C" context function PyObject PyUnicode_DecodeFSDefault(input string s);

    import "DPI-C" context function PyObject PyUnicode_DecodeFSDefaultAndSize(input string s, input int unsigned size);

    import "DPI-C" context function PyObject PyUnicode_DecodeLatin1(input string _string, input int unsigned length, input string errors);

    import "DPI-C" context function PyObject PyUnicode_DecodeLocale(input string str, input string errors);

    import "DPI-C" context function PyObject PyUnicode_DecodeLocaleAndSize(input string str, input int unsigned len, input string errors);

    import "DPI-C" context function PyObject PyUnicode_DecodeRawUnicodeEscape(input string _string, input int unsigned length, input string errors);

    import "DPI-C" context function PyObject PyUnicode_DecodeUTF16(input string _string, input int unsigned length, input string errors, output int byteorder);

    import "DPI-C" context function PyObject PyUnicode_DecodeUTF16Stateful(input string _string, input int unsigned length, input string errors, output int byteorder, output int unsigned consumed);

    import "DPI-C" context function PyObject PyUnicode_DecodeUTF32(input string _string, input int unsigned length, input string errors, output int byteorder);

    import "DPI-C" context function PyObject PyUnicode_DecodeUTF32Stateful(input string _string, input int unsigned length, input string errors, output int byteorder, output int unsigned consumed);

    import "DPI-C" context function PyObject PyUnicode_DecodeUTF7(input string _string, input int unsigned length, input string errors);

    import "DPI-C" context function PyObject PyUnicode_DecodeUTF7Stateful(input string _string, input int unsigned length, input string errors, output int unsigned consumed);

    import "DPI-C" context function PyObject PyUnicode_DecodeUTF8(input string _string, input int unsigned length, input string errors);

    import "DPI-C" context function PyObject PyUnicode_DecodeUTF8Stateful(input string _string, input int unsigned length, input string errors, output int unsigned consumed);

    import "DPI-C" context function PyObject PyUnicode_DecodeUnicodeEscape(input string _string, input int unsigned length, input string errors);

    import "DPI-C" context function PyObject PyUnicode_EncodeFSDefault(input PyObject unicode);

    import "DPI-C" context function PyObject PyUnicode_EncodeLocale(input PyObject unicode, input string errors);

    import "DPI-C" context function int PyUnicode_FSConverter(input PyObject p0, input chandle p1);

    import "DPI-C" context function int PyUnicode_FSDecoder(input PyObject p0, input chandle p1);

    import "DPI-C" context function int unsigned PyUnicode_Find(input PyObject str, input PyObject substr, input int unsigned start, input int unsigned _end, input int direction);

    import "DPI-C" context function PyObject PyUnicode_Format(input PyObject format, input PyObject args);

    import "DPI-C" context function PyObject PyUnicode_FromEncodedObject(input PyObject obj, input string encoding, input string errors);

    import "DPI-C" context function PyObject PyUnicode_FromObject(input PyObject obj);

    import "DPI-C" context function PyObject PyUnicode_FromOrdinal(input int ordinal);

    import "DPI-C" context function PyObject PyUnicode_FromString(input string u);

    import "DPI-C" context function PyObject PyUnicode_FromStringAndSize(input string u, input int unsigned size);

    import "DPI-C" context function string PyUnicode_GetDefaultEncoding();

    import "DPI-C" context function int unsigned PyUnicode_GetLength(input PyObject unicode);

    import "DPI-C" context function PyObject PyUnicode_InternFromString(input string u);

    import "DPI-C" context function int PyUnicode_IsIdentifier(input PyObject s);

    import "DPI-C" context function PyObject PyUnicode_Join(input PyObject separator, input PyObject seq);

    import "DPI-C" context function PyObject PyUnicode_Partition(input PyObject s, input PyObject sep);

    import "DPI-C" context function PyObject PyUnicode_RPartition(input PyObject s, input PyObject sep);

    import "DPI-C" context function PyObject PyUnicode_RSplit(input PyObject s, input PyObject sep, input int unsigned maxsplit);

    import "DPI-C" context function PyObject PyUnicode_Replace(input PyObject str, input PyObject substr, input PyObject replstr, input int unsigned maxcount);

    import "DPI-C" context function PyObject PyUnicode_RichCompare(input PyObject left, input PyObject right, input int op);

    import "DPI-C" context function PyObject PyUnicode_Split(input PyObject s, input PyObject sep, input int unsigned maxsplit);

    import "DPI-C" context function PyObject PyUnicode_Splitlines(input PyObject s, input int keepends);

    import "DPI-C" context function PyObject PyUnicode_Substring(input PyObject str, input int unsigned start, input int unsigned _end);

    import "DPI-C" context function int unsigned PyUnicode_Tailmatch(input PyObject str, input PyObject substr, input int unsigned start, input int unsigned _end, input int direction);

    import "DPI-C" context function PyObject PyUnicode_Translate(input PyObject str, input PyObject _table, input string errors);

    import "DPI-C" context function void Py_DecRef(input PyObject p0);

    import "DPI-C" context function int Py_EnterRecursiveCall(input string where);

    import "DPI-C" context function void Py_Finalize();

    import "DPI-C" context function int Py_FinalizeEx();

    import "DPI-C" context function string Py_GETENV(input string name);

    import "DPI-C" context function PyObject Py_GenericAlias(input PyObject p0, input PyObject p1);

    import "DPI-C" context function string Py_GetBuildInfo();

    import "DPI-C" context function string Py_GetCompiler();

    import "DPI-C" context function string Py_GetCopyright();

    import "DPI-C" context function string Py_GetExecPrefix();

    import "DPI-C" context function string Py_GetPath();

    import "DPI-C" context function string Py_GetPlatform();

    import "DPI-C" context function string Py_GetPrefix();

    import "DPI-C" context function string Py_GetProgramFullPath();

    import "DPI-C" context function string Py_GetProgramName();

    import "DPI-C" context function string Py_GetPythonHome();

    import "DPI-C" context function int Py_GetRecursionLimit();

    import "DPI-C" context function string Py_GetVersion();

    import "DPI-C" context function void Py_IncRef(input PyObject p0);

    import "DPI-C" context function void Py_Initialize();

    import "DPI-C" context function void Py_InitializeEx(input int p0);

    import "DPI-C" context function int Py_IsInitialized();

    import "DPI-C" context function void Py_LeaveRecursiveCall();

    import "DPI-C" context function int Py_MakePendingCalls();

    import "DPI-C" context function int Py_ReprEnter(input PyObject p0);

    import "DPI-C" context function void Py_ReprLeave(input PyObject p0);

    import "DPI-C" context function int Py_RunMain();

    import "DPI-C" context function void Py_SetRecursionLimit(input int p0);
