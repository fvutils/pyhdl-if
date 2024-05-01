/**
 * pyhdl_if_reqrsp_fifo.sv
 *
 * Copyright 2024 Matthew Ballance and Contributors
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
`ifndef PYHDL_IF_VPI
`ifdef __ICARUS__
`define PYHDL_IF_VPI 1
`endif
`endif

`ifdef PYHDL_IF_VPI
`define ENTITY_TYPE module
`define END_ENTITY_TYPE endmodule
`else
`define ENTITY_TYPE interface
`define END_ENTITY_TYPE endinterface
`endif

`ENTITY_TYPE pyhdl_if_reqrsp_fifo #(
    parameter TReqWidth=32, 
    parameter TReqDepth=1,
    parameter TRspWidth=32, 
    parameter TRspDepth=TReqDepth) (
    input                   clock,
    input                   reset,
    output                  req_valid,
    input                   req_ready,
    output[TReqWidth-1:0]   req_dat_o,
    input                   rsp_valid,
    output                  rsp_ready,
    input[TRspWidth-1:0]    rsp_dat_i
    );
`ifndef PYHDL_IF_VPI
    import pyhdl_if::*;
`endif
    localparam ReqPointer_w = (TReqDepth > 1)?$clog2(TReqDepth):1;
    localparam ReqCounter_w = ReqPointer_w+1;
    localparam RspPointer_w = (TRspDepth > 1)?$clog2(TRspDepth):1;
    localparam RspCounter_w = RspPointer_w+1;

    reg[TReqWidth-1:0]     req_fifo[TReqDepth-1:0];
    reg[ReqPointer_w-1:0]  req_rptr;
    reg[ReqPointer_w-1:0]  req_wptr;
    reg[ReqCounter_w-1:0]  req_count;

    assign req_valid = (req_count != 0);
    assign req_dat_o = req_fifo[req_rptr];

    wire                    req_pop = (req_valid && req_ready);
    reg                     req_push;
    wire                    req_push_v = (req_push && req_count != TReqDepth);
    reg[TReqWidth-1:0]      req_push_dat;

    always @(posedge clock or posedge reset) begin
        if (reset) begin
            req_rptr <= {ReqPointer_w{1'b0}};
            req_wptr <= {ReqPointer_w{1'b0}};
            req_count <= {ReqCounter_w{1'b0}};
            req_push = 0;
        end else begin
            case ({req_push_v, req_pop})
            2'b00: begin end
            2'b01: begin // Pop with no push
                req_count <= req_count - 1;
                req_rptr <= ((req_rptr+1) & (TReqDepth-1));
            end
            2'b10: begin // Push with no pop
                req_fifo[req_wptr] <= req_push_dat;
                req_count <= ((req_count + 1) % (TReqDepth+1));
                req_wptr <= ((req_wptr+1) & (TReqDepth-1));
                req_push = 0;
            end
            2'b11: begin // Simultaneous push and pop
                req_fifo[req_wptr] <= req_push_dat;
                req_wptr <= ((req_wptr+1) & (TReqDepth-1));
                req_rptr <= ((req_rptr+1) & (TReqDepth-1));
                req_push = 0;
            end
            endcase
        end
    end

    task put(input reg[TReqWidth-1:0]  dat);
    begin
        while (reset !== 0) begin
            @(posedge clock);
        end

        while (req_push == 1) begin
            @(posedge clock);
        end

        req_push = 1'b1;
        req_push_dat = dat;

        // Wait to take effect
    end
    endtask

    reg[TRspWidth-1:0]     rsp_fifo[TRspDepth-1:0];
    reg[RspPointer_w-1:0]  rsp_rptr;
    reg[RspPointer_w-1:0]  rsp_wptr;
    reg[RspCounter_w-1:0]  rsp_count;

    assign rsp_ready = ((rsp_count != TRspDepth) & !reset);
    wire rsp_push = (rsp_valid & rsp_ready);
    reg rsp_pop;

    always @(posedge clock or posedge reset) begin
        if (reset) begin
            rsp_rptr <= {RspPointer_w{1'b0}};
            rsp_wptr <= {RspPointer_w{1'b0}};
            rsp_count <= {RspCounter_w{1'b0}};
            rsp_pop = 0;
        end else begin
            case ({rsp_push, rsp_pop})
            2'b00: begin end
            2'b01: begin // Pop with no push
                rsp_count <= rsp_count - 1;
                rsp_rptr <= ((rsp_rptr + 1) & (TRspDepth-1));
                rsp_pop = 0;
            end
            2'b10: begin // Push with no pop
                rsp_fifo[rsp_wptr] <= rsp_dat_i;
                rsp_count <= ((rsp_count + 1) % (TRspDepth+1));
                rsp_wptr <= ((rsp_wptr+1) & (TRspDepth-1));
            end
            2'b11: begin // Simultaneous push and pop
                rsp_fifo[rsp_wptr] <= rsp_dat_i;
                rsp_wptr <= ((rsp_wptr+1) & (TRspDepth-1));
                rsp_rptr <= ((rsp_rptr + 1) & (TRspDepth-1));
                rsp_pop = 0;
            end
            endcase
        end
    end

    task get(output reg[TRspWidth-1:0] dat_o);
    begin
        $display("--> get");
        while (reset !== 0) begin
            @(posedge clock);
        end

        while ((rsp_count == 0 && !rsp_push) || rsp_pop == 1) begin
            @(posedge clock);
        end

        if (rsp_count == 0) begin
            dat_o = rsp_dat_i;
        end else begin
            dat_o = rsp_fifo[rsp_rptr];
        end
        rsp_pop = 1;
        $display("<-- get");
    end
    endtask

`ifndef PYHDL_IF_VPI
    class Closure implements ICallApi;

        virtual function PyObject invokeFunc(
            string      method,
            PyObject    args);
            $display("Fatal Error: unexpected function invocation %0s", method);
            $finish;
        endfunction

        virtual task invokeTask(
            output PyObject    retval,
            input string       method,
            input PyObject     args);
            bit [TReqWidth-1:0]    tmp_req = 0;
            bit [TRspWidth-1:0]    tmp_rsp = 0;
            PyObject obj, intval, rshift;

            $display("invokeTask: method=%0s", method);

            retval = None;

            case (method)
                "get": begin
                    get(tmp_rsp[TRspWidth-1:0]);

                    if (TRspWidth <= 64) begin
                        retval = PyLong_FromUnsignedLongLong(tmp_rsp);
                    end else begin
                        $display("TODO: implement >64-bit");
                        $finish;
                    end
                end
                "put": begin
                    intval = PyTuple_GetItem(args, 0);

                    if (TReqWidth <= 64) begin
                        longint unsigned lval;
                        lval = PyLong_AsUnsignedLongLong(intval);
                        tmp_req = lval[TReqWidth-1:0];
                    end else begin
                        rshift = PyObject_GetAttrString(intval, "__rshift__");
                        $display("TODO: implement >64-bit");
                        $finish;
                    end
                    put(tmp_req); 
                end
                default: begin
                    $display("Fatal Error: unsupported task call %0s", method);
                    $finish;
                end
            endcase
        endtask

    endclass

    Closure             __closure;
    PyObject            __obj;

    initial begin : fifo_reg
        __closure = new();
        __obj = pyhdl_tlm_if_registerStream(
            StreamKind_Req,
            $sformatf("%m"),
            __closure);
    end
`else /* VPI */
    reg[31:0]           __obj;
    reg                 __ev = 0;
    reg[31:0]           __req;
    reg[31:0]               __None;
    reg[TReqWidth-1:0]      __tmp_req;
    reg[TRspWidth-1:0]      __tmp_rsp;


    initial begin : fifo_reg
        __None = $pyhdl_if_None;
        __obj = $pyhdl_if_TlmApi_registerStream("reqrsp", __ev);

        $pyhdl_if_CallApi_setMethodId(__obj, "put", 1);
        $pyhdl_if_CallApi_setMethodId(__obj, "get", 2);

        forever begin
            __req = $pyhdl_if_CallApi_nextReq(__obj);
            $display("__req='h%08h ; __None='h%08h", __req, __None);
            if (__req !== __None) begin
                $Py_IncRef(__req);
                case ($PyLong_AsLong($PyObject_GetAttrString(__req, "id")))
                1: begin // put
                    $display("Processing req command");
                    $pyhdl_if_TlmApi_reqGet(__req, __tmp_req);
                    $display("__tmp: 'h%08h", __tmp_req);
                    put(__tmp_req);
                    $pyhdl_if_CallApi_ack(__req, 0);
                    $Py_DecRef(__req);
                end
                2: begin // get
                    $display("Processing rsp command");
                    get(__tmp_rsp);
                    $pyhdl_if_TlmApi_rspAck(__req, __tmp_rsp);
                end
                endcase
            end else begin
                @(__ev);
            end
        end
    end
`endif /* PYHDL_IF_VPI */


`END_ENTITY_TYPE

`undef ENTITY_TYPE
`undef END_ENTITY_TYPE
