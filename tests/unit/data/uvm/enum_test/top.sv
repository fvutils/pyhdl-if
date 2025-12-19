/**
 * top.sv - Top module for enum registration test
 */

`include "uvm_macros.svh"

module tb_top;
    import uvm_pkg::*;
    import pyhdl_uvm::*;
    import pyhdl_if::*;
    import enum_test_pkg::*;

    initial begin
        pyhdl_if_time_cb time_cb;
        pyhdl_uvm_enum_rgy enum_rgy;
        pyhdl_uvm_object_rgy obj_rgy;
        PyObject enum_names, enum_values, enum_types;
        py_gil_state gstate;

        // Initialize pyhdl_if
        pyhdl_if_init(1'b1);
        time_cb = pyhdl_if_time_cb::inst();
        
        gstate = py_gil_enter();

        // Get enum registry instance
        enum_rgy = pyhdl_uvm_enum_rgy::inst();
        obj_rgy = pyhdl_uvm_object_rgy::inst();

        // Test 1: Get all registered enum types
        $display("Test 1: Get all registered enum types");
        enum_types = enum_rgy.get_enum_types();
        if (enum_types != None) begin
            $display("  PASS: Got enum types list");
        end else begin
            $display("  FAIL: enum_types is None");
        end

        // Test 2: Get enum names for color_e
        $display("Test 2: Get enum names for color_e");
        enum_names = enum_rgy.get_enum_names("color_e");
        if (enum_names != None) begin
            $display("  PASS: Got enum names for color_e");
        end else begin
            $display("  FAIL: enum_names is None");
        end

        // Test 3: Get enum values for color_e
        $display("Test 3: Get enum values for color_e");
        enum_values = enum_rgy.get_enum_values("color_e");
        if (enum_values != None) begin
            $display("  PASS: Got enum values for color_e");
        end else begin
            $display("  FAIL: enum_values is None");
        end

        // Test 4: Get enum names for state_e
        $display("Test 4: Get enum names for state_e");
        enum_names = enum_rgy.get_enum_names("state_e");
        if (enum_names != None) begin
            $display("  PASS: Got enum names for state_e");
        end else begin
            $display("  FAIL: enum_names is None");
        end

        // Test 5: Get enum values for state_e
        $display("Test 5: Get enum values for state_e");
        enum_values = enum_rgy.get_enum_values("state_e");
        if (enum_values != None) begin
            $display("  PASS: Got enum values for state_e");
        end else begin
            $display("  FAIL: enum_values is None");
        end

        py_gil_leave(gstate);

        $display("===========================================");
        $display("All enum registry tests completed!");
        $display("===========================================");

        #100;
        $finish;
    end

endmodule
