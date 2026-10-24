/**
 * Collects the bytes of each packet on a port and publishes a pkt_item.
 * port is -1 for the input port, else the output port number.
 */
class pkt_monitor extends uvm_monitor;
    `uvm_component_utils(pkt_monitor)

    virtual pkt_if                  vif;
    int                             port = -1;
    uvm_analysis_port #(pkt_item)   ap;

    function new(string name, uvm_component parent);
        super.new(name, parent);
        ap = new("ap", this);
    endfunction

    task run_phase(uvm_phase phase);
        bytes_t b;
        forever begin
            @(posedge vif.clk);
            if (vif.valid === 1 && vif.ready === 1) begin
                if (vif.sop) b.delete();
                b.push_back(vif.data);
                if (vif.eop) begin
                    pkt_item p = pkt_item::type_id::create("p");
                    p.unpack(b);
                    p.port = port;
                    ap.write(p);
                end
            end
        end
    endtask
endclass
