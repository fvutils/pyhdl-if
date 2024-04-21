package pkg;
    import pyhdl_if::*;
    `include "MyC.svh"

    class MyCImpl extends MyC;
	    virtual task read(
            output int unsigned retval, 
            input int unsigned addr);
            #1ns;
            $display("read: %0d", v);
            retval = v+1;
        endtask

	    virtual task write(
            input int unsigned addr,
            input int unsigned data);
            #1ns;
            $display("write: %0d %0d",addr, data);
        endtask
    endclass

    class SeqImpl extends MyC;

	    virtual task read(
            output int unsigned retval, 
            input int unsigned addr);
            // ...
        endtask

	    virtual task write(
            input int unsigned addr,
            input int unsigned data);
            // ...
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


