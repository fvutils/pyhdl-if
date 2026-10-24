/**
 * A directed SV sequence that replays the reference packets from Python.
 */
package ref_test_pkg;
    import uvm_pkg::*;
    import ipv4_pkt_pkg::*;
    import ipv4_env_pkg::*;
    `include "uvm_macros.svh"

    class ref_seq extends uvm_sequence #(pkt_item);
        `uvm_object_utils(ref_seq)

        ipv4_fwd_scoreboard sb;     // to check each packet's expected fate

        function new(string name="ref_seq");
            super.new(name);
        endfunction

        task body();
            ref_xchg_pkg::RefSource src;
            ref_xchg_pkg::RefPkt r;
            pyhdl_if::py_object obj;
            int n = 0;

            pyhdl_if::pyhdl_if_start();
            obj = pyhdl_if::py_import("ref_source");
            if (obj != null) obj = obj.call_attr("open_source");
            if (obj == null)
                `uvm_fatal(get_type_name(), "failed to open the reference packets")
            src = ref_xchg_pkg::RefSource_from_py(obj.borrow());

            while ((r = src.get_next()) != null) begin
                int port;
                bit [15:0] cksum;
                pkt_fate_e fate;

                req = pkt_item::type_id::create(r.name);
                start_item(req);
                req.version = 4;
                req.options = r.options;
                req.payload = r.payload;
                req.ihl = (r.ihl != 0) ? 4'(r.ihl) : 4'(5 + r.options.size() / 4);
                req.tos = 0;
                req.id = 16'(n);
                req.flags = r.dont_fragment ? 3'b010 : 3'b000;
                req.frag_off = 0;
                req.ttl = r.ttl;
                req.protocol = r.protocol;
                req.src = r.src;
                req.dst = r.dst;
                req.fix();
                if (r.corrupt_checksum)
                    req.checksum ^= 16'h0100;

                // The reference data says what should happen; so does the env
                fate = sb.predict(req, port, cksum);
                if (int'(fate) != int'(r.expected))
                    `uvm_error(get_type_name(), $sformatf("%s: expected %s, the scoreboard predicts %s",
                        r.name, r.expected.name(), fate.name()))
                else
                    `uvm_info(get_type_name(), $sformatf("%-16s %s -> %s", r.name,
                        req.convert2string(), fate.name()), UVM_LOW)
                finish_item(req);
                n++;
            end
            src.dispose();
            if (n == 0)
                `uvm_error(get_type_name(), "no reference packets")
        endtask
    endclass

    class ref_test extends ipv4_base_test;
        `uvm_component_utils(ref_test)

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        virtual task run_traffic();
            ref_seq seq = ref_seq::type_id::create("seq");
            seq.sb = env.sb;
            seq.start(env.in_agent.sqr);
        endtask
    endclass
endpackage
