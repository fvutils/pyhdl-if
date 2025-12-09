package pkg;
    import pyhdl_if::*;
    `include "MyC.svh"

endpackage

module sv2py_call;
    import pyhdl_if::*;
    import pkg::*;

    initial begin
        // Create an instance of the extended class, then wrap
        // it with the wrapper
	    automatic MyC_wrap c = new(MyC_wrap#()::create_pyobj(.clsname("MyCExt")));
	
	    for (int i=0; i<256; i++) begin
		    int res = c.countones(i);
		    $display("res: %0d %0d", i, res);
	    end
    end
endmodule


