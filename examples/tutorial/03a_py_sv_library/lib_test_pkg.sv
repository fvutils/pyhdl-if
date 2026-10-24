/**
 * The UVM team's code: sequences and a capture monitor built on ipv4_lib.
 * It is all SystemVerilog.
 */
package lib_test_pkg;
    import uvm_pkg::*;
    import ipv4_pkt_pkg::*;
    import ipv4_env_pkg::*;
    import ipv4_lib::*;
    `include "uvm_macros.svh"

    // Packets with options, built with ipv4_pkt
    class options_seq extends uvm_sequence #(pkt_item);
        `uvm_object_utils(options_seq)

        int n_pkts = 20;
        string dsts[$] = '{"10.9.0.1", "10.1.7.7", "10.1.2.200", "192.168.4.4"};
        string opts[$] = '{"nop", "rr", "router_alert"};
        string protos[$] = '{"icmp", "tcp", "udp"};

        function new(string name="options_seq");
            super.new(name);
        endfunction

        task body();
            repeat (n_pkts) begin
                ipv4_pkt p = new();
                ipv4_bytes_t payload;
                p.set_src("172.16.0.1");
                p.set_dst(dsts[$urandom_range(0, dsts.size()-1)]);
                p.set_ttl($urandom_range(2, 128));
                p.set_protocol(protos[$urandom_range(0, protos.size()-1)]);
                repeat ($urandom_range(0, 3))
                    p.add_option(opts[$urandom_range(0, opts.size()-1)]);
                repeat ($urandom_range(0, 32)) payload.push_back(8'($urandom));
                p.set_payload(payload);
                send(p);
                p.free();
            end
        endtask

        task send(ipv4_pkt p);
            req = pkt_item::type_id::create("req");
            start_item(req);
            req.unpack(p.pack());
            finish_item(req);
        endtask
    endclass

    // Malformed variants of good packets, from ipv4_mutator
    class error_seq extends options_seq;
        `uvm_object_utils(error_seq)

        function new(string name="error_seq");
            super.new(name);
        endfunction

        task body();
            ipv4_mutator m = new();
            m.seed($urandom);
            repeat (n_pkts) begin
                ipv4_pkt good = new(), bad;
                good.set_src("172.16.0.2");
                good.set_dst(dsts[$urandom_range(0, dsts.size()-1)]);
                good.add_option("rr");
                bad = m.mutate(good);
                `uvm_info(get_type_name(), $sformatf("%-12s %s", m.last_mutation(), bad.summary()), UVM_LOW)
                send(bad);
                good.free();
                bad.free();
            end
        endtask
    endclass

    // Logs each packet's summary and writes it to a capture
    class pcap_monitor extends uvm_subscriber #(pkt_item);
        `uvm_component_utils(pcap_monitor)

        string      path;
        pcap_writer pcap;

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void start_of_simulation_phase(uvm_phase phase);
            pcap = new();
            pcap.open(path);
        endfunction

        function void write(pkt_item t);
            ipv4_pkt p = ipv4_pkt::unpack(t.pack());
            `uvm_info(get_name(), (t.port >= 0) ? $sformatf("port %0d: %s", t.port, p.summary()) : p.summary(), UVM_LOW)
            pcap.write(t.pack());
            p.free();
        endfunction

        function void final_phase(uvm_phase phase);
            pcap.close();
        endfunction
    endclass

    class lib_test extends ipv4_base_test;
        `uvm_component_utils(lib_test)

        pcap_monitor in_cap, out_cap;

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            in_cap = pcap_monitor::type_id::create("in_cap", this);
            in_cap.path = "in.pcap";
            out_cap = pcap_monitor::type_id::create("out_cap", this);
            out_cap.path = "out.pcap";
        endfunction

        function void connect_phase(uvm_phase phase);
            env.in_agent.mon.ap.connect(in_cap.analysis_export);
            foreach (env.out_mon[i]) env.out_mon[i].ap.connect(out_cap.analysis_export);
        endfunction

        virtual task run_traffic();
            options_seq ok = options_seq::type_id::create("ok");
            error_seq bad = error_seq::type_id::create("bad");
            ok.start(env.in_agent.sqr);
            bad.start(env.in_agent.sqr);
        endtask
    endclass
endpackage
