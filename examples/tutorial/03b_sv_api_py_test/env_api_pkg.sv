/**
 * The env's API for test writers: send packets, reprogram routes, wait,
 * read counters. gen-from-sv mirrors it so a Python test can call it.
 */
package env_api_pkg;
    import ipv4_pkt_pkg::*;

    interface class ipv4_env_api;
        // Drives one packet, after setting its length and checksum
        pure virtual task send(pkt_item p);

        // Programs route idx (an existing one, or the next new one).
        // Call between bursts, after wait_idle().
        pure virtual task set_route(int idx, int unsigned prefix, int len, int port);

        // Waits until every forwarded packet has come out
        pure virtual task wait_idle();

        pure virtual task get_fwd_count(output int unsigned count, input int port);

        pure virtual task get_drop_count(output int unsigned count, input pkt_fate_e reason);

        // The seed for the test's own randomization, from the SV seed
        pure virtual function int unsigned get_seed();
    endclass
endpackage
