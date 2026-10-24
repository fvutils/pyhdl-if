/**
 * The base test: programs the routing table, runs traffic, then checks the
 * DUT's counters against the scoreboard. Examples override run_traffic().
 */
class ipv4_base_test extends uvm_test;
    `uvm_component_utils(ipv4_base_test)

    ipv4_fwd_cfg    cfg;
    ipv4_env        env;

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
        cfg = ipv4_fwd_cfg::type_id::create("cfg");
        cfg.add_route(32'h0A00_0000, 8, 0);    // 10.0.0.0/8     -> 0
        cfg.add_route(32'h0A01_0000, 16, 1);   // 10.1.0.0/16    -> 1
        cfg.add_route(32'h0A01_0200, 24, 2);   // 10.1.2.0/24    -> 2
        cfg.add_route(32'hC0A8_0000, 16, 3);   // 192.168.0.0/16 -> 3
        uvm_config_db #(ipv4_fwd_cfg)::set(this, "env", "cfg", cfg);
        env = ipv4_env::type_id::create("env", this);
    endfunction

    // The stimulus. The default is random traffic; +N_PKTS sets the count.
    virtual task run_traffic();
        pkt_rand_seq seq = pkt_rand_seq::type_id::create("seq");
        seq.cfg = cfg;
        void'($value$plusargs("N_PKTS=%d", seq.n_pkts));
        seq.start(env.in_agent.sqr);
    endtask

    task run_phase(uvm_phase phase);
        phase.raise_objection(this);
        env.csr.wait_reset();
        env.csr.program_routes(cfg);
        run_traffic();
        env.wait_idle();
        check_counters();
        phase.drop_objection(this);
    endtask

    virtual task check_counters();
        pkt_fate_e DROPS[4] = '{FATE_BAD_HDR, FATE_BAD_CKSUM, FATE_TTL, FATE_NO_ROUTE};
        int unsigned n;
        for (int p=0; p<N_PORTS; p++) begin
            env.csr.read_fwd_count(p, n);
            if (n != env.sb.n_fwd[p])
                `uvm_error(get_type_name(), $sformatf("port %0d forwarded: DUT %0d, expected %0d",
                    p, n, env.sb.n_fwd[p]))
        end
        foreach (DROPS[i]) begin
            env.csr.read_drop_count(DROPS[i], n);
            if (n != env.sb.count(DROPS[i]))
                `uvm_error(get_type_name(), $sformatf("%s dropped: DUT %0d, expected %0d",
                    DROPS[i].name(), n, env.sb.count(DROPS[i])))
        end
    endtask

    function void report_phase(uvm_phase phase);
        uvm_report_server rs = uvm_report_server::get_server();
        if (rs.get_severity_count(UVM_ERROR) + rs.get_severity_count(UVM_FATAL) == 0)
            `uvm_info(get_type_name(), "TEST PASSED", UVM_NONE)
        else
            `uvm_info(get_type_name(), "TEST FAILED", UVM_NONE)
    endfunction
endclass
