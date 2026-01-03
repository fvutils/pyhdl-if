
module SVHelperImpl(
    input           clock
);
    import flush_test_pkg::*;

    class SVHelperClass extends SVHelper_imp_impl #(SVHelperClass);

        function new();
            super.new(this);
        endfunction

        virtual function void display_msg(int unsigned i);
            $display("[SV %0t] Message from Python iteration %0d", $time, i);
        endfunction

    endclass

    SVHelperClass m_helper;

    initial begin
        m_helper = new();
        pyhdl_if::pyhdl_if_registerObject(m_helper.m_obj, $sformatf("%m"), 1);
    end

endmodule
