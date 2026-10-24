module uvm_rec_tb;
  import uvm_pkg::*;
  import pkt_item_pkg::*;

  function automatic pyhdl_if::PyObject call_py(pyhdl_if::PyObject m, string name, pyhdl_if::PyObject arg);
    pyhdl_if::PyObject args, ret;
    pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
    args = pyhdl_if::PyTuple_New((arg == null) ? 0 : 1);
    if (arg != null) void'(pyhdl_if::PyTuple_SetItem(args, 0, arg));
    ret = pyhdl_if::pyhdl_if_rt_callPyFunc(m, name, args);
    pyhdl_if::PyGILState_Release(state);
    return ret;
  endfunction

  initial begin
    pkt_item it;
    pkt_sink_if sink;
    pyhdl_if::PyObject m, o;
    pyhdl_if::PyGILState_STATE state;
    int fd, errs;

    pyhdl_if::pyhdl_if_start();
    state = pyhdl_if::PyGILState_Ensure();
    m = pyhdl_if::PyImport_ImportModule("uvm_rec_drv");
    if (m == null) begin
      pyhdl_if::PyErr_Print();
      $finish;
    end
    pyhdl_if::PyGILState_Release(state);

    it = pkt_item::type_id::create("it");
    it.src = 32'h0A000001;
    it.dst = 32'hC0A80001;
    it.ttl = 7;
    it.payload = '{8'h01, 8'h02, 8'h83};
    it.kind = K_CTRL;
    it.udata = new[1];
    it.udata[0] = 8'hFE;
    foreach (it.mac[i]) it.mac[i] = i;
    it.nums = '{5, -6};
    for (int i=1; i<=2; i++) begin
      automatic opt_c o = new();
      o.code = i;
      it.opts.push_back(o);
    end

    // A copy, through the SV interface class implemented in Python
    o = call_py(m, "make_mon", null);
    sink = pkt_gen_pkg::pkt_sink_if_from_py(o);
    sink.write(it);

    // A reference to the same object
    void'(call_py(m, "cover_ref", pkt_gen_pkg::pkt_item_ref_to_py(pkt_gen_pkg::pkt_item_wrap(it))));

    state = pyhdl_if::PyGILState_Ensure();
    errs = int'(pyhdl_if::PyLong_AsLongLong(call_py(m, "check", null)));
    pyhdl_if::PyGILState_Release(state);

    // The UVM DPI layer is live: real regular expressions, and UVM's
    // command-line processor sees plusargs
    begin
      string v;
      uvm_cmdline_processor clp = uvm_cmdline_processor::get_inst();
      if (uvm_re_match("^ab+c$", "abbbc") != 0) begin
        $display("[SV] FAIL: uvm_re_match did not match a regex");
        errs++;
      end
      if (!clp.get_arg_value("+REC_ARG=", v) || v != "42") begin
        $display("[SV] FAIL: uvm_cmdline_processor did not see +REC_ARG (got '%0s')", v);
        errs++;
      end
    end

    fd = $fopen("status.txt", "w");
    if (errs == 0 && it.ttl == 99 && it.payload.size() == 4 && it.payload[3] == -1
        && it.udata.size() == 2 && it.udata[1] == 8'h20 && it.mac[0] == 8'hAA && it.mac[5] == 8'hFF
        && it.nums.size() == 2 && it.nums[0] == -1 && it.opts.size() == 1 && it.opts[0].code == 9)
      $fdisplay(fd, "PASS:");
    else
      $fdisplay(fd, "FAIL: errs=%0d ttl=%0d size=%0d udata=%p mac=%p nums=%p opts=%0d",
        errs, it.ttl, it.payload.size(), it.udata, it.mac, it.nums, it.opts.size());
    $fclose(fd);
    $finish;
  end
endmodule
