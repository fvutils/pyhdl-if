
module hvl2hdl_fifo;
    reg clock = 0;
    reg reset = 1;

    initial begin
        forever begin
            #10ns;
            clock <= ~clock;
        end
    end 

    initial begin
        repeat (20) begin
            @(posedge clock);
        end
        reset = 0;
    end

    reg ready = 1;
    wire valid;
    wire[31:0] data;

    always @(posedge clock) begin
        $display("clock: reset=%0d", reset);
        if (ready && valid) begin
            $display("data: 0x%08h", data);
        end
    end

    tlm_hvl2hdl_fifo #(
        .Tdepth(4)
        ) u_fifo (
        .clock(clock),
        .reset(reset),
        .ready(ready),
        .valid(valid),
        .dat_o(data)
    );

    initial begin
        automatic int i;
        while (reset == 1) begin
            @(posedge clock);
        end
        for (i=1; i<=20; i=i+1) begin
            u_fifo.put(i);
        end
        $finish;
    end
endmodule
