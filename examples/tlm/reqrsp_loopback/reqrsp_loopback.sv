
`ifndef __ICARUS__
`timescale 1ns/1ns
`endif
module reqrsp_loopback;
`ifndef __ICARUS__
    import pyhdl_if::*;
`endif

    reg clock = 0;
    reg reset = 1;

    initial begin
        forever begin
`ifdef __ICARUS__
            #10;
`else
            #10ns;
`endif
            clock = ~clock;
        end 
    end

    initial begin
`ifdef __ICARUS__
        #100;
`else
        #100ns;
`endif
        reset = 0;
    end

    wire[31:0]      req_data;
    wire            req_ready;
    wire            req_valid;

    ReqRspLoopback #(
        .DEPTH_req_req(2),
        .DEPTH_req_rsp(2)
        ) u_loopback (
        .clock(clock),
        .reset(reset),
        .req_req_valid(req_valid),
        .req_req_ready(req_ready),
        .req_req_data(req_data),
        .req_rsp_valid(req_valid),
        .req_rsp_ready(req_ready),
        .req_rsp_data(req_data)
    );

/*
    initial begin
        bit[31:0]     tmp;

        forever begin
            u_loopback.rsp.get(tmp);
            $display("Have tmp: %08h", tmp);
        end

    end
 */

    always @(posedge clock) begin
	    if (!reset && req_valid && req_ready) begin
		    $display("req_data: 0x%08h", req_data);
	    end
    end


`ifndef __ICARUS__
    initial begin
        automatic PyObject req_rsp_loopback_m = PyImport_ImportModule("reqrsp_loopback");
        automatic PyObject init = PyObject_GetAttrString(req_rsp_loopback_m, "init");
        automatic PyObject args = PyTuple_New(0);

        $dumpfile("trace.vcd");
        $dumpvars();

        pyhdl_pi_if_start();

        #0;

        void'(pyhdl_pi_if_HandleErr(PyObject_Call(init, args, null)));

        pyhdl_pi_if_idle();

        #1us;
        $finish;
    end
`else /* ICARUS */
    reg[31:0]       req_rsp_loopback_m;
    reg[31:0]       init_h;
    reg[31:0]       args;
    reg[31:0]       res;

    initial begin
        $dumpfile("trace.vcd");
        $dumpvars();

        req_rsp_loopback_m = $PyImport_ImportModule("reqrsp_loopback");
        init_h = $PyObject_GetAttrString(req_rsp_loopback_m, "init");
        args = $PyTuple_New(0);

        #0;

        res = $PyObject_Call(init_h, args, 0);

        $pyhdl_if_idle();

        #1000;
        $finish;
    end
`endif

endmodule
