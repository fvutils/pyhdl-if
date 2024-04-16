
package reqrsp_fifo_pkg;
    typedef struct packed {
        bit[7:0]       data;
        bit[7:0]       data2;
    } req_t;
    typedef struct packed {
        bit[7:0]       data;
        bit[7:0]       data2;
    } rsp_t;
endpackage

module reqrsp_fifo #(
    parameter Wreq=$bits(reqrsp_fifo_pkg::req_t), 
    parameter Wrsp=$bits(reqrsp_fifo_pkg::rsp_t)) (
    input               clock,
    input               reset,
    output              req_valid,
    output [Wreq-1:0]   req_data,
    input               req_ready,
    input               rsp_valid,
    input [Wrsp-1:0]    rsp_data,
    output              rsp_ready);

    tlm_hvl2hdl_fifo #(
        .Twidth(Wreq),
        .Tdepth(1)
    ) req (
        .clock(clock),
        .reset(reset),
        .valid(req_valid),
        .dat_o(req_data),
        .ready(req_ready)
    );

    tlm_hdl2hvl_fifo #(
        .Twidth(Wrsp),
        .Tdepth(1)
    ) rsp (
        .clock(clock),
        .reset(reset),
        .valid(rsp_valid),
        .dat_i(rsp_data),
        .ready(rsp_ready)
    );

    initial begin
        // pyhdl_tlm_if::hti_registerIF("reqrsp_fifo", $sformatf("%m"), 2);
    end

endmodule

module reqrsp_fifo_loopback();
    import pyhdl_dpi_if::*;
    import reqrsp_fifo_pkg::*;

    reg clock = 0;
    reg reset = 1;
    initial begin
        forever begin
            #10ns;
            clock <= ~clock;
        end
    end

    initial begin
        reset <= 1'b1;
        #100ns;
        reset <= 1'b0;

        #100us;
        $finish;
    end

    wire req_valid, req_ready;
    req_t req_data;
    wire rsp_valid, rsp_ready;
    rsp_t rsp_data;

    assign rsp_data = req_data;
    assign req_ready = rsp_ready;
    assign rsp_valid = req_valid;

    reqrsp_fifo u_reqrsp(
        .clock(clock),
        .reset(reset),
        .req_valid(req_valid),
        .req_data(req_data),
        .req_ready(req_ready),
        .rsp_valid(rsp_valid),
        .rsp_data(rsp_data),
        .rsp_ready(rsp_ready));

    initial begin
        automatic PyObject reqrsp_fifo_loopback_m = pyhdl_pi_if_HandleErr(PyImport_ImportModule("reqrsp_fifo_loopback"));
        automatic PyObject run_m = PyObject_GetAttrString(reqrsp_fifo_loopback_m, "run");
        automatic PyObject args = PyTuple_New(0);

        pyhdl_pi_if_start();

        pyhdl_pi_if_mkTask(PyObject_Call(run_m, args, null));
    end

endmodule
