
module async_call;
    import pyhdl_call_if::*;
    import pyhdl_dpi_if::*;

    class MyC extends PyHdlCallApiBase implements PyHdlCallApiIF;

        function new();
            PyObject async_call_m = PyImport_ImportModule("async_call");
            PyObject MyC_t = PyObject_GetAttrString(async_call_m, "MyC");
            m_obj = pyhdl_call_if_new(MyC_t, this, PyTuple_New(0));

            // Register ourselves such that we can be invoked
        endfunction

        function int inbound();
            PyObject inbound_f = PyObject_GetAttrString(m_obj, "inbound");
            PyObject args = PyTuple_New(0);
            PyObject res = PyObject_Call(inbound_f, args, null);
            return PyLong_AsLong(res);
        endfunction

        function int outbound();
            $display("outbound");
            return 5;
        endfunction

        task inbound_t();
            PyObject res;
            PyObject args = PyTuple_New(0);
            pyhdl_call_if_invokePyTask(
                res,
                m_obj,
                "inbound_t",
                args);
        endtask

        task outbound_t();
            $display("--> outbound_t %0t", $time);
            #10ns;
            $display("<-- outbound_t %0t", $time);
        endtask

        virtual function PyObject invokeFunc(
            string      method,
            PyObject    args);
            PyObject ret = None;
            $display("invokeFunc");
            case (method)
            "outbound": begin
                int __ret;
                $display("outbound");
                __ret = outbound(); 
                ret = PyLong_FromLong(__ret);
            end
            default:
                $display("Fail: unknown method %0s", method);
            endcase
            return ret;
        endfunction

        virtual task invokeTask(
            string      method,
            PyObject    args);
            $display("invokeTask: %0s", method);
            case (method)
                "outbound_t": begin
                    outbound_t();
                end
            endcase
        endtask

    endclass

    initial begin
        automatic MyC ci = new();
        automatic int val;

        pyhdl_call_if_start();

        val = ci.inbound();
        $display("val: %0d", val);
        $display("--> ci.inbound_t %0t", $time);
        ci.inbound_t();
        $display("<-- ci.inbound_t %0t", $time);
    end

endmodule
