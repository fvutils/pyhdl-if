
module simple_bfm 
    import pyhdl_if::*;
    import flush_test_pkg::*;
    (
        input clock,
        input reset
    );

    SimpleBFM_imp_if m_api_if(.*);

endmodule
