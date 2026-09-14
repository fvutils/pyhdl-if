
`ifndef INCLUDED_PYHDL_IF_MACROS_SVH
`define INCLUDED_PYHDL_IF_MACROS_SVH

/**
 * Prints a trace message when debug output is enabled.
 *
 * The argument is a parenthesised $display argument list -- note the doubled
 * parentheses, which is what lets one macro argument carry a whole format
 * string and its operands::
 *
 *     `PYHDL_IF_DEBUG(("value is %0d", val));
 *
 * Costs a comparison against pyhdl_if::pyhdl_if_debug when switched off, so
 * these can be left in place. Set that variable non-zero to see them.
 *
 * @param x The parenthesised argument list.
 */
`define PYHDL_IF_DEBUG(x) \
    if (pyhdl_if::pyhdl_if_debug > 0) begin \
        $write("PyHDL-IF: "); \
        $display x ; \
    end

/**
 * Traces entry to a function or task, prefixed `-->`.
 *
 * Pairs with #PYHDL_IF_LEAVE to bracket a call in the debug log.
 *
 * @param x A parenthesised `$display` argument list.
 */
`define PYHDL_IF_ENTER(x) \
    if (pyhdl_if::pyhdl_if_debug > 0) begin \
        $write("--> PyHDL-IF: "); \
        $display x ; \
    end

/**
 * Traces exit from a function or task, prefixed `<--`.
 *
 * @param x A parenthesised `$display` argument list.
 */
`define PYHDL_IF_LEAVE(x) \
    if (pyhdl_if::pyhdl_if_debug > 0) begin \
        $write("<-- PyHDL-IF: "); \
        $display x ; \
    end

/**
 * Reports an error. Always printed, whether or not debug is enabled.
 *
 * Does not stop the simulation -- use #PYHDL_IF_FATAL when continuing is not
 * meaningful.
 *
 * @param x A parenthesised `$display` argument list.
 */
`define PYHDL_IF_ERROR(x) \
    $write("PyHDL-IF Error: "); \
    $display x ;

/**
 * Reports an error and ends the simulation with `$finish`.
 *
 * @param x A parenthesised `$display` argument list.
 */
`define PYHDL_IF_FATAL(x) \
    $write("PyHDL-IF Fatal: "); \
    $display x ; \
    $finish ;

/**
 * Prints the SystemVerilog call stack.
 *
 * A macro rather than a direct `$stacktrace` so simulators lacking it can be
 * accommodated in one place.
 */
`define STACKTRACE $stacktrace


`endif /* INCLUDED_PYHDL_IF_MACROS_SVH */
