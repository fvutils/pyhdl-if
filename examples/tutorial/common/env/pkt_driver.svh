/**
 * Drives each pkt_item onto the input port, one byte per accepted clock.
 */
class pkt_driver extends uvm_driver #(pkt_item);
    `uvm_component_utils(pkt_driver)

    virtual pkt_if vif;

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    task run_phase(uvm_phase phase);
        vif.valid <= 0;
        forever begin
            bytes_t b;
            seq_item_port.get_next_item(req);
            b = req.pack();
            foreach (b[i]) begin
                vif.valid <= 1;
                vif.data <= b[i];
                vif.sop <= (i == 0);
                vif.eop <= (i == b.size()-1);
                do @(posedge vif.clk); while (!vif.ready);
            end
            vif.valid <= 0;
            seq_item_port.item_done();
        end
    endtask
endclass
