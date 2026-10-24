/**
 * The environment: input agent, one monitor per output port, register
 * access and the scoreboard.
 */
class ipv4_env extends uvm_env;
    `uvm_component_utils(ipv4_env)

    ipv4_fwd_cfg            cfg;
    ipv4_fwd_csr            csr;
    pkt_agent               in_agent;
    pkt_monitor             out_mon[N_PORTS];
    ipv4_fwd_scoreboard     sb;

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
        if (!uvm_config_db #(ipv4_fwd_cfg)::get(this, "", "cfg", cfg))
            `uvm_fatal(get_type_name(), "no cfg")
        csr = ipv4_fwd_csr::type_id::create("csr");
        if (!uvm_config_db #(virtual csr_if)::get(this, "", "csr_vif", csr.vif))
            `uvm_fatal(get_type_name(), "no csr_vif")
        in_agent = pkt_agent::type_id::create("in_agent", this);
        for (int i=0; i<N_PORTS; i++) begin
            out_mon[i] = pkt_monitor::type_id::create($sformatf("out_mon%0d", i), this);
            out_mon[i].port = i;
            if (!uvm_config_db #(virtual pkt_if)::get(this, "", $sformatf("out_vif%0d", i), out_mon[i].vif))
                `uvm_fatal(get_type_name(), $sformatf("no out_vif%0d", i))
        end
        sb = ipv4_fwd_scoreboard::type_id::create("sb", this);
        sb.cfg = cfg;
    endfunction

    function void connect_phase(uvm_phase phase);
        in_agent.mon.ap.connect(sb.in_imp);
        foreach (out_mon[i]) out_mon[i].ap.connect(sb.out_imp);
    endfunction

    // Wait until every expected packet has come out (or give up)
    task wait_idle();
        int cycles = 0;
        while (sb.expected.size() != 0 && cycles < 10000) begin
            @(posedge csr.vif.clk);
            cycles++;
        end
        repeat (10) @(posedge csr.vif.clk);
    endtask
endclass
