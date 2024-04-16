
module call_python();
    import pyhdl_if::*;

    initial begin
        automatic PyObject call_python_m = PyImport_ImportModule("call_python");
        automatic PyObject countones = PyObject_GetAttrString(call_python_m, "countones");

        begin
            for (int i=0; i<256; i++) begin
                PyObject res_o;
                int res;
                PyObject args = PyTuple_New(1);
                void'(PyTuple_SetItem(args, 0, PyLong_FromLong(i)));
                res_o = PyObject_Call(countones, args, null);
                res = PyLong_AsLong(res_o);
                if (res != $countones(i)) begin
                    $display("Error: ");
                end else begin
                    $display("Pass: %0d == %0d", res, $countones(i));
                end
            end
        end

        $finish;
    end
endmodule
