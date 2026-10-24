/**
 * The base test plus a subscriber on the input monitor that samples every
 * packet in the Python coverage model.
 */
package cov_test_pkg;
    import uvm_pkg::*;
    import ipv4_pkt_pkg::*;
    import ipv4_env_pkg::*;
    import cov_if_pkg::*;
    `include "uvm_macros.svh"

    class pkt_cov_subscriber extends uvm_subscriber #(pkt_item);
        `uvm_component_utils(pkt_cov_subscriber)

        pkt_cov_if cov;

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            pyhdl_if::py_object model;
            pyhdl_if::pyhdl_if_start();
            pyhdl_if::py_gil_enter();
            model = pyhdl_if::py_import("ipv4_cov").call_attr("Ipv4Coverage");
            pyhdl_if::py_gil_leave();
            if (model == null)
                `uvm_fatal(get_type_name(), "failed to create ipv4_cov.Ipv4Coverage")
            // The Python object, as an SV pkt_cov_if handle
            cov = cov_gen_pkg::pkt_cov_if_from_py(model.borrow());
        endfunction

        // Each packet goes to Python as a copy
        function void write(pkt_item t);
            cov.sample(t);
        endfunction

        function void report_phase(uvm_phase phase);
            `uvm_info(get_type_name(), $sformatf("IPv4 coverage: %0.1f%%", cov.report()), UVM_LOW)
        endfunction
    endclass

    class cov_test extends ipv4_base_test;
        `uvm_component_utils(cov_test)

        pkt_cov_subscriber cov_sub;

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        function void build_phase(uvm_phase phase);
            super.build_phase(phase);
            cov_sub = pkt_cov_subscriber::type_id::create("cov_sub", this);
        endfunction

        function void connect_phase(uvm_phase phase);
            env.in_agent.mon.ap.connect(cov_sub.analysis_export);
        endfunction
    endclass
endpackage
