`uvm_analysis_imp_decl(_in)
`uvm_analysis_imp_decl(_out)

/**
 * Predicts what the forwarder does with each input packet and checks the
 * output ports against it. predict() is the reference model; section 1
 * replaces it with one in Python.
 */
class ipv4_fwd_scoreboard extends uvm_scoreboard;
    `uvm_component_utils(ipv4_fwd_scoreboard)

    uvm_analysis_imp_in #(pkt_item, ipv4_fwd_scoreboard)   in_imp;
    uvm_analysis_imp_out #(pkt_item, ipv4_fwd_scoreboard)  out_imp;

    ipv4_fwd_cfg        cfg;
    pkt_item            expected[$];
    int unsigned        n_fate[pkt_fate_e];
    int unsigned        n_fwd[N_PORTS];
    int unsigned        n_checked;

    function new(string name, uvm_component parent);
        super.new(name, parent);
        in_imp = new("in_imp", this);
        out_imp = new("out_imp", this);
    endfunction

    // The reference model: the packet's fate, and for a forwarded packet,
    // its output port and the header checksum after the TTL decrement.
    virtual function pkt_fate_e predict(pkt_item p, output int port, output bit [15:0] new_cksum);
        pkt_item fwd;
        port = -1;
        new_cksum = 0;
        if (p.version != 4 || p.ihl < 5 || int'(p.ihl) * 4 > p.pack().size())
            return FATE_BAD_HDR;
        if (p.calc_checksum() != p.checksum)
            return FATE_BAD_CKSUM;
        if (p.ttl <= 1)
            return FATE_TTL;
        port = cfg.lookup(p.dst);
        if (port < 0)
            return FATE_NO_ROUTE;
        $cast(fwd, p.clone());
        fwd.ttl = p.ttl - 1;
        new_cksum = fwd.calc_checksum();
        return FATE_FWD;
    endfunction

    function void write_in(pkt_item p);
        int port;
        bit [15:0] new_cksum;
        pkt_fate_e fate = predict(p, port, new_cksum);
        n_fate[fate]++;
        if (fate == FATE_FWD) begin
            pkt_item exp;
            $cast(exp, p.clone());
            exp.ttl = p.ttl - 1;
            exp.checksum = new_cksum;
            exp.port = port;
            n_fwd[port]++;
            expected.push_back(exp);
        end
        `uvm_info(get_type_name(), $sformatf("%s -> %s", p.convert2string(), fate.name()), UVM_HIGH)
    endfunction

    function void write_out(pkt_item p);
        pkt_item exp;
        if (expected.size() == 0) begin
            `uvm_error(get_type_name(), $sformatf("unexpected output: %s", p.convert2string()))
            return;
        end
        exp = expected.pop_front();
        if (p.port != exp.port || !p.compare(exp))
            `uvm_error(get_type_name(), $sformatf("mismatch:\n  expected %s\n  actual   %s",
                exp.convert2string(), p.convert2string()))
        n_checked++;
    endfunction

    function int unsigned count(pkt_fate_e fate);
        return n_fate.exists(fate) ? n_fate[fate] : 0;
    endfunction

    function void check_phase(uvm_phase phase);
        if (expected.size() != 0)
            `uvm_error(get_type_name(), $sformatf("%0d expected packets never came out", expected.size()))
    endfunction

    function void report_phase(uvm_phase phase);
        `uvm_info(get_type_name(), $sformatf(
            "checked %0d forwarded; dropped: hdr=%0d cksum=%0d ttl=%0d route=%0d",
            n_checked, count(FATE_BAD_HDR), count(FATE_BAD_CKSUM),
            count(FATE_TTL), count(FATE_NO_ROUTE)), UVM_LOW)
    endfunction
endclass
