
module call_python();

    initial begin
        static reg[63:0] call_python_m = $PyImport_ImportModule("call_python");
        static reg[63:0] countones = $PyObject_GetAttrString(call_python_m, "countones");
        static int i;

        begin : vars
            static reg[63:0] res_o;
            static int res;
            static reg[63:0] args;

            for (i=0; i<1; i=i+1) begin
                args = $PyTuple_New(1);
                res = $PyTuple_SetItem(args, 0, $PyLong_FromLong(i));
                res_o = $PyObject_Call(countones, args, 0);
                res = $PyLong_AsLong(res_o);
                if (res != $countones(i)) begin
                    $display("Error: res=%0d countones=%0d", res, $countones(i));
                end else begin
                    $display("Pass: %0d == %0d", res, $countones(i));
                end
            end
        end

        $finish;
    end
endmodule
