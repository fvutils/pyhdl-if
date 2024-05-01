#****************************************************************************
#* gen_ifc_sv.py
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
from hdl_if.tlm.tlm_method import TlmMethod
from .type_info_tlm_if import TypeInfoTlmIF

class GenIfcSv(object):

    def __init__(self, is_vlog=False):
        self._ind = ""
        self._fp = None
        self._is_vlog = is_vlog

    def gen_ifc_module(self, ifc : TypeInfoTlmIF, fp):
        from hdl_if.tlm.tlm_method import TlmMethodKind
        self._fp = fp
        self._ind = ""

        self.println("`ifndef PYHDL_IF_VPI")
        self.println("`ifdef __ICARUS__")
        self.println("`define PYHDL_IF_VPI 1")
        self.println("`endif /* __ICARUS__ */")
        self.println("`endif /* PYHDL_IF_VPI */")
        self.println()
        self.println("`ifdef PYHDL_IF_VPI")
        self.println("`define ENTITY_TYPE module")
        self.println("`define END_ENTITY_TYPE endmodule")
        self.println("`else /* PYHDL_IF_VPI */")
        self.println("`define ENTITY_TYPE interface")
        self.println("`define END_ENTITY_TYPE endinterface")
        self.println("`endif /* PYHDL_IF_VPI */")
        self.println()

        self.println("`ENTITY_TYPE %s #(" % ifc.name)
        self.inc_ind()

        # TODO: Eventually, we will want parameters here

        print("ifc.getMethods: %d" % len(ifc.getMethods()))

        for i,m in enumerate(ifc.getMethods()):
            if m.kind in (TlmMethodKind.Req, TlmMethodKind.Rsp):
                self.println("parameter WIDTH_%s = %s," % (
                    m.name,
                    self.getWidthExpr(m.t1 if m.kind == TlmMethodKind.Req else m.t2)))
            else:
                self.println("parameter WIDTH_%s_req = %s," % (
                    m.name,
                    self.getWidthExpr(m.t1)))
                self.println("parameter WIDTH_%s_rsp = %s," % (
                    m.name,
                    self.getWidthExpr(m.t2)))
            self.println("parameter DEPTH_%s_req = 1," % m.name)
            self.println("parameter DEPTH_%s_rsp = 1%s" % (
                m.name,
                "," if (i+1)<len(ifc.getMethods()) else ""))

        self.println(") (")
        self.inc_ind()
        self.println("input clock,")
        self.println("input reset,")
        for i,m in enumerate(ifc.getMethods()):
            if m.kind == TlmMethodKind.Req:
                self.println("output %s_valid," % m.name)
                self.println("input  %s_ready," % m.name)
                self.println("output [WIDTH_%s-1:0] %s_data%s" % (
                    m.name,
                    m.name,
                    "," if i+1<len(ifc.getMethods()) else ""
                ))
            elif m.kind == TlmMethodKind.Rsp:
                self.println("input  %s_valid," % m.name)
                self.println("output %s_ready," % m.name)
                self.println("input [WIDTH_%s-1:0] %s_data%s" % (
                    m.name,
                    m.name,
                    "," if i+1<len(ifc.getMethods()) else ""
                ))
            elif m.kind == TlmMethodKind.ReqRsp:
                self.println("output %s_req_valid," % m.name)
                self.println("input  %s_req_ready," % m.name)
                self.println("output [WIDTH_%s_req-1:0] %s_req_data," % (
                    m.name,
                    m.name
                ))
                self.println("input  %s_rsp_valid," % m.name)
                self.println("output %s_rsp_ready," % m.name)
                self.println("input [WIDTH_%s_rsp-1:0] %s_rsp_data%s" % (
                    m.name,
                    m.name,
                    "," if i+1<len(ifc.getMethods()) else ""
                ))
            else:
                raise Exception("Unhandled method type %s" % str(m.kind))
        self.dec_ind()
        self.println(");")
        self.dec_ind()

        self.println()
        self.inc_ind()

        for i,m in enumerate(ifc.getMethods()):
            if i:
                self.println()
            if m.kind == TlmMethodKind.Req:
                self.println("pyhdl_if_req_fifo #(")
                self.inc_ind()
                self.println(".Twidth(WIDTH_%s)," % m.name)
                self.println(".Tdepth(DEPTH_%s)" % m.name)
                self.dec_ind()
                self.println(") %s (" % m.name)
                self.inc_ind()
                self.println(".clock(clock),")
                self.println(".reset(reset),")
                self.println(".valid(%s_valid)," % m.name)
                self.println(".ready(%s_ready)," % m.name)
                self.println(".dat_o(%s_data)" % m.name)
                self.dec_ind()
                self.println(");")
            elif m.kind == TlmMethodKind.Rsp:
                self.println("pyhdl_if_rsp_fifo #(")
                self.inc_ind()
                self.println(".Twidth(WIDTH_%s)," % m.name)
                self.println(".Tdepth(DEPTH_%s)" % m.name)
                self.dec_ind()
                self.println(") %s (" % m.name)
                self.inc_ind()
                self.println(".clock(clock),")
                self.println(".reset(reset),")
                self.println(".valid(%s_valid)," % m.name)
                self.println(".ready(%s_ready)," % m.name)
                self.println(".dat_i(%s_data)" % m.name)
                self.dec_ind()
                self.println(");")
            elif m.kind == TlmMethodKind.ReqRsp:
                self.println("pyhdl_if_reqrsp_fifo #(")
                self.inc_ind()
                self.println(".TReqWidth(WIDTH_%s_req)," % m.name)
                self.println(".TReqDepth(DEPTH_%s_req)," % m.name)
                self.println(".TRspWidth(WIDTH_%s_rsp)," % m.name)
                self.println(".TRspDepth(DEPTH_%s_rsp)" % m.name)
                self.dec_ind()
                self.println(") %s (" % m.name)
                self.inc_ind()
                self.println(".clock(clock),")
                self.println(".reset(reset),")
                self.println(".req_valid(%s_req_valid)," % m.name)
                self.println(".req_ready(%s_req_ready)," % m.name)
                self.println(".req_dat_o(%s_req_data)," % m.name)
                self.println(".rsp_valid(%s_rsp_valid)," % m.name)
                self.println(".rsp_ready(%s_rsp_ready)," % m.name)
                self.println(".rsp_dat_i(%s_rsp_data)" % m.name)
                self.dec_ind()
                self.println(");")

        self.println()
        self.dec_ind()

        self.println("`END_ENTITY_TYPE")

        self.println("`undef ENTITY_TYPE")
        self.println("`undef END_ENTITY_TYPE")

    _type_width_m = {
        ctypes.c_longlong : 64,
        ctypes.c_ulonglong : 64,
        ctypes.c_int64 : 64,
        ctypes.c_uint64 : 64,
        ctypes.c_int : 32,
        ctypes.c_uint : 32, 
        ctypes.c_int32 : 32, 
        ctypes.c_uint32 : 32, 
        ctypes.c_short : 16,
        ctypes.c_ushort : 16, 
        ctypes.c_int16 : 16, 
        ctypes.c_uint16 : 16, 
        ctypes.c_byte : 8,
        ctypes.c_ubyte : 8, 
        ctypes.c_char : 8,
        ctypes.c_int8 : 8, 
        ctypes.c_uint8 : 8, 
    }
    
    def getWidthExpr(self, t):
        bits = ""
        for f in t._fields_:
            if len(f) > 2:
                sz = f[2]
            else:
                sz = GenIfcSv._type_width_m[f[1]]
            if len(bits) > 0:
                bits += "+"
            bits += str(sz)
        return bits

    def gen_types_pkg(self, ifc : TypeInfoTlmIF, fp):
        self._fp = fp
        self._ind = ""

    def println(self, msg=""):
        self._fp.write("%s%s\n" % (self._ind, msg))
    
    def write(self, msg):
        self._fp.write(msg)

    def inc_ind(self):
        self._ind += "    "
    
    def dec_ind(self):
        if len(self._ind) > 4:
            self._ind = self._ind[4:]
        else:
            self._ind = ""


