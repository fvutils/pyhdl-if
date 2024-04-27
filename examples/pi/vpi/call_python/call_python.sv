
module call_python();

    initial begin
        static reg[63:0] call_python_m;
        static reg[63:0] countones;
        static int i;
        
        call_python_m = $PyImport_ImportModule("call_python");
        $display("call_python_m: %08h", call_python_m);
        countones = $PyObject_GetAttrString(call_python_m, "countones");
        $display("countones: %08h", countones);

        begin : vars
            static reg[63:0] res_o;
            static int res;
            static reg[63:0] args, lval;

	    $display("countones: %08h", countones);

            for (i=0; i<1; i=i+1) begin
                args = $PyTuple_New(1);
		$display("args: %08h", args);
        lval = $PyLong_FromLong(i);
                $display("SetItem: %08h %08h", args, lval);
                res = $PyTuple_SetItem(args, 0, 2);
		$display("res: %0d", res);
                res_o = $PyObject_Call(countones, args, 0);
		$display("res_o: %08h", res_o);
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
