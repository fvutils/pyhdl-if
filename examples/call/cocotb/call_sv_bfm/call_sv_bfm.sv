
module WishboneInitiatorBFM(
    input           clock,
    input           reset,
    output reg[31:0]        adr,
    output reg[31:0]        dat_w,
    input[31:0]             dat_r,
    output                  cyc,
    input                   err,
    output reg[3:0]         sel,
    output                  stb,
    input                   ack,
    output reg              we
);
    `include "hdl_call_if_api.svh"

    reg [31:0]      bfm_dat_w, bfm_dat_r, bfm_adr;
    reg[3:0]        bfm_sel;
    reg             bfm_we, bfm_req, bfm_ack;
    reg             state;
    assign stb = (state == 1'b1);
    assign cyc = (state == 1'b1);
    always @(posedge clock or reset) begin
        if (reset) begin
            bfm_dat_w = {32{1'b0}};
            bfm_dat_r = {32{1'b0}};
            bfm_adr = {32{1'b0}};
            bfm_sel = {4{1'b0}};
            bfm_we = 1'b0;
            bfm_req = 1'b0;
            bfm_ack = 1'b0;
            state <= 1'b0;
        end else begin
            case (state)
                1'b0: begin
                    if (bfm_req) begin
                        sel <= bfm_sel;
                        we <= bfm_we;
                        adr <= bfm_adr;
                        dat_w <= bfm_dat_w;
                        bfm_req = 0;
                        state <= 1'b1;
                    end
                end
                1'b1: begin
                    if (cyc && stb && ack) begin
                        bfm_dat_r <= dat_r;
                        bfm_ack = 1;
                        state <= 1'b0;
                    end
                end
            endcase
        end
    end

    task bfm_write(int unsigned adr_v, int unsigned dat_v);
        while (bfm_req === 1'b1) begin
            @(posedge clock);
        end
        bfm_adr = adr_v;
        bfm_we = 1'b1;
        bfm_sel = {4{1'b1}};
        bfm_dat_w = dat_v;
        bfm_req = 1'b1;
        while (bfm_ack === 1'b0) begin
            @(posedge clock);
        end
        bfm_ack = 1'b0;
    endtask

    task bfm_read(output int unsigned dat_v, int unsigned adr_v);
        while (bfm_req === 1'b1) begin
            @(posedge clock);
        end
        bfm_adr = adr_v;
        bfm_we = 1'b0;
        bfm_sel = {4{1'b0}};
        bfm_dat_w = {32{1'b0}};
        bfm_req = 1'b1;
        while (bfm_ack === 1'b0) begin
            @(posedge clock);
        end
        dat_v = bfm_dat_r;
        bfm_ack = 1'b0;
    endtask

    class WishboneInitiatorImpl extends WishboneInitiator;
        virtual task write(int unsigned addr, int unsigned data);
            $display("write");
            $display("--> write");
            bfm_write(addr, data);
            $display("<-- write");
            #10ns;
        endtask
        
        virtual task read(output int unsigned retval, input int unsigned addr);
            $display("--> read");
            bfm_read(retval, addr);
            $display("<-- read");
        endtask

    endclass

    WishboneInitiatorImpl       m_api_obj;

    // Register ourselves with the PyHDL-IF object registry
    initial begin : init
        m_api_obj = new();
        $display("Path: %m");
        pyhdl_if::pyhdl_if_registerObject(m_api_obj.m_obj, $sformatf("%m"), 1);
    end
endmodule

module call_sv_bfm;
    import pyhdl_if::*;

    reg clk = 0;
    reg reset = 1;
    initial begin
        pyhdl_pi_if_start();

        clk = 0;
        forever begin
            #10ns;
            clk = ~clk;
        end
    end

    initial begin
        $dumpfile("trace.vcd");
        $dumpvars;
        #50ns;
        reset = 0;
        #15us;
        $finish;
    end

    wire[31:0] dat_r, dat_w;
    wire[31:0] adr;
    wire stb, cyc, we;
    reg  ack_r;
    wire ack = (ack_r && cyc && stb);

    always @(posedge clk or reset) begin
        if (reset) begin
            ack_r <= 1'b0;
        end else begin
            ack_r <= (stb & cyc);
        end
    end

    assign dat_r = dat_w;

    WishboneInitiatorBFM    init_bfm(
        .clock(clk),
        .reset(reset),
        .adr(adr),
        .dat_r(dat_r),
        .dat_w(dat_w),
        .stb(stb),
        .cyc(cyc),
        .ack(ack),
        .we(we)
    );

endmodule

