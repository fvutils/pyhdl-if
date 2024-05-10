
interface WishboneInitiatorBFM;
    `include "hdl_call_if_api.svh"

    class WishboneInitiatorImpl extends WishboneInitiator;
        virtual task write(int unsigned addr, int unsigned data);
            $display("write");
        endtask
        
        virtual task read(output int unsigned retval, input int unsigned addr);
            $display("read");
            retval = 0;
        endtask

    endclass

    WishboneInitiatorImpl       m_api_obj;

    initial begin : init
        m_api_obj = new();
        $display("Path: %m");
        pyhdl_if::pyhdl_if_registerObject(m_api_obj.m_obj, $sformatf("%m"), 1);
    end
endinterface

module call_sv_bfm;
    import pyhdl_if::*;

    reg clk = 0;
    initial begin
        pyhdl_pi_if_start();

        clk = 0;
        forever begin
            #10ns;
            clk = ~clk;
        end
    end

    WishboneInitiatorBFM    init_bfm();

endmodule

