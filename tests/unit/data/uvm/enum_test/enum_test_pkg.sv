/**
 * enum_test_pkg.sv - Test package for enum registration
 */

`include "uvm_macros.svh"

package enum_test_pkg;
    import uvm_pkg::*;
    import pyhdl_uvm::*;
    import pyhdl_if::*;

    // Define test enum types
    typedef enum bit [1:0] {
        RED   = 0,
        GREEN = 1,
        BLUE  = 2,
        YELLOW = 3
    } color_e;

    typedef enum bit [2:0] {
        IDLE   = 0,
        ACTIVE = 1,
        BUSY   = 2,
        DONE   = 3,
        ERROR  = 4
    } state_e;

    typedef enum bit [1:0] {
        ADD = 0,
        SUB = 1,
        MUL = 2,
        DIV = 3
    } operation_e;

    // Register the enums
    `pyhdl_uvm_enum_utils(color_e)
    `pyhdl_uvm_enum_utils(state_e)
    `pyhdl_uvm_enum_utils(operation_e)

    // Define a test sequence item with enum fields
    class test_item extends uvm_sequence_item;
        rand color_e      color;
        rand state_e      state;
        rand operation_e  op;
        rand int unsigned data;

        `uvm_object_utils_begin(test_item)
            `uvm_field_enum(color_e, color, UVM_ALL_ON)
            `uvm_field_enum(state_e, state, UVM_ALL_ON)
            `uvm_field_enum(operation_e, op, UVM_ALL_ON)
            `uvm_field_int(data, UVM_ALL_ON)
        `uvm_object_utils_end

        function new(string name = "test_item");
            super.new(name);
        endfunction
    endclass

endpackage
