/**
 * The scoreboard with its reference model in Python (ipv4_model.py).
 */
package numpy_sb_pkg;
    import uvm_pkg::*;
    import pyhdl_if::*;
    import ipv4_pkt_pkg::*;
    import ipv4_env_pkg::*;
    `include "uvm_macros.svh"

    class numpy_scoreboard extends ipv4_fwd_scoreboard;
        `uvm_component_utils(numpy_scoreboard)

        py_object model;    // the ipv4_model module

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        // Python ints in a list
        static function py_object py_from_bytes(bytes_t b);
            py_list l = new();
            foreach (b[i]) l.append(py_from_int(b[i]));
            return l;
        endfunction

        function void start_of_simulation_phase(uvm_phase phase);
            py_list routes;
            pyhdl_if_start();
            py_gil_enter();
            model = py_import("ipv4_model");
            if (model == null)
                `uvm_fatal(get_type_name(), "failed to import ipv4_model")
            routes = new();
            foreach (cfg.rt_prefix[i])
                routes.append(py_tuple::mk_init('{
                    py_from_ulong(cfg.rt_prefix[i]), py_from_int(cfg.rt_len[i]), py_from_int(cfg.rt_port[i])}));
            void'(model.call_attr("set_routes", py_tuple::mk_init('{routes})));
            py_gil_leave();
        endfunction

        virtual function pkt_fate_e predict(pkt_item p, output int port, output bit [15:0] new_cksum);
            py_object ret;
            py_tuple r;
            pkt_fate_e fate = FATE_BAD_HDR;
            py_gil_enter();
            ret = model.call_attr("predict", py_tuple::mk_init('{
                py_from_bytes(p.header()), py_from_int(p.pack().size())}));
            if (ret == null) begin
                // The traceback is already printed
                `uvm_error(get_type_name(), "ipv4_model.predict raised an exception")
                port = -1;
                new_cksum = 0;
            end else begin
                r = py_tuple::mk(ret);
                fate = pkt_fate_e'(r.get_item(0).as_int());
                port = r.get_item(1).as_int();
                new_cksum = 16'(r.get_item(2).as_int());
            end
            py_gil_leave();
            return fate;
        endfunction
    endclass

    class numpy_test extends ipv4_base_test;
        `uvm_component_utils(numpy_test)

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            set_type_override_by_type(ipv4_fwd_scoreboard::get_type(), numpy_scoreboard::get_type());
            super.build_phase(phase);
        endfunction
    endclass
endpackage
