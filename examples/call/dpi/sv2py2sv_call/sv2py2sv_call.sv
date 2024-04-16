package pkg;
    import pyhdl_dpi_if::*;
    import pyhdl_call_if::*;
    `include "MyC.svh"

    class MyCImpl extends MyC;
	    virtual function int getscale(int v);
            $display("getscale: %0d", v);
            return v+1;
        endfunction
    endclass

endpackage

module sv2py2sv_call;
    import pyhdl_dpi_if::*;
    import pyhdl_call_if::*;
    import pkg::*;

    initial begin
	automatic MyCImpl c = new();
	
	for (int i=0; i<256; i++) begin
		automatic int res = c.countones(i);
		$display("res: %0d %0d", i, res);
	end
    end
endmodule


