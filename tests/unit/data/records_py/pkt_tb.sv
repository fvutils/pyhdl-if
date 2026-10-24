// SV implementation of a Python-declared interface, receiving copies of a
// Python-declared record.
class sink_impl implements pkt_pkg::PktSink;
    int n;
    int errors;

    virtual task send(output bit [31:0] retval, input pkt_pkg::RefPkt p);
        #10;
        if (p.dst != 32'hC0A80001 || p.payload.size() != p.ttl - 1 ||
                p.opts.size() != 2 || p.opts[1] != 16'hFFFF ||
                p.proto != ((p.ttl % 2) ? pkt_pkg::UDP : pkt_pkg::TCP)) begin
            $display("[SV] FAIL: bad packet ttl=%0d", p.ttl);
            errors++;
        end
        retval = p.ttl - 1;
        n++;
    endtask

    virtual function bit [31:0] count();
        return n;
    endfunction

    virtual function void dispose();
    endfunction
endclass

module pkt_tb;
    initial begin
        sink_impl sink = new();
        pyhdl_if::PyObject m, args, res;
        pyhdl_if::PyGILState_STATE state;
        int fd, ok;

        pyhdl_if::pyhdl_if_start();
        state = pyhdl_if::PyGILState_Ensure();
        m = pyhdl_if::PyImport_ImportModule("pkt_drv");
        if (m == null) begin
            pyhdl_if::PyErr_Print();
            $finish;
        end
        args = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(args, 0, pkt_pkg::PktSink_to_py(sink)));
        pyhdl_if::PyGILState_Release(state);

        pyhdl_if::pyhdl_if_rt_callPyTask(res, m, "run", args);
        state = pyhdl_if::PyGILState_Ensure();
        ok = (res != null) ? int'(pyhdl_if::PyLong_AsLongLong(res)) : 0;
        pyhdl_if::PyGILState_Release(state);

        fd = $fopen("status.txt", "w");
        if (ok && sink.errors == 0 && sink.n == 10 && $time == 100) begin
            $fdisplay(fd, "PASS:");
        end else begin
            $fdisplay(fd, "FAIL: ok=%0d errors=%0d n=%0d time=%0t", ok, sink.errors, sink.n, $time);
        end
        $fclose(fd);
        $finish;
    end
endmodule
