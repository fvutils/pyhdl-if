/**
 * The input agent: sequencer, driver and monitor on the input port.
 */
class pkt_agent extends uvm_agent;
    `uvm_component_utils(pkt_agent)

    uvm_sequencer #(pkt_item)   sqr;
    pkt_driver                  drv;
    pkt_monitor                 mon;

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
        virtual pkt_if vif;
        if (!uvm_config_db #(virtual pkt_if)::get(this, "", "in_vif", vif))
            `uvm_fatal(get_type_name(), "no in_vif")
        sqr = uvm_sequencer #(pkt_item)::type_id::create("sqr", this);
        drv = pkt_driver::type_id::create("drv", this);
        mon = pkt_monitor::type_id::create("mon", this);
        drv.vif = vif;
        mon.vif = vif;
    endfunction

    function void connect_phase(uvm_phase phase);
        drv.seq_item_port.connect(sqr.seq_item_export);
    endfunction
endclass
