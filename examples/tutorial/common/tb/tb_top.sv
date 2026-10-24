/**
 * Testbench top shared by every example: the DUT, its ports and run_test().
 * Examples differ only in the test they select with +UVM_TESTNAME.
 */
module tb_top;
    import uvm_pkg::*;
    import ipv4_env_pkg::*;

    logic clk = 0;
    logic rst_n = 0;

    always #5 clk = ~clk;
    initial begin
        repeat (5) @(posedge clk);
        rst_n <= 1;
    end

    pkt_if in_if(clk);
    pkt_if out_if0(clk);
    pkt_if out_if1(clk);
    pkt_if out_if2(clk);
    pkt_if out_if3(clk);
    csr_if csr(clk, rst_n);

    logic [3:0] out_valid;
    logic [7:0] out_data;
    logic       out_sop, out_eop;

    ipv4_fwd u_dut(
        .clk(clk), .rst_n(rst_n),
        .in_valid(in_if.valid), .in_ready(in_if.ready), .in_data(in_if.data),
        .in_sop(in_if.sop), .in_eop(in_if.eop),
        .out_valid(out_valid),
        .out_ready({out_if3.ready, out_if2.ready, out_if1.ready, out_if0.ready}),
        .out_data(out_data), .out_sop(out_sop), .out_eop(out_eop),
        .csr_valid(csr.valid), .csr_write(csr.write), .csr_addr(csr.addr),
        .csr_wdata(csr.wdata), .csr_rdata(csr.rdata));

`define TB_OUT_PORT(p) \
    assign out_if``p.valid = out_valid[p]; \
    assign out_if``p.data = out_data; \
    assign out_if``p.sop = out_sop; \
    assign out_if``p.eop = out_eop; \
    assign out_if``p.ready = 1'b1;

    `TB_OUT_PORT(0)
    `TB_OUT_PORT(1)
    `TB_OUT_PORT(2)
    `TB_OUT_PORT(3)

    initial begin
        in_if.valid = 0;
        csr.valid = 0;
        uvm_config_db #(virtual pkt_if)::set(null, "*", "in_vif", in_if);
        uvm_config_db #(virtual pkt_if)::set(null, "*", "out_vif0", out_if0);
        uvm_config_db #(virtual pkt_if)::set(null, "*", "out_vif1", out_if1);
        uvm_config_db #(virtual pkt_if)::set(null, "*", "out_vif2", out_if2);
        uvm_config_db #(virtual pkt_if)::set(null, "*", "out_vif3", out_if3);
        uvm_config_db #(virtual csr_if)::set(null, "*", "csr_vif", csr);
        run_test();
    end
endmodule
