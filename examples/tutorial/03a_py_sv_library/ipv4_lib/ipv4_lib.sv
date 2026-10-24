/**
 * ipv4_lib: an IPv4 packet library for SystemVerilog.
 *
 *   ipv4_pkt      build packets (addresses, TTL, options, payload), pack()
 *                 them to bytes, unpack() bytes, and summary() for logs
 *   ipv4_mutator  protocol-aware malformed variants of a packet
 *   pcap_writer   capture packets for Wireshark
 *   pcap_reader   read a capture back
 *
 * Implemented in Python with scapy (ipv4_lib_impl.py); install
 * requirements.txt in the simulator's Python environment.
 */
package ipv4_lib;
    import uvm_pkg::*;
    `include "uvm_macros.svh"

    typedef byte unsigned ipv4_bytes_t[$];

    // The Python side of the library, created on first use
    class ipv4_lib_ctx;
        local static ipv4_lib_gen::Ipv4Lib m_lib;

        static function ipv4_lib_gen::Ipv4Lib get();
            if (m_lib == null) begin
                pyhdl_if::py_object o;
                pyhdl_if::pyhdl_if_start();
                pyhdl_if::py_gil_enter();
                o = pyhdl_if::py_import("ipv4_lib_impl");
                if (o != null) o = o.call_attr("Ipv4LibImpl");
                pyhdl_if::py_gil_leave();
                if (o == null) begin
                    `uvm_fatal("ipv4_lib", "failed to load the Python side (ipv4_lib_impl)")
                    return null;
                end
                m_lib = ipv4_lib_gen::Ipv4Lib_from_py(o.borrow());
            end
            return m_lib;
        endfunction
    endclass

    class ipv4_pkt extends uvm_object;
        `uvm_object_utils(ipv4_pkt)

        local ipv4_lib_gen::Ipv4Pkt m_h;

        function new(string name="ipv4_pkt");
            super.new(name);
        endfunction

        local function ipv4_lib_gen::Ipv4Pkt h();
            if (m_h == null) m_h = ipv4_lib_ctx::get().new_pkt();
            return m_h;
        endfunction

        static function ipv4_pkt unpack(ipv4_bytes_t data);
            ipv4_pkt p = new();
            p.m_h = ipv4_lib_ctx::get().unpack(data);
            return p;
        endfunction

        // Used by ipv4_mutator
        static function ipv4_pkt wrap(ipv4_lib_gen::Ipv4Pkt h);
            ipv4_pkt p = new();
            p.m_h = h;
            return p;
        endfunction

        function void set_src(string addr);     h().set_src(addr);      endfunction
        function void set_dst(string addr);     h().set_dst(addr);      endfunction
        function string get_dst();              return h().get_dst();   endfunction
        function void set_ttl(int ttl);         h().set_ttl(8'(ttl));   endfunction
        function int get_ttl();                 return h().get_ttl();   endfunction
        // icmp, tcp or udp
        function void set_protocol(string name); h().set_protocol(name); endfunction
        // nop, rr (record route) or router_alert
        function void add_option(string name);  h().add_option(name);   endfunction
        function void set_payload(ipv4_bytes_t data); h().set_payload(data); endfunction
        function void corrupt_checksum();       h().corrupt_checksum(); endfunction
        function bit checksum_ok();             return h().checksum_ok(); endfunction
        function ipv4_bytes_t pack();           return h().pack();      endfunction
        function string summary();              return h().summary();   endfunction

        virtual function string convert2string();
            return summary();
        endfunction

        // Frees the Python object now, rather than at the end of the run
        function void free();
            if (m_h != null) m_h.dispose();
            m_h = null;
        endfunction
    endclass

    class ipv4_mutator extends uvm_object;
        `uvm_object_utils(ipv4_mutator)

        local ipv4_lib_gen::Ipv4Mutator m_h;

        function new(string name="ipv4_mutator");
            super.new(name);
        endfunction

        function void seed(int unsigned s);
            if (m_h != null) m_h.dispose();
            m_h = ipv4_lib_ctx::get().new_mutator(s);
        endfunction

        // A malformed variant of p: bad checksum, expired TTL, bad IHL, or
        // fuzzed header fields
        function ipv4_pkt mutate(ipv4_pkt p);
            if (m_h == null) seed(0);
            return ipv4_pkt::wrap(m_h.mutate(p.pack()));
        endfunction

        function string last_mutation();
            return (m_h != null) ? m_h.last_mutation() : "";
        endfunction
    endclass

    class pcap_writer extends uvm_object;
        `uvm_object_utils(pcap_writer)

        local ipv4_lib_gen::PcapWriter m_h;

        function new(string name="pcap_writer");
            super.new(name);
        endfunction

        function void open(string path);
            m_h = ipv4_lib_ctx::get().pcap_writer(path);
        endfunction

        // Timestamped with the current simulation time
        function void write(ipv4_bytes_t data);
            if (m_h != null) m_h.write(data, 64'($realtime / 1ps));
        endfunction

        function void close();
            if (m_h != null) begin
                m_h.close();
                m_h.dispose();
                m_h = null;
            end
        endfunction
    endclass

    class pcap_reader extends uvm_object;
        `uvm_object_utils(pcap_reader)

        local ipv4_lib_gen::PcapReader m_h;

        function new(string name="pcap_reader");
            super.new(name);
        endfunction

        function void open(string path);
            m_h = ipv4_lib_ctx::get().pcap_reader(path);
        endfunction

        // 0 at the end of the file
        function bit read(output ipv4_bytes_t data);
            data = m_h.read();
            return data.size() != 0;
        endfunction

        function void close();
            if (m_h != null) begin
                m_h.close();
                m_h.dispose();
                m_h = null;
            end
        endfunction
    endclass
endpackage
