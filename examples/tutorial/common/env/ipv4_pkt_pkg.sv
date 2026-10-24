/**
 * The packet transaction: an IPv4 header, its options and the payload.
 * Section 2a mirrors this class into Python with gen-from-sv.
 */
package ipv4_pkt_pkg;
    import uvm_pkg::*;
    `include "uvm_macros.svh"

    typedef byte unsigned bytes_t[$];

    // What the forwarder does with a packet
    typedef enum { FATE_FWD, FATE_BAD_HDR, FATE_BAD_CKSUM, FATE_TTL, FATE_NO_ROUTE } pkt_fate_e;

    class pkt_item extends uvm_sequence_item;
        `uvm_object_utils(pkt_item)

        rand bit [3:0]      version;
        rand bit [3:0]      ihl;
        rand bit [7:0]      tos;
        bit [15:0]          total_len;
        rand bit [15:0]     id;
        rand bit [2:0]      flags;
        rand bit [12:0]     frag_off;
        rand bit [7:0]      ttl;
        rand bit [7:0]      protocol;
        bit [15:0]          checksum;
        rand bit [31:0]     src;
        rand bit [31:0]     dst;
        byte unsigned       options[$];
        byte unsigned       payload[$];
        int                 port = -1;   // output port it was seen on; -1 on input

        constraint c_valid {
            version == 4;
            ihl inside {[5:15]};
            ttl >= 2;
            frag_off == 0;
            flags inside {0, 2};          // DF or nothing
            protocol inside {1, 6, 17};   // ICMP, TCP, UDP
        }

        function new(string name="pkt_item");
            super.new(name);
        endfunction

        // Options: NOPs ending in EOL, filling IHL; a random payload
        function void post_randomize();
            int n_opt = (ihl > 5) ? (int'(ihl) - 5) * 4 : 0;
            options.delete();
            for (int i=0; i<n_opt; i++)
                options.push_back((i == n_opt-1) ? 8'h00 : 8'h01);
            payload.delete();
            repeat ($urandom_range(0, 64)) payload.push_back(8'($urandom));
            fix();
        endfunction

        // Set total_len and checksum from the current contents
        function void fix();
            total_len = 16'(20 + options.size() + payload.size());
            checksum = calc_checksum();
        endfunction

        function bytes_t header();
            bytes_t h;
            h.push_back({version, ihl});
            h.push_back(tos);
            h.push_back(total_len[15:8]);
            h.push_back(total_len[7:0]);
            h.push_back(id[15:8]);
            h.push_back(id[7:0]);
            h.push_back({flags, frag_off[12:8]});
            h.push_back(frag_off[7:0]);
            h.push_back(ttl);
            h.push_back(protocol);
            h.push_back(checksum[15:8]);
            h.push_back(checksum[7:0]);
            for (int i=3; i>=0; i--) h.push_back(src[8*i +: 8]);
            for (int i=3; i>=0; i--) h.push_back(dst[8*i +: 8]);
            foreach (options[i]) h.push_back(options[i]);
            return h;
        endfunction

        // Internet checksum over the header, with the checksum field as zero
        function bit [15:0] calc_checksum();
            bytes_t h = header();
            bit [31:0] sum = 0;
            h[10] = 0;
            h[11] = 0;
            for (int i=0; i<h.size(); i+=2)
                sum += {h[i], (i+1 < h.size()) ? h[i+1] : 8'h00};
            while (sum[31:16] != 0)
                sum = sum[15:0] + sum[31:16];
            return ~sum[15:0];
        endfunction

        function bytes_t pack();
            bytes_t b = header();
            foreach (payload[i]) b.push_back(payload[i]);
            return b;
        endfunction

        function void unpack(bytes_t b);
            int hlen;
            version = b[0][7:4];
            ihl = b[0][3:0];
            tos = b[1];
            total_len = {b[2], b[3]};
            id = {b[4], b[5]};
            flags = b[6][7:5];
            frag_off = {b[6][4:0], b[7]};
            ttl = b[8];
            protocol = b[9];
            checksum = {b[10], b[11]};
            src = {b[12], b[13], b[14], b[15]};
            dst = {b[16], b[17], b[18], b[19]};
            hlen = (ihl > 5) ? int'(ihl) * 4 : 20;
            options.delete();
            payload.delete();
            for (int i=20; i<hlen && i<b.size(); i++) options.push_back(b[i]);
            for (int i=hlen; i<b.size(); i++) payload.push_back(b[i]);
        endfunction

        static function string ip2str(bit [31:0] a);
            return $sformatf("%0d.%0d.%0d.%0d", a[31:24], a[23:16], a[15:8], a[7:0]);
        endfunction

        virtual function string convert2string();
            return $sformatf("%s > %s ttl=%0d ihl=%0d len=%0d chksum=%04h%s",
                ip2str(src), ip2str(dst), ttl, ihl, total_len, checksum,
                (port >= 0) ? $sformatf(" port=%0d", port) : "");
        endfunction

        virtual function void do_copy(uvm_object rhs);
            pkt_item p;
            super.do_copy(rhs);
            $cast(p, rhs);
            unpack(p.pack());
            port = p.port;
        endfunction

        virtual function bit do_compare(uvm_object rhs, uvm_comparer comparer);
            pkt_item p;
            $cast(p, rhs);
            return pack() == p.pack();
        endfunction
    endclass

endpackage
