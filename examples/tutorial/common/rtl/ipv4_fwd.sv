/**
 * ipv4_fwd: a minimal store-and-forward IPv4 forwarder.
 *
 * - Input: one byte stream (valid/ready, sop/eop) carrying raw IPv4 packets.
 * - Checks the header checksum over IHL*4 bytes; drops on a bad checksum,
 *   TTL <= 1, or a malformed header (version != 4, IHL < 5, or IHL*4 longer
 *   than the packet).
 * - Decrements TTL and updates the checksum (RFC 1624); options and payload
 *   pass through unchanged.
 * - Routes by longest-prefix match on the destination address to one of
 *   N_PORTS output streams. No matching route: drop.
 * - Counters: forwarded per port, dropped per reason.
 *
 * CSRs (word addresses):
 *   0x00       ID (RO)
 *   0x10+2*i   route i prefix
 *   0x11+2*i   route i control: [31] valid, [13:8] prefix length, [1:0] port
 *   0x30+p     forwarded count, port p (RO)
 *   0x38..0x3B dropped count: bad header, bad checksum, TTL, no route (RO)
 *   0x3F       write 1: clear all counters
 */
module ipv4_fwd #(
    parameter int N_PORTS   = 4,
    parameter int N_ROUTES  = 8,
    parameter int BUF_BYTES = 2048
) (
    input  logic                clk,
    input  logic                rst_n,

    input  logic                in_valid,
    output logic                in_ready,
    input  logic [7:0]          in_data,
    input  logic                in_sop,
    input  logic                in_eop,

    // One packet leaves at a time: data/sop/eop are shared, valid is per port
    output logic [N_PORTS-1:0]  out_valid,
    input  logic [N_PORTS-1:0]  out_ready,
    output logic [7:0]          out_data,
    output logic                out_sop,
    output logic                out_eop,

    input  logic                csr_valid,
    input  logic                csr_write,
    input  logic [7:0]          csr_addr,
    input  logic [31:0]         csr_wdata,
    output logic [31:0]         csr_rdata
);
    localparam int IDX_W = $clog2(BUF_BYTES+1);
    localparam logic [31:0] ID = 32'h1F40_0001;

    typedef enum logic [1:0] { RX, DECIDE, TX } state_e;
    typedef enum logic [1:0] { DROP_HDR, DROP_CKSUM, DROP_TTL, DROP_ROUTE } drop_e;

    state_e             state;
    logic [7:0]         buffer[BUF_BYTES];
    logic [IDX_W-1:0]   idx;        // RX: bytes received; TX: next byte to send
    logic [IDX_W-1:0]   len;

    // Header fields, captured as the bytes arrive
    logic [3:0]         version, ihl;
    logic [7:0]         ttl, proto;
    logic [15:0]        hdr_cksum;
    logic [31:0]        dst;
    logic [19:0]        sum;        // one's-complement sum of the header

    // Routing table
    logic [31:0]        rt_prefix[N_ROUTES];
    logic [5:0]         rt_len[N_ROUTES];
    logic [1:0]         rt_port[N_ROUTES];
    logic               rt_valid[N_ROUTES];

    logic [31:0]        fwd_cnt[N_PORTS];
    logic [31:0]        drop_cnt[4];

    logic [1:0]         port;
    logic [7:0]         new_ttl;
    logic [15:0]        new_cksum;

    // Longest-prefix match
    logic               lpm_hit;
    logic [1:0]         lpm_port;
    always_comb begin
        int best;
        logic [31:0] mask;
        lpm_hit = 0;
        lpm_port = 0;
        best = -1;
        for (int i=0; i<N_ROUTES; i++) begin
            mask = (rt_len[i] == 0) ? 32'h0 : ~((32'h1 << (32 - rt_len[i])) - 1);
            if (rt_valid[i] && ((dst ^ rt_prefix[i]) & mask) == 0 && int'(rt_len[i]) > best) begin
                best = int'(rt_len[i]);
                lpm_hit = 1;
                lpm_port = rt_port[i];
            end
        end
    end

    function automatic logic [15:0] fold(logic [19:0] s);
        logic [19:0] t = {4'b0, s[15:0]} + {16'b0, s[19:16]};
        return t[15:0] + {12'b0, t[19:16]};
    endfunction

    // RFC 1624 eqn 3: HC' = ~(~HC + ~m + m'), m = {TTL, protocol}
    function automatic logic [15:0] update_cksum(
        logic [15:0] hc, logic [15:0] m, logic [15:0] m_new);
        logic [19:0] s = {4'b0, ~hc} + {4'b0, ~m} + {4'b0, m_new};
        return ~fold(s);
    endfunction

    assign in_ready = (state == RX);

    wire [IDX_W-1:0] hdr_len = {ihl, 2'b00};

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= RX;
            idx <= 0;
            len <= 0;
            sum <= 0;
            for (int i=0; i<N_ROUTES; i++) begin
                rt_valid[i] <= 0;
                rt_prefix[i] <= 0;
                rt_len[i] <= 0;
                rt_port[i] <= 0;
            end
            for (int i=0; i<N_PORTS; i++) fwd_cnt[i] <= 0;
            for (int i=0; i<4; i++) drop_cnt[i] <= 0;
        end else begin
            case (state)
            RX: if (in_valid) begin : rx
                logic [IDX_W-1:0] i;
                logic [3:0] cur_ihl;
                i = in_sop ? 0 : idx;
                cur_ihl = (i == 0) ? in_data[3:0] : ihl;
                if (i < BUF_BYTES) buffer[i] <= in_data;
                if (i == 0) begin
                    version <= in_data[7:4];
                    ihl <= in_data[3:0];
                end
                case (i)
                    8:  ttl <= in_data;
                    9:  proto <= in_data;
                    10: hdr_cksum[15:8] <= in_data;
                    11: hdr_cksum[7:0] <= in_data;
                    16: dst[31:24] <= in_data;
                    17: dst[23:16] <= in_data;
                    18: dst[15:8] <= in_data;
                    19: dst[7:0] <= in_data;
                    default: ;
                endcase
                // Sum 16-bit words over the header (IHL is known after byte 0)
                if (i == 0)
                    sum <= {4'b0, in_data, 8'b0};
                else if (i < {cur_ihl, 2'b00})
                    sum <= sum + (i[0] ? {12'b0, in_data} : {4'b0, in_data, 8'b0});
                idx <= i + 1;
                if (in_eop) begin
                    len <= i + 1;
                    state <= DECIDE;
                end
            end
            DECIDE: begin
                if (version != 4 || ihl < 5 || hdr_len > len) begin
                    drop_cnt[DROP_HDR] <= drop_cnt[DROP_HDR] + 1;
                    state <= RX;
                end else if (fold(sum) != 16'hFFFF) begin
                    drop_cnt[DROP_CKSUM] <= drop_cnt[DROP_CKSUM] + 1;
                    state <= RX;
                end else if (ttl <= 1) begin
                    drop_cnt[DROP_TTL] <= drop_cnt[DROP_TTL] + 1;
                    state <= RX;
                end else if (!lpm_hit) begin
                    drop_cnt[DROP_ROUTE] <= drop_cnt[DROP_ROUTE] + 1;
                    state <= RX;
                end else begin
                    port <= lpm_port;
                    new_ttl <= ttl - 1;
                    new_cksum <= update_cksum(hdr_cksum, {ttl, proto}, {ttl - 8'd1, proto});
                    idx <= 0;
                    state <= TX;
                end
            end
            TX: if (out_ready[port]) begin
                if (idx + 1 == len) begin
                    fwd_cnt[port] <= fwd_cnt[port] + 1;
                    idx <= 0;
                    state <= RX;
                end else begin
                    idx <= idx + 1;
                end
            end
            default: state <= RX;
            endcase

            if (csr_valid && csr_write) begin
                if (csr_addr >= 8'h10 && csr_addr < 8'h10 + 2*N_ROUTES) begin
                    automatic int r = (int'(csr_addr) - 'h10) / 2;
                    if (csr_addr[0] == 0) begin
                        rt_prefix[r] <= csr_wdata;
                    end else begin
                        rt_valid[r] <= csr_wdata[31];
                        rt_len[r] <= (csr_wdata[13:8] > 32) ? 6'd32 : csr_wdata[13:8];
                        rt_port[r] <= csr_wdata[1:0];
                    end
                end else if (csr_addr == 8'h3F && csr_wdata[0]) begin
                    for (int i=0; i<N_PORTS; i++) fwd_cnt[i] <= 0;
                    for (int i=0; i<4; i++) drop_cnt[i] <= 0;
                end
            end
        end
    end

    // Output: the buffered packet with TTL and checksum replaced
    always_comb begin
        out_valid = '0;
        out_data = buffer[idx[$clog2(BUF_BYTES)-1:0]];
        case (idx)
            8:  out_data = new_ttl;
            10: out_data = new_cksum[15:8];
            11: out_data = new_cksum[7:0];
            default: ;
        endcase
        out_sop = (idx == 0);
        out_eop = (idx + 1 == len);
        if (state == TX) out_valid[port] = 1'b1;
    end

    always_comb begin
        csr_rdata = '0;
        if (csr_addr == 8'h00)
            csr_rdata = ID;
        else if (csr_addr >= 8'h10 && csr_addr < 8'h10 + 2*N_ROUTES) begin
            automatic int r = (int'(csr_addr) - 'h10) / 2;
            csr_rdata = csr_addr[0] ? {rt_valid[r], 17'b0, rt_len[r], 6'b0, rt_port[r]}
                                    : rt_prefix[r];
        end else if (csr_addr >= 8'h30 && csr_addr < 8'h30 + N_PORTS)
            csr_rdata = fwd_cnt[csr_addr - 8'h30];
        else if (csr_addr >= 8'h38 && csr_addr < 8'h3C)
            csr_rdata = drop_cnt[csr_addr - 8'h38];
    end

endmodule
