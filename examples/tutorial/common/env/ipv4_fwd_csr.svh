/**
 * Register access to the forwarder: routes and counters.
 */
class ipv4_fwd_csr extends uvm_object;
    `uvm_object_utils(ipv4_fwd_csr)

    localparam bit [7:0] ADDR_ID = 8'h00;
    localparam bit [7:0] ADDR_ROUTE = 8'h10;
    localparam bit [7:0] ADDR_FWD = 8'h30;
    localparam bit [7:0] ADDR_DROP = 8'h38;
    localparam bit [7:0] ADDR_CLEAR = 8'h3F;

    virtual csr_if vif;

    function new(string name="ipv4_fwd_csr");
        super.new(name);
    endfunction

    task wait_reset();
        while (vif.rst_n !== 1) @(posedge vif.clk);
        @(posedge vif.clk);
    endtask

    task write(bit [7:0] addr, bit [31:0] data);
        vif.valid <= 1;
        vif.write <= 1;
        vif.addr <= addr;
        vif.wdata <= data;
        @(posedge vif.clk);
        vif.valid <= 0;
        vif.write <= 0;
    endtask

    task read(bit [7:0] addr, output bit [31:0] data);
        vif.addr <= addr;
        @(posedge vif.clk);
        data = vif.rdata;
    endtask

    task set_route(int idx, bit [31:0] prefix, int len, int port, bit valid=1);
        write(ADDR_ROUTE + 8'(2*idx), prefix);
        write(ADDR_ROUTE + 8'(2*idx+1), {valid, 17'b0, 6'(len), 6'b0, 2'(port)});
    endtask

    task program_routes(ipv4_fwd_cfg cfg);
        foreach (cfg.rt_prefix[i])
            set_route(i, cfg.rt_prefix[i], cfg.rt_len[i], cfg.rt_port[i]);
    endtask

    task read_fwd_count(int port, output int unsigned count);
        bit [31:0] d;
        read(ADDR_FWD + 8'(port), d);
        count = d;
    endtask

    // reason: FATE_BAD_HDR .. FATE_NO_ROUTE
    task read_drop_count(pkt_fate_e reason, output int unsigned count);
        bit [31:0] d;
        read(ADDR_DROP + 8'(int'(reason) - 1), d);
        count = d;
    endtask

    task clear_counters();
        write(ADDR_CLEAR, 1);
    endtask
endclass
