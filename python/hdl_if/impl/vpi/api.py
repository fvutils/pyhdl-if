#****************************************************************************
#* api.py
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

unimplemented_vpi_funcs = []

vpiAlways = 1
vpiAssignStmt = 2
vpiAssignment = 3
vpiBegin = 4
vpiCase = 5
vpiCaseItem = 6
vpiConstant = 7
vpiContAssign = 8
vpiDeassign = 9
vpiDefParam = 10
vpiDelayControl = 11
vpiDisable = 12
vpiEventControl = 13
vpiEventStmt = 14
vpiFor = 15
vpiForce = 16
vpiForever = 17
vpiFork = 18
vpiFuncCall = 19
vpiFunction = 20
vpiGate = 21
vpiIf = 22
vpiIfElse = 23
vpiInitial = 24
vpiIntegerVar = 25
vpiInterModPath = 26
vpiIterator = 27
vpiIODecl = 28
vpiMemory = 29
vpiMemoryWord = 30
vpiModPath = 31
vpiModule = 32
vpiNamedBegin = 33
vpiNamedEvent = 34
vpiNamedFork = 35
vpiNet = 36
vpiNetBit = 37
vpiNullStmt = 38
vpiOperation = 39
vpiParamAssign = 40
vpiParameter = 41
vpiPartSelect = 42
vpiPathTerm = 43
vpiPort = 44
vpiPortBit = 45
vpiPrimTerm = 46
vpiRealVar = 47
vpiReg = 48
vpiRegBit = 49
vpiRelease = 50
vpiRepeat = 51
vpiRepeatControl = 52
vpiSchedEvent = 53
vpiSpecParam = 54
vpiSwitch = 55
vpiSysFuncCall = 56
vpiSysTaskCall = 57
vpiTableEntry = 58
vpiTask = 59
vpiTaskCall = 60
vpiTchk = 61
vpiTchkTerm = 62
vpiTimeVar = 63
vpiTimeQueue = 64
vpiUdp = 65
vpiUdpDefn = 66
vpiUserSystf = 67
vpiVarSelect = 68
vpiWait = 69
vpiWhile = 70
vpiAttribute = 105
vpiBitSelect = 106
vpiCallback = 107
vpiDelayTerm = 108
vpiDelayDevice = 109
vpiFrame = 110
vpiGateArray = 111
vpiModuleArray = 112
vpiPrimitiveArray = 113
vpiNetArray = 114
vpiRange = 115
vpiRegArray = 116
vpiSwitchArray = 117
vpiUdpArray = 118
vpiContAssignBit = 128
vpiNamedEventArray = 129
vpiIndexedPartSelect = 130
vpiGenScopeArray = 133
vpiGenScope = 134
vpiGenVar = 135
vpiCondition = 71
vpiDelay = 72
vpiElseStmt = 73
vpiForIncStmt = 74
vpiForInitStmt = 75
vpiHighConn = 76
vpiLhs = 77
vpiIndex = 78
vpiLeftRange = 79
vpiLowConn = 80
vpiParent = 81
vpiRhs = 82
vpiRightRange = 83
vpiScope = 84
vpiSysTfCall = 85
vpiTchkDataTerm = 86
vpiTchkNotifier = 87
vpiTchkRefTerm = 88
vpiArgument = 89
vpiBit = 90
vpiDriver = 91
vpiInternalScope = 92
vpiLoad = 93
vpiModDataPathIn = 94
vpiModPathIn = 95
vpiModPathOut = 96
vpiOperand = 97
vpiPortInst = 98
vpiProcess = 99
vpiVariables = 100
vpiUse = 101
vpiExpr = 102
vpiPrimitive = 103
vpiStmt = 104
vpiActiveTimeFormat = 119
vpiInTerm = 120
vpiInstanceArray = 121
vpiLocalDriver = 122
vpiLocalLoad = 123
vpiOutTerm = 124
vpiPorts = 125
vpiSimNet = 126
vpiTaskFunc = 127
vpiBaseExpr = 131
vpiWidthExpr = 132
vpiAutomatics = 136
vpiUndefined = -1
vpiType = 1
vpiName = 2
vpiFullName = 3
vpiSize = 4
vpiFile = 5
vpiLineNo = 6
vpiTopModule = 7
vpiCellInstance = 8
vpiDefName = 9
vpiProtected = 10
vpiTimeUnit = 11
vpiTimePrecision = 12
vpiDefNetType = 13
vpiUnconnDrive = 14
vpiHighZ = 1
vpiPull1 = 2
vpiPull0 = 3
vpiDefFile = 15
vpiDefLineNo = 16
vpiDefDelayMode = 47
vpiDelayModeNone = 1
vpiDelayModePath = 2
vpiDelayModeDistrib = 3
vpiDelayModeUnit = 4
vpiDelayModeZero = 5
vpiDelayModeMTM = 6
vpiDefDecayTime = 48
vpiScalar = 17
vpiVector = 18
vpiExplicitName = 19
vpiDirection = 20
vpiInput = 1
vpiOutput = 2
vpiInout = 3
vpiMixedIO = 4
vpiNoDirection = 5
vpiConnByName = 21
vpiNetType = 22
vpiWire = 1
vpiWand = 2
vpiWor = 3
vpiTri = 4
vpiTri0 = 5
vpiTri1 = 6
vpiTriReg = 7
vpiTriAnd = 8
vpiTriOr = 9
vpiSupply1 = 10
vpiSupply0 = 11
vpiNone = 12
vpiUwire = 13
vpiExplicitScalared = 23
vpiExplicitVectored = 24
vpiExpanded = 25
vpiImplicitDecl = 26
vpiChargeStrength = 27
vpiArray = 28
vpiPortIndex = 29
vpiTermIndex = 30
vpiStrength0 = 31
vpiStrength1 = 32
vpiPrimType = 33
vpiAndPrim = 1
vpiNandPrim = 2
vpiNorPrim = 3
vpiOrPrim = 4
vpiXorPrim = 5
vpiXnorPrim = 6
vpiBufPrim = 7
vpiNotPrim = 8
vpiBufif0Prim = 9
vpiBufif1Prim = 10
vpiNotif0Prim = 11
vpiNotif1Prim = 12
vpiNmosPrim = 13
vpiPmosPrim = 14
vpiCmosPrim = 15
vpiRnmosPrim = 16
vpiRpmosPrim = 17
vpiRcmosPrim = 18
vpiRtranPrim = 19
vpiRtranif0Prim = 20
vpiRtranif1Prim = 21
vpiTranPrim = 22
vpiTranif0Prim = 23
vpiTranif1Prim = 24
vpiPullupPrim = 25
vpiPulldownPrim = 26
vpiSeqPrim = 27
vpiCombPrim = 28
vpiPolarity = 34
vpiDataPolarity = 35
vpiPositive = 1
vpiNegative = 2
vpiUnknown = 3
vpiEdge = 36
vpiNoEdge = 0x00
vpiEdge01 = 0x01
vpiEdge10 = 0x02
vpiEdge0x = 0x04
vpiEdgex1 = 0x08
vpiEdge1x = 0x10
vpiEdgex0 = 0x20
vpiPosedge = (vpiEdgex1 | vpiEdge01 | vpiEdge0x)
vpiNegedge = (vpiEdgex0 | vpiEdge10 | vpiEdge1x)
vpiAnyEdge = (vpiPosedge | vpiNegedge)
vpiPathType = 37
vpiPathFull = 1
vpiPathParallel = 2
vpiTchkType = 38
vpiSetup = 1
vpiHold = 2
vpiPeriod = 3
vpiWidth = 4
vpiSkew = 5
vpiRecovery = 6
vpiNoChange = 7
vpiSetupHold = 8
vpiFullskew = 9
vpiRecrem = 10
vpiRemoval = 11
vpiTimeskew = 12
vpiOpType = 39
vpiMinusOp = 1
vpiPlusOp = 2
vpiNotOp = 3
vpiBitNegOp = 4
vpiUnaryAndOp = 5
vpiUnaryNandOp = 6
vpiUnaryOrOp = 7
vpiUnaryNorOp = 8
vpiUnaryXorOp = 9
vpiUnaryXNorOp = 10
vpiSubOp = 11
vpiDivOp = 12
vpiModOp = 13
vpiEqOp = 14
vpiNeqOp = 15
vpiCaseEqOp = 16
vpiCaseNeqOp = 17
vpiGtOp = 18
vpiGeOp = 19
vpiLtOp = 20
vpiLeOp = 21
vpiLShiftOp = 22
vpiRShiftOp = 23
vpiAddOp = 24
vpiMultOp = 25
vpiLogAndOp = 26
vpiLogOrOp = 27
vpiBitAndOp = 28
vpiBitOrOp = 29
vpiBitXorOp = 30
vpiBitXNorOp = 31
vpiBitXnorOp = vpiBitXNorOp
vpiConditionOp = 32
vpiConcatOp = 33
vpiMultiConcatOp = 34
vpiEventOrOp = 35
vpiNullOp = 36
vpiListOp = 37
vpiMinTypMaxOp = 38
vpiPosedgeOp = 39
vpiNegedgeOp = 40
vpiArithLShiftOp = 41
vpiArithRShiftOp = 42
vpiPowerOp = 43
vpiConstType = 40
vpiDecConst = 1
vpiRealConst = 2
vpiBinaryConst = 3
vpiOctConst = 4
vpiHexConst = 5
vpiStringConst = 6
vpiIntConst = 7
vpiTimeConst = 8
vpiBlocking = 41
vpiCaseType = 42
vpiCaseExact = 1
vpiCaseX = 2
vpiCaseZ = 3
vpiNetDeclAssign = 43
vpiFuncType = 44
vpiIntFunc = 1
vpiRealFunc = 2
vpiTimeFunc = 3
vpiSizedFunc = 4
vpiSizedSignedFunc = 5
vpiSysFuncType = vpiFuncType
vpiSysFuncInt = vpiIntFunc
vpiSysFuncReal = vpiRealFunc
vpiSysFuncTime = vpiTimeFunc
vpiSysFuncSized = vpiSizedFunc
vpiUserDefn = 45
vpiScheduled = 46
vpiActive = 49
vpiAutomatic = 50
vpiCell = 51
vpiConfig = 52
vpiConstantSelect = 53
vpiDecompile = 54
vpiDefAttribute = 55
vpiDelayType = 56
vpiModPathDelay = 1
vpiInterModPathDelay = 2
vpiMIPDelay = 3
vpiIteratorType = 57
vpiLibrary = 58
vpiOffset = 60
vpiResolvedNetType = 61
vpiSaveRestartID = 62
vpiSaveRestartLocation = 63
vpiValid = 64
vpiValidFalse = 0
vpiValidTrue = 1
vpiSigned = 65
vpiLocalParam = 70
vpiModPathHasIfNone = 71
vpiIndexedPartSelectType = 72
vpiPosIndexed = 1
vpiNegIndexed = 2
vpiIsMemory = 73
vpiIsProtected = 74
vpiStop = 66
vpiFinish = 67
vpiReset = 68
vpiSetInteractiveScope = 69
vpiScaledRealTime = 1
vpiSimTime = 2
vpiSuppressTime = 3
vpiSupplyDrive = 0x80
vpiStrongDrive = 0x40
vpiPullDrive = 0x20
vpiWeakDrive = 0x08
vpiLargeCharge = 0x10
vpiMediumCharge = 0x04
vpiSmallCharge = 0x02
vpiHiZ = 0x01
vpiBinStrVal = 1
vpiOctStrVal = 2
vpiDecStrVal = 3
vpiHexStrVal = 4
vpiScalarVal = 5
vpiIntVal = 6
vpiRealVal = 7
vpiStringVal = 8
vpiVectorVal = 9
vpiStrengthVal = 10
vpiTimeVal = 11
vpiObjTypeVal = 12
vpiSuppressVal = 13
vpiShortIntVal = 14
vpiLongIntVal = 15
vpiShortRealVal = 16
vpiRawTwoStateVal = 17
vpiRawFourStateVal = 18
vpiNoDelay = 1
vpiInertialDelay = 2
vpiTransportDelay = 3
vpiPureTransportDelay = 4
vpiForceFlag = 5
vpiReleaseFlag = 6
vpiCancelEvent = 7
vpiReturnEvent = 0x1000
vpiUserAllocFlag = 0x2000
vpiOneValue = 0x4000
vpiPropagateOff = 0x8000
vpi0 = 0
vpi1 = 1
vpiZ = 2
vpiX = 3
vpiH = 4
vpiL = 5
vpiDontCare = 6
vpiSysTask = 1
vpiSysFunc = 2
vpiCompile = 1
vpiPLI = 2
vpiRun = 3
vpiNotice = 1
vpiWarning = 2
vpiError = 3
vpiSystem = 4
vpiInternal = 5


class t_vpi_time(ctypes.Structure):
    _fields_ = [("type", ctypes.c_int),
        ("high", ctypes.c_uint),
        ("low", ctypes.c_uint),
        ("real", ctypes.c_double)
    ]

class t_vpi_delay(ctypes.Structure):
    _fields_ = [("da", ctypes.POINTER(t_vpi_time)),
        ("no_of_delays", ctypes.c_int),
        ("time_type", ctypes.c_int),
        ("mtm_flag", ctypes.c_int),
        ("append_flag", ctypes.c_int),
        ("pulsere_flag", ctypes.c_int)
    ]

class t_vpi_vecval(ctypes.Structure):
    _fields_ = [("aval", ctypes.c_uint),
        ("bval", ctypes.c_uint)
    ]

class t_vpi_strengthval(ctypes.Structure):
    _fields_ = [("logic", ctypes.c_int),
        ("s0", ctypes.c_int),
        ("s1", ctypes.c_int)
    ]

class t_vpi_value_u(ctypes.Union):
    _fields_ = [
        ("str", ctypes.c_char_p),
        ("scalar", ctypes.c_int),
        ("integer", ctypes.c_int),
        ("double", ctypes.c_double),
        ("time", ctypes.POINTER(t_vpi_time)),
        ("vector", ctypes.POINTER(t_vpi_vecval)),
        ("strength", ctypes.POINTER(t_vpi_strengthval)),
        ("misc", ctypes.c_void_p)
    ]

class t_vpi_value(ctypes.Structure):
    _fields_ = [("format", ctypes.c_int),
        ("value", t_vpi_value_u)
    ]

class t_vpi_arrayvalue_u(ctypes.Union):
    _fields_ = [("integers", ctypes.POINTER(ctypes.c_int)),
                ("shortints", ctypes.POINTER(ctypes.c_short)),
                ("longints", ctypes.POINTER(ctypes.c_longlong)),
                ("rawvals", ctypes.POINTER(ctypes.c_void_p)),
                ("vectors", ctypes.POINTER(t_vpi_vecval)),
                ("times", ctypes.POINTER(t_vpi_time)),
                ("reals", ctypes.POINTER(ctypes.c_double)),
                ("shortreals", ctypes.POINTER(ctypes.c_float))
    ]

class t_vpi_arrayvalue(ctypes.Structure):
    _fields_ = [("format", ctypes.c_uint),
        ("flags", ctypes.c_uint),
        ("value", t_vpi_arrayvalue_u)
    ]

class t_vpi_systf_data(ctypes.Structure):
    _fields_ = [("type", ctypes.c_int),
        ("sysfunctype", ctypes.c_int),
        ("tfname", ctypes.c_char_p),
        ("calltf", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))), # PLI_INT32 (*)(PLI_BYTE8*)),
        ("compiletf", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))), # PLI_INT32 (*)(PLI_BYTE8*)),
        ("sizetf", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_byte))), # PLI_INT32 (*)(PLI_BYTE8*)),
        ("user_data", ctypes.c_char_p)
    ]

class t_vpi_vlog_info(ctypes.Structure):
    _fields_ = [("argc", ctypes.c_int),
        ("argv", ctypes.POINTER(ctypes.c_char_p)),
        ("product", ctypes.c_char_p),
        ("version", ctypes.c_char_p)
    ]

class t_vpi_error_info(ctypes.Structure):
    _fields_ = [("state", ctypes.c_int),
        ("level", ctypes.c_int),
        ("message", ctypes.c_char_p),
        ("product", ctypes.c_char_p),
        ("code", ctypes.c_char_p),
        ("file", ctypes.c_char_p),
        ("line", ctypes.c_int)
    ]

class t_cb_data(ctypes.Structure):
    _fields_ = [("reason", ctypes.c_int),
        ("cb_rtn", ctypes.c_void_p), #PLI_INT32 (*)(struct t_cb_data*)),
        ("obj", ctypes.c_void_p),
        ("time", ctypes.POINTER(t_vpi_time)),
        ("value", ctypes.POINTER(t_vpi_value)),
        ("index", ctypes.c_int),
        ("user_data", ctypes.c_char_p)
    ]


p_vpi_delay = ctypes.POINTER(t_vpi_delay)
p_vpi_vecval = ctypes.POINTER(t_vpi_vecval)
p_vpi_strengthval = ctypes.POINTER(t_vpi_strengthval)
p_vpi_value = ctypes.POINTER(t_vpi_value)
p_vpi_arrayvalue = ctypes.POINTER(t_vpi_arrayvalue)
p_vpi_systf_data = ctypes.POINTER(t_vpi_systf_data)
p_vpi_time = ctypes.POINTER(t_vpi_time)
p_vpi_value = ctypes.POINTER(t_vpi_value)
p_vpi_vlog_info = ctypes.POINTER(t_vpi_vlog_info)
p_vpi_error_info = ctypes.POINTER(t_vpi_error_info)
p_cb_data = ctypes.POINTER(t_cb_data)
vpi_chk_error = None
vpi_compare_objects = None
vpi_control = None
vpi_flush = None
vpi_free_object = None
vpi_get = None
vpi_get64 = None
vpi_get_cb_info = None
vpi_get_data = None
vpi_get_delays = None
vpi_get_str = None
vpi_get_systf_info = None
vpi_get_time = None
vpi_get_userdata = None
vpi_get_value = None
vpi_get_value_array = None
vpi_get_vlog_info = None
vpi_handle = None
vpi_handle_by_index = None
vpi_handle_by_multi_index = None
vpi_handle_by_name = None
vpi_handle_multi = None
vpi_iterate = None
vpi_mcd_close = None
vpi_mcd_flush = None
vpi_mcd_name = None
vpi_mcd_open = None
vpi_mcd_printf = None
vpi_mcd_vprintf = None
vpi_printf = None
vpi_put_data = None
vpi_put_delays = None
vpi_put_userdata = None
vpi_put_value = None
vpi_put_value_array = None
vpi_register_cb = None
vpi_register_systf = None
vpi_release_handle = None
vpi_remove_cb = None
vpi_scan = None
vpi_vprintf = None


def load(lib):
    global vpi_chk_error, vpi_compare_objects, vpi_control, vpi_flush, vpi_free_object, vpi_get, vpi_get64, vpi_get_cb_info
    global vpi_get_data, vpi_get_delays, vpi_get_str, vpi_get_systf_info, vpi_get_time, vpi_get_userdata, vpi_get_value, vpi_get_value_array
    global vpi_get_vlog_info, vpi_handle, vpi_handle_by_index, vpi_handle_by_multi_index, vpi_handle_by_name, vpi_handle_multi, vpi_iterate, vpi_mcd_close
    global vpi_mcd_flush, vpi_mcd_name, vpi_mcd_open, vpi_mcd_printf, vpi_mcd_vprintf, vpi_printf, vpi_put_data, vpi_put_delays
    global vpi_put_userdata, vpi_put_value, vpi_put_value_array, vpi_register_cb, vpi_register_systf, vpi_release_handle, vpi_remove_cb, vpi_scan
    global vpi_vprintf
    global unimplemented_vpi_funcs

    vpi_chk_error = getattr(lib, "vpi_chk_error")
    vpi_chk_error.restype = ctypes.c_int
    vpi_chk_error.argtypes = [p_vpi_error_info]
    vpi_compare_objects = getattr(lib, "vpi_compare_objects")
    vpi_compare_objects.restype = ctypes.c_int
    vpi_compare_objects.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    vpi_control = getattr(lib, "vpi_control")
    vpi_control.restype = ctypes.c_int
    vpi_control.argtypes = [ctypes.c_int]
    vpi_flush = getattr(lib, "vpi_flush")
    vpi_flush.restype = ctypes.c_int
    vpi_flush.argtypes = []
    vpi_free_object = getattr(lib, "vpi_free_object")
    vpi_free_object.restype = ctypes.c_int
    vpi_free_object.argtypes = [ctypes.c_void_p]
    vpi_get = getattr(lib, "vpi_get")
    vpi_get.restype = ctypes.c_int
    vpi_get.argtypes = [ctypes.c_int, ctypes.c_void_p]
    if hasattr(lib, "vpi_get64"):
        vpi_get64 = getattr(lib, "vpi_get64")
        vpi_get64.restype = ctypes.c_longlong
        vpi_get64.argtypes = [ctypes.c_int, ctypes.c_void_p]
    else:
        unimplemented_vpi_funcs.append("vpi_get64")
    if hasattr(lib, "vpi_get_cb_info"):
        vpi_get_cb_info = getattr(lib, "vpi_get_cb_info")
        vpi_get_cb_info.restype = None
        vpi_get_cb_info.argtypes = [ctypes.c_void_p, p_cb_data]
    if hasattr(lib, "vpi_get_data"):
        vpi_get_data = getattr(lib, "vpi_get_data")
        vpi_get_data.restype = ctypes.c_int
        vpi_get_data.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    vpi_get_delays = getattr(lib, "vpi_get_delays")
    vpi_get_delays.restype = None
    vpi_get_delays.argtypes = [ctypes.c_void_p, p_vpi_delay]
    vpi_get_str = getattr(lib, "vpi_get_str")
    vpi_get_str.restype = ctypes.c_char_p
    vpi_get_str.argtypes = [ctypes.c_int, ctypes.c_void_p]
    vpi_get_systf_info = getattr(lib, "vpi_get_systf_info")
    vpi_get_systf_info.restype = None
    vpi_get_systf_info.argtypes = [ctypes.c_void_p, p_vpi_systf_data]
    vpi_get_time = getattr(lib, "vpi_get_time")
    vpi_get_time.restype = None
    vpi_get_time.argtypes = [ctypes.c_void_p, p_vpi_time]
    vpi_get_userdata = getattr(lib, "vpi_get_userdata")
    vpi_get_userdata.restype = ctypes.c_void_p
    vpi_get_userdata.argtypes = [ctypes.c_void_p]
    vpi_get_value = getattr(lib, "vpi_get_value")
    vpi_get_value.restype = None
    vpi_get_value.argtypes = [ctypes.c_void_p, p_vpi_value]
    if hasattr(lib, "vpi_get_value_array"):
        vpi_get_value_array = getattr(lib, "vpi_get_value_array")
        vpi_get_value_array.restype = None
        vpi_get_value_array.argtypes = [ctypes.c_void_p, p_vpi_arrayvalue, ctypes.POINTER(ctypes.c_int), ctypes.c_uint]
    vpi_get_vlog_info = getattr(lib, "vpi_get_vlog_info")
    vpi_get_vlog_info.restype = ctypes.c_int
    vpi_get_vlog_info.argtypes = [p_vpi_vlog_info]
    vpi_handle = getattr(lib, "vpi_handle")
    vpi_handle.restype = ctypes.c_void_p
    vpi_handle.argtypes = [ctypes.c_int, ctypes.c_void_p]
    vpi_handle_by_index = getattr(lib, "vpi_handle_by_index")
    vpi_handle_by_index.restype = ctypes.c_void_p
    vpi_handle_by_index.argtypes = [ctypes.c_void_p, ctypes.c_int]
    if hasattr(lib, "vpi_handle_by_multi_index"):
        vpi_handle_by_multi_index = getattr(lib, "vpi_handle_by_multi_index")
        vpi_handle_by_multi_index.restype = ctypes.c_void_p
        vpi_handle_by_multi_index.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    vpi_handle_by_name = getattr(lib, "vpi_handle_by_name")
    vpi_handle_by_name.restype = ctypes.c_void_p
    vpi_handle_by_name.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    if hasattr(lib, "vpi_handle_multi"):
        vpi_handle_multi = getattr(lib, "vpi_handle_multi")
        vpi_handle_multi.restype = ctypes.c_void_p
        vpi_handle_multi.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
    vpi_iterate = getattr(lib, "vpi_iterate")
    vpi_iterate.restype = ctypes.c_void_p
    vpi_iterate.argtypes = [ctypes.c_int, ctypes.c_void_p]
    vpi_mcd_close = getattr(lib, "vpi_mcd_close")
    vpi_mcd_close.restype = ctypes.c_uint
    vpi_mcd_close.argtypes = [ctypes.c_uint]
    vpi_mcd_flush = getattr(lib, "vpi_mcd_flush")
    vpi_mcd_flush.restype = ctypes.c_int
    vpi_mcd_flush.argtypes = [ctypes.c_uint]
    vpi_mcd_name = getattr(lib, "vpi_mcd_name")
    vpi_mcd_name.restype = ctypes.c_char_p
    vpi_mcd_name.argtypes = [ctypes.c_uint]
    vpi_mcd_open = getattr(lib, "vpi_mcd_open")
    vpi_mcd_open.restype = ctypes.c_uint
    vpi_mcd_open.argtypes = [ctypes.c_char_p]
    vpi_mcd_printf = getattr(lib, "vpi_mcd_printf")
    vpi_mcd_printf.restype = ctypes.c_int
    vpi_mcd_printf.argtypes = [ctypes.c_uint, ctypes.c_char_p]
    vpi_printf = getattr(lib, "vpi_printf")
    vpi_printf.restype = ctypes.c_int
    vpi_printf.argtypes = [ctypes.c_char_p]
    if hasattr(lib, "vpi_put_data"):
        vpi_put_data = getattr(lib, "vpi_put_data")
        vpi_put_data.restype = ctypes.c_int
        vpi_put_data.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    vpi_put_delays = getattr(lib, "vpi_put_delays")
    vpi_put_delays.restype = None
    vpi_put_delays.argtypes = [ctypes.c_void_p, p_vpi_delay]
    vpi_put_userdata = getattr(lib, "vpi_put_userdata")
    vpi_put_userdata.restype = ctypes.c_int
    vpi_put_userdata.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    vpi_put_value = getattr(lib, "vpi_put_value")
    vpi_put_value.restype = ctypes.c_void_p
    vpi_put_value.argtypes = [ctypes.c_void_p, p_vpi_value, p_vpi_time, ctypes.c_int]
    if hasattr(lib, "vpi_put_value_array"):
        vpi_put_value_array = getattr(lib, "vpi_put_value_array")
        vpi_put_value_array.restype = None
        vpi_put_value_array.argtypes = [ctypes.c_void_p, p_vpi_arrayvalue, ctypes.POINTER(ctypes.c_int), ctypes.c_uint]
    vpi_register_cb = getattr(lib, "vpi_register_cb")
    vpi_register_cb.restype = ctypes.c_void_p
    vpi_register_cb.argtypes = [p_cb_data]
    vpi_register_systf = getattr(lib, "vpi_register_systf")
    vpi_register_systf.restype = ctypes.c_void_p
    vpi_register_systf.argtypes = [p_vpi_systf_data]
    if hasattr(lib, "vpi_release_handle"):
        vpi_release_handle = getattr(lib, "vpi_release_handle")
        vpi_release_handle.restype = ctypes.c_int
        vpi_release_handle.argtypes = [ctypes.c_void_p]
    vpi_remove_cb = getattr(lib, "vpi_remove_cb")
    vpi_remove_cb.restype = ctypes.c_int
    vpi_remove_cb.argtypes = [ctypes.c_void_p]
    vpi_scan = getattr(lib, "vpi_scan")
    vpi_scan.restype = ctypes.c_void_p
    vpi_scan.argtypes = [ctypes.c_void_p]
