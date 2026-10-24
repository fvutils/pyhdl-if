// SV half of the records_types simulation test.

class sv_svc2 implements types_pkg::svc2;
    types_pkg::base_rec kept;

    function new();
        kept = new();
        kept.b = 77;
    endfunction

    virtual task t0();
        #1;
    endtask

    virtual function types_pkg::list_derived_rec_t f_list(types_pkg::list_derived_rec_t l);
        types_pkg::list_derived_rec_t ret;
        for (int i=l.size()-1; i>=0; i--) begin
            types_pkg::derived_rec c = types_pkg::derived_rec_copy(l[i]);
            c.b = c.b + 1;
            ret.push_back(c);
        end
        return ret;
    endfunction

    virtual function types_pkg::base_rec_if f_ref(types_pkg::derived_rec_if r);
        types_pkg::base_rec b = new();
        types_pkg::base_rec items[$] = r.get_items();
        b.b = 3;
        items.push_back(b);
        r.set_flag(!r.get_flag());
        r.set_items(items);
        r.dispose();
        return kept;
    endfunction

    virtual function types_pkg::svc2 f_if(types_pkg::svc2 i);
        return i;
    endfunction

    virtual function pyhdl_if::pyhdl_if_bytes_t f_bytes(pyhdl_if::pyhdl_if_bytes_t b);
        pyhdl_if::pyhdl_if_bytes_t ret;
        foreach (b[i]) ret.push_front(b[i]);
        return ret;
    endfunction

    virtual function string f_str(string s);
        return {s, "!"};
    endfunction

    virtual function real f_real(real x, shortreal y);
        return x + y;
    endfunction

    virtual function bit f_bool(bit b);
        return !b;
    endfunction

    virtual function types_pkg::big_e f_enum(types_pkg::sev_e e);
        return (e == types_pkg::SEV_HIGH) ? types_pkg::BIG_TOP : types_pkg::BIG_ZERO;
    endfunction

    virtual function bit [99:0] f_wide(bit signed [79:0] w);
        return w;
    endfunction

    virtual function int f_names(int state, int args, int method, int ret, int m_impl, int m_obj);
        return state + args + method + ret + m_impl + m_obj;
    endfunction

    virtual task t_names(output types_pkg::empty_rec retval, input int state, input int args);
        #1;
        retval = new();
    endtask

    virtual function void f_empty(types_pkg::empty_rec e, types_pkg::empty_if x);
    endfunction

    virtual function void dispose();
    endfunction
endclass

module types_tb;
    import types_pkg::*;

    int errors = 0;
    pyhdl_if::PyObject m_test;
    string UNI = "h\303\251llo \342\234\223 \"q\" \\ \t";

    `define CHECK(cond, msg) \
        if (!(cond)) begin \
            $display("[SV] FAIL: %0s", msg); \
            errors++; \
        end

    function automatic pyhdl_if::PyObject call_py(string name, pyhdl_if::PyObject args=null);
        pyhdl_if::PyObject ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        if (args == null) args = pyhdl_if::PyTuple_New(0);
        ret = pyhdl_if::pyhdl_if_rt_callPyFunc(m_test, name, args);
        pyhdl_if::PyGILState_Release(state);
        return ret;
    endfunction

    function automatic pyhdl_if::PyObject args1(pyhdl_if::PyObject a0);
        pyhdl_if::PyObject ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        ret = pyhdl_if::PyTuple_New(1);
        void'(pyhdl_if::PyTuple_SetItem(ret, 0, a0));
        pyhdl_if::PyGILState_Release(state);
        return ret;
    endfunction

    function automatic pyhdl_if::PyObject args2(pyhdl_if::PyObject a0, pyhdl_if::PyObject a1);
        pyhdl_if::PyObject ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        ret = pyhdl_if::PyTuple_New(2);
        void'(pyhdl_if::PyTuple_SetItem(ret, 0, a0));
        void'(pyhdl_if::PyTuple_SetItem(ret, 1, a1));
        pyhdl_if::PyGILState_Release(state);
        return ret;
    endfunction

    function automatic pyhdl_if::PyObject py_bool(bit v);
        pyhdl_if::PyObject ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        ret = pyhdl_if::PyBool_FromLong(64'(v));
        pyhdl_if::PyGILState_Release(state);
        return ret;
    endfunction

    function automatic longint py_int(pyhdl_if::PyObject o);
        longint ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        ret = pyhdl_if::PyLong_AsLongLong(o);
        pyhdl_if::Py_DecRef(o);
        pyhdl_if::PyGILState_Release(state);
        return ret;
    endfunction

    function automatic void py_decref(pyhdl_if::PyObject o);
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::Py_DecRef(o);
        pyhdl_if::PyGILState_Release(state);
    endfunction

    function automatic base_rec mk_base(int b);
        base_rec r = new();
        r.b = b;
        return r;
    endfunction

    // Matches expected_derived() in types_drv.py
    function automatic derived_rec mk_derived();
        derived_rec d = new();
        d.a = 1;
        d.b = -2048;
        d.c = 64'hFFFF_FFFF_FFFF_FFFF;
        d.d = 64'h8000_0000_0000_0000;
        d.e = 1.5;
        d.s = -128;
        d.t = 16'hFFFF;
        d.items.push_back(mk_base(5));
        d.items.push_back(mk_base(-1));
        d.grid = '{'{8'd1, 8'd2, 8'd3}, '{}, '{8'd255}};
        d.strs = '{"", UNI};
        d.w = {1'b1, 79'b0};
        d.sev = SEV_LOW;
        d.big = BIG_TOP;
        d.blobs = '{'{}, '{8'h00, 8'hFF}};
        d.flag = 1;
        d.x = -0.125;
        return d;
    endfunction

    task automatic test_copy();
        derived_rec d = mk_derived(), r;
        pyhdl_if::PyObject o, ro;
        $display("[SV] test_copy");
        o = derived_rec_to_py(d);
        ro = call_py("check_derived", args1(o));
        r = derived_rec_from_py(ro);
        py_decref(ro);
        `CHECK(r != null, "null result")
        `CHECK(r.b == 2047 && r.w == 80'h7FFF_FFFF_FFFF_FFFF_FFFF, $sformatf("b/w %0d %0h", r.b, r.w))
        `CHECK(r.c == 64'hFFFF_FFFF_FFFF_FFFF && r.d == 64'h8000_0000_0000_0000, "c/d")
        `CHECK(r.a == 1 && r.s == -128 && r.t == 16'hFFFF && r.e == 1.5 && r.x == -0.125, "scalars")
        `CHECK(r.items.size() == 3 && r.items[2].c == 7 && r.items[1].b == -1, "items")
        `CHECK(r.grid.size() == 3 && r.grid[1].size() == 1 && r.grid[1][0] == 9 && r.grid[2][0] == 255, "grid")
        `CHECK(r.strs.size() == 1 && r.strs[0] == {UNI, "!"}, {"strs ", r.strs[0]})
        `CHECK(r.sev == SEV_HIGH && r.big == BIG_ZERO, "enums")
        `CHECK(r.blobs.size() == 1 && r.blobs[0].size() == 256 && r.blobs[0][255] == 255, "blobs")
        `CHECK(r.flag == 1, "flag")
        // Deep copy in SV
        begin
            derived_rec c = derived_rec_copy(d);
            c.items[0].b = 99;
            c.grid[0][0] = 99;
            `CHECK(d.items[0].b == 5 && d.grid[0][0] == 1, "derived_rec_copy is not deep")
        end
    endtask

    task automatic test_sv_impl();
        sv_svc2 svc = new();
        pyhdl_if::PyObject o, res;
        int py_errs;
        $display("[SV] test_sv_impl");
        o = svc2_to_py(svc);
        pyhdl_if::pyhdl_if_rt_callPyTask(res, m_test, "run_svc2", args2(o, py_bool(1)));
        py_errs = int'(py_int(res));
        `CHECK(py_errs == 0, $sformatf("run_svc2(SV): %0d Python errors", py_errs))
    endtask

    task automatic test_py_impl();
        svc2 svc;
        pyhdl_if::PyObject o;
        list_derived_rec_t l, lo;
        derived_rec d = mk_derived();
        base_rec_if k;
        pyhdl_if::pyhdl_if_bytes_t b, bo;
        empty_rec e;
        $display("[SV] test_py_impl");
        o = call_py("make_py_svc2");
        svc = svc2_from_py(o);
        py_decref(o);

        svc.t0();
        l.push_back(mk_derived());
        l.push_back(mk_base_derived(10));
        lo = svc.f_list(l);
        `CHECK(lo.size() == 2 && lo[0].b == 11 && lo[1].b == -2047, "f_list")
        `CHECK(lo[1].strs[1] == UNI && lo[1].w == {1'b1, 79'b0}, "f_list deep")
        l.delete();
        lo = svc.f_list(l);
        `CHECK(lo.size() == 0, "f_list empty")

        // A local object passed by reference: Python modifies it
        k = svc.f_ref(d);
        `CHECK(d.flag == 0 && d.items.size() == 3 && d.items[2].b == 3, "f_ref by reference")
        `CHECK(k != null && k.get_b() == 77, "f_ref returned ref")
        k.dispose();

        begin
            svc2 back = svc.f_if(svc);
            `CHECK(back != null && back.f_str("") == "!", "f_if round trip")
        end

        b.delete();
        bo = svc.f_bytes(b);
        `CHECK(bo.size() == 0, "f_bytes empty")
        for (int i=0; i<4096; i++) b.push_back(i);
        bo = svc.f_bytes(b);
        `CHECK(bo.size() == 4096 && bo[0] == 8'hFF && bo[4095] == 0, "f_bytes 4096")
        `CHECK(svc.f_str(UNI) == {UNI, "!"}, "f_str")
        `CHECK(svc.f_real(1.25, 0.5) == 1.75, "f_real")
        `CHECK(svc.f_bool(1) == 0 && svc.f_bool(0) == 1, "f_bool")
        `CHECK(svc.f_enum(SEV_HIGH) == BIG_TOP && svc.f_enum(SEV_LOW) == BIG_ZERO, "f_enum")
        `CHECK(svc.f_wide(-1) == {100{1'b1}} && svc.f_wide(5) == 5, "f_wide")
        `CHECK(svc.f_names(1, 2, 3, 4, 5, 6) == 21, "f_names")
        svc.t_names(e, 1, 2);
        `CHECK(e != null, "t_names")
        begin
            empty_rec er = new();
            svc.f_empty(er, null);
        end
        svc.dispose();
    endtask

    function automatic derived_rec mk_base_derived(int b);
        derived_rec d = new();
        d.b = b;
        return d;
    endfunction

    initial begin
        pyhdl_if::PyGILState_STATE state;
        int fd, py_errs;

        pyhdl_if::pyhdl_if_start();
        pyhdl_if::pyhdl_if_rt_error_fatal = 0;

        state = pyhdl_if::PyGILState_Ensure();
        m_test = pyhdl_if::PyImport_ImportModule("types_drv");
        if (m_test == null) begin
            pyhdl_if::PyErr_Print();
            $display("FAIL: cannot import types_drv");
            $finish;
        end
        pyhdl_if::PyGILState_Release(state);

        test_copy();
        test_sv_impl();
        test_py_impl();

        py_errs = int'(py_int(call_py("errors")));
        $display("[SV] errors=%0d py_errors=%0d rt_errors=%0d", errors, py_errs, pyhdl_if::pyhdl_if_rt_errors);
        fd = $fopen("status.txt", "w");
        if (errors == 0 && py_errs == 0 && pyhdl_if::pyhdl_if_rt_errors == 0) begin
            $fdisplay(fd, "PASS:");
        end else begin
            $fdisplay(fd, "FAIL: errors=%0d py_errors=%0d rt_errors=%0d",
                errors, py_errs, pyhdl_if::pyhdl_if_rt_errors);
        end
        $fclose(fd);
        $finish;
    end

endmodule
