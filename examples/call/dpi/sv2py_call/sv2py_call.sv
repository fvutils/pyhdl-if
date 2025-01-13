package pkg;
    import pyhdl_if::*;
    `include "MyC.svh"

endpackage

module sv2py_call;
    import pyhdl_if::*;
    import pkg::*;

    initial begin
	automatic MyC c = new();
	
	for (int i=0; i<256; i++) begin
		automatic int res = c.countones(i);
		$display("res: %0d %0d", i, res);
	end
    end
endmodule


