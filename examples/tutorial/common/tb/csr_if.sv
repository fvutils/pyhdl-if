/**
 * Register port: a write takes effect on the clock where valid and write
 * are high. rdata follows addr combinationally.
 */
interface csr_if(input logic clk, input logic rst_n);
    logic        valid;
    logic        write;
    logic [7:0]  addr;
    logic [31:0] wdata;
    logic [31:0] rdata;
endinterface
