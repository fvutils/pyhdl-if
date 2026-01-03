
module SimpleBFM_imp(
    input           clock,
    input           reset
);
    import flush_test_pkg::*;

    SimpleBFM_imp_if m_api_if(.*);

    class SimpleBFMImpl extends SimpleBFM_imp_impl #(SimpleBFMImpl);

        function new();
            super.new(this);
        endfunction

        virtual task do_operation(int unsigned value, output int unsigned result);
            $display("[SV %0t] do_operation called with value=%0d", $time, value);
            #10ns;
            result = value + 100;
            $display("[SV %0t] do_operation returning result=%0d", $time, result);
        endtask

    endclass

    SimpleBFMImpl m_bfm;

    initial begin
        m_bfm = new();
        m_api_if.register(m_bfm);
    end

endmodule
