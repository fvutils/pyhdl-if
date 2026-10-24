/**
 * What the UVM env needs from a coverage model. gen-from-sv mirrors this
 * interface class, so a Python object can implement it.
 */
package cov_if_pkg;
    import ipv4_pkt_pkg::*;

    interface class pkt_cov_if;
        pure virtual function void sample(pkt_item p);
        // Prints the report; returns the coverage (%)
        pure virtual function real report();
    endclass
endpackage
