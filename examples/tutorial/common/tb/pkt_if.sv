/**
 * Byte-stream packet port: one byte moves on each clock where valid and
 * ready are both high. sop/eop mark the first and last byte.
 */
interface pkt_if(input logic clk);
    logic       valid;
    logic       ready;
    logic [7:0] data;
    logic       sop;
    logic       eop;
endinterface
