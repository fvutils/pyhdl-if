/**
 * The base UVM environment for the IPv4 forwarder: packet agent, output
 * monitors, register access, an SV-only scoreboard and the base test.
 */
package ipv4_env_pkg;
    import uvm_pkg::*;
    import ipv4_pkt_pkg::*;
    `include "uvm_macros.svh"

    localparam int N_PORTS = 4;

    `include "ipv4_fwd_cfg.svh"
    `include "ipv4_fwd_csr.svh"
    `include "pkt_driver.svh"
    `include "pkt_monitor.svh"
    `include "pkt_agent.svh"
    `include "ipv4_fwd_scoreboard.svh"
    `include "ipv4_env.svh"
    `include "pkt_rand_seq.svh"
    `include "ipv4_base_test.svh"
endpackage
