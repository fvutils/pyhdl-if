
package api_pkg;
    import pyhdl_dpi_if::*;
    import pyhdl_call_if::*;

    `include "api_gen_ext_1.svh"

endpackage

module api_gen_ext_1;
    import api_pkg::*;
    import pyhdl_dpi_if::*;

    initial begin
        automatic PyObject obj = pyhdl_pi_if_NewClass("api_gen_ext_1", "MyCExt", {});
        automatic MyC_wrap c = new();

        // Connect our SV and Python classes
        c.init(obj);

        $display("val: %0d", c.get_py_val(20));
        $finish;
    end

endmodule
