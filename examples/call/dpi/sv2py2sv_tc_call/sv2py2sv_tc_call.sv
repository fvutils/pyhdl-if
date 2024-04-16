package pkg;
    import pyhdl_if::*;
    `include "MyC.svh"

    class MyCImpl extends MyC;
	    virtual task read(output int retval, input int v);
            #1ns;
            $display("read: %0d", v);
            retval = v+1;
        endtask
    endclass

endpackage

module sv2py2sv_tc_call;
    import pyhdl_if::*;
    import pkg::*;

    initial begin
        automatic MyCImpl c = new();

        pyhdl_pi_if_start();

        c.body();
    end
endmodule


