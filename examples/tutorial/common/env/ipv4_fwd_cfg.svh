/**
 * The routing table the test programs into the DUT, which the scoreboard
 * also uses to predict where each packet goes.
 */
class ipv4_fwd_cfg extends uvm_object;
    `uvm_object_utils(ipv4_fwd_cfg)

    bit [31:0]  rt_prefix[$];
    int         rt_len[$];
    int         rt_port[$];

    function new(string name="ipv4_fwd_cfg");
        super.new(name);
    endfunction

    function void add_route(bit [31:0] prefix, int len, int port);
        rt_prefix.push_back(prefix);
        rt_len.push_back(len);
        rt_port.push_back(port);
    endfunction

    static function bit [31:0] mask(int len);
        return (len == 0) ? 32'h0 : ~((32'h1 << (32 - len)) - 1);
    endfunction

    // Longest-prefix match: the output port, or -1 when no route matches
    function int lookup(bit [31:0] dst);
        int best = -1, port = -1;
        foreach (rt_prefix[i]) begin
            if (((dst ^ rt_prefix[i]) & mask(rt_len[i])) == 0 && rt_len[i] > best) begin
                best = rt_len[i];
                port = rt_port[i];
            end
        end
        return port;
    endfunction

    // A random address inside route i
    function bit [31:0] addr_in_route(int i);
        return (rt_prefix[i] & mask(rt_len[i])) | ($urandom & ~mask(rt_len[i]));
    endfunction
endclass
