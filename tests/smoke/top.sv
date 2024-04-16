
module top;
    import pyhdl_call_if::*;

    task automatic timed_task();
        $display("--> timed_task");
        repeat (20) begin
            $display("-- tick");
            #1ns;
        end
        $display("<-- timed_task");
    endtask
    export "DPI-C" task timed_task;
    import "DPI-C" context function longint unsigned svGetScope();

    longint unsigned scope = svGetScope();

    initial begin
        PyObject test_smoke;
        PyObject args;
        PyObject my_method;
        longint unsigned our_scope1, our_scope2;

        our_scope1 = svGetScope();

        pyhdl_start();

        our_scope2 = svGetCallerScope();
        $display("CallerScope: %08h %08h %08h", scope, our_scope1, our_scope2);

        test_smoke = PyImport_ImportModule("my_module");
        if (test_smoke == null) begin
            $display("Fatal: failed to load module");
            $finish;
        end else begin
            my_method = PyObject_GetAttrString(test_smoke, "my_method");
            void'(PyObject_Call(my_method, pyhdl_mkTuple('{
                PyLong_FromUnsignedLongLong(scope)
            }), null));
        end
        repeat (100) begin
            #1ns;
        end
        $finish;
    end

endmodule
