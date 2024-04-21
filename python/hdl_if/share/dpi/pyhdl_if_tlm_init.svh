
function automatic bit __pyhdl_if_tlm_init();
        PyObject args, stream_rgy_t, inst_m;
        PyObject hdl_if_tlm, hdl_if_impl_tlm;

        hdl_if_tlm = pyhdl_pi_if_HandleErr(PyImport_ImportModule("hdl_if.tlm"));
        hdl_if_impl_tlm = pyhdl_pi_if_HandleErr(PyImport_ImportModule("hdl_if.impl.tlm"));
        
        if (hdl_if_tlm == null) begin
            $display("Fatal Error: Failed to load hdl_if.tlm package");
            $finish;
            return 0;
        end

        stream_req_t = pyhdl_pi_if_HandleErr(PyObject_GetAttrString(hdl_if_impl_tlm, "StreamReq"));
        if (stream_req_t == null) begin
            $display("Fatal Error: Failed to find StreamReq class in hdl_if.impl.tlm");
            $finish;
            return 0;
        end
        stream_rsp_t = pyhdl_pi_if_HandleErr(PyObject_GetAttrString(hdl_if_impl_tlm, "StreamRsp"));
        if (stream_rsp_t == null) begin
            $display("Fatal Error: Failed to find StreamRsp class in hdl_if.impl.impl");
            $finish;
            return 0;
        end

        stream_rgy_t = pyhdl_pi_if_HandleErr(PyObject_GetAttrString(hdl_if_tlm, "StreamRgy"));
        inst_m = pyhdl_pi_if_HandleErr(PyObject_GetAttrString(stream_rgy_t, "inst"));

        args = PyTuple_New(0);
        stream_rgy = pyhdl_pi_if_HandleErr(PyObject_Call(inst_m, args, null));

        register_stream = pyhdl_pi_if_HandleErr(PyObject_GetAttrString(stream_rgy, "register_stream"));

        return 1;
endfunction
