/**
 * Random traffic: most packets go to a routed address; a few are
 * malformed, carry a bad checksum, have TTL <= 1, or have no route.
 */
class pkt_rand_seq extends uvm_sequence #(pkt_item);
    `uvm_object_utils(pkt_rand_seq)

    ipv4_fwd_cfg    cfg;
    int             n_pkts = 40;

    function new(string name="pkt_rand_seq");
        super.new(name);
    endfunction

    task body();
        repeat (n_pkts) begin
            int r;
            req = pkt_item::type_id::create("req");
            start_item(req);
            if (!req.randomize())
                `uvm_fatal(get_type_name(), "randomize failed")
            r = $urandom_range(0, 99);
            if (r < 85)
                req.dst = cfg.addr_in_route($urandom_range(0, cfg.rt_prefix.size()-1));
            if (r >= 70 && r < 76) begin
                req.ttl = 8'($urandom_range(0, 1));
                req.fix();
            end else if (r >= 76 && r < 80) begin
                req.ihl = 4'($urandom_range(0, 4));
                req.options.delete();
                req.fix();
            end else begin
                req.fix();
            end
            if (r >= 80 && r < 85)
                req.checksum ^= 16'h0100;
            finish_item(req);
        end
    endtask
endclass
