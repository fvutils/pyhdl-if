
module hdl2hvl_fifo;
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

    wire ready;
    reg valid = 1;
    reg[31:0] data = 1;

    always @(posedge clock) begin
        $display("clock: reset=%0d", reset);
        if (ready && valid) begin
            $display("Write data: 0x%08h", data);
            data <= data + 1;
        end
    end

    tlm_hdl2hvl_fifo #(
        .Tdepth(4)
        ) u_fifo (
        .clock(clock),
        .reset(reset),
        .ready(ready),
        .valid(valid),
        .dat_i(data)
    );

    initial begin
        automatic int i, tdat;
        while (reset == 1) begin
            @(posedge clock);
        end
        for (i=0; i<20; i=i+1) begin
            u_fifo.get(tdat);
            $display("Read data: 0x%08h", tdat);
        end
        $finish;
    end
endmodule
