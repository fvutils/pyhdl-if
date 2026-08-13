`ifndef PYHDL_IF_VPI
`ifdef __ICARUS__
`define PYHDL_IF_VPI 1
`endif /* __ICARUS__ */
`endif /* PYHDL_IF_VPI */

`ifdef PYHDL_IF_VPI
`define ENTITY_TYPE module
`define END_ENTITY_TYPE endmodule
`else /* PYHDL_IF_VPI */
`define ENTITY_TYPE interface
`define END_ENTITY_TYPE endinterface
`endif /* PYHDL_IF_VPI */

`ENTITY_TYPE WishboneInitiator #(
    parameter WIDTH_req = 32+32,
    parameter DEPTH_req_req = 1,
    parameter DEPTH_req_rsp = 1,
    parameter WIDTH_rsp = 32,
    parameter DEPTH_rsp_req = 1,
    parameter DEPTH_rsp_rsp = 1
    ) (
        input clock,
        input reset,
        output req_valid,
        input  req_ready,
        output [WIDTH_req-1:0] req_data,
        input  rsp_valid,
        output rsp_ready,
        input [WIDTH_rsp-1:0] rsp_data
    );

    pyhdl_if_req_fifo #(
        .Twidth(WIDTH_req),
        .Tdepth(DEPTH_req)
    ) req (
        .clock(clock),
        .reset(reset),
        .valid(req_valid),
        .ready(req_ready),
        .dat_o(req_data)
    );
    
    pyhdl_if_rsp_fifo #(
        .Twidth(WIDTH_rsp),
        .Tdepth(DEPTH_rsp)
    ) rsp (
        .clock(clock),
        .reset(reset),
        .valid(rsp_valid),
        .ready(rsp_ready),
        .dat_i(rsp_data)
    );
    
`END_ENTITY_TYPE
`undef ENTITY_TYPE
`undef END_ENTITY_TYPE
