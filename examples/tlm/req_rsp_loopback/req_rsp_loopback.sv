
module req_rsp_loopback;
    import pyhdl_if::*;

    reg clock = 0;
    reg reset = 1;

    initial begin
        forever begin
            #10ns;
            clock = ~clock;
        end 
    end

    initial begin
        #100ns;
        reset = 0;
    end

    wire[31:0]      req_data;
    wire            req_ready;
    wire            req_valid;

    ReqRspLoopback u_loopback(
        .clock(clock),
        .reset(reset),
        .req_valid(req_valid),
        .req_ready(req_ready),
        .req_data(req_data),
        .rsp_valid(req_valid),
        .rsp_ready(req_ready),
        .rsp_data(req_data)
    );

    always @(posedge clock) begin
	    if (!reset && req_valid && req_ready) begin
		    $display("req_data: 0x%08h", req_data);
	    end
    end


    initial begin
        automatic PyObject req_rsp_loopback_m = PyImport_ImportModule("req_rsp_loopback");
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

endmodule
