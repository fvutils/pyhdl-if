
module call_sv_bfm;
    import pyhdl_if::*;
    import call_sv_bfm_pkg::*;

    reg clk = 0;
    reg reset = 1;
    initial begin
        pyhdl_if_start();

        clk = 0;
        forever begin
            #10ns;
            clk = ~clk;
        end
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

    initial begin
        automatic Test test;

        $dumpfile("trace.vcd");
        $dumpvars;
        #50ns;
        reset = 0;

        // Create an instance of the Test class and run
        $display("%0t --> run", $time);
        test = new();
        test.run(init_bfm.m_api_obj.m_obj);
        $display("%0t <-- run", $time);
        #30us;
        $finish;
    end

endmodule
