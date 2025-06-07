
`ifndef INCLUDED_PYHDL_IF_MACROS_SVH
`define INCLUDED_PYHDL_IF_MACROS_SVH

`define PYHDL_IF_DEBUG(x) \
    if (pyhdl_if::pyhdl_if_debug > 0) begin \
        $write("PyHDL-IF: "); \
        $display x ; \
    end

`define PYHDL_IF_ENTER(x) \
    if (pyhdl_if::pyhdl_if_debug > 0) begin \
        $write("--> PyHDL-IF: "); \
        $display x ; \
    end

`define PYHDL_IF_LEAVE(x) \
    if (pyhdl_if::pyhdl_if_debug > 0) begin \
        $write("<-- PyHDL-IF: "); \
        $display x ; \
    end


`endif /* INCLUDED_PYHDL_IF_MACROS_SVH */
