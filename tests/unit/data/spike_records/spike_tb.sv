// SV half of the records/interfaces spike test.

class sv_cb implements spike_pkg::cb_if;
    int got[$];
    virtual function void notify(int v);
        got.push_back(v);
    endfunction
    virtual function void dispose();
    endfunction
endclass

// SV implementation of pkt_svc
class sv_svc implements spike_pkg::pkt_svc;
    spike_pkg::pkt  kept[$];
    spike_pkg::cb_if cb;

    virtual function int add(int a, int b);
        return a + b;
    endfunction

    virtual function spike_pkg::pkt bump(spike_pkg::pkt p);
        spike_pkg::pkt ret = spike_pkg::pkt_copy(p);
        ret.ttl--;
        ret.name = {p.name, "-bumped"};
        return ret;
    endfunction

    // Works on any pkt_if: a local pkt or a Python object
    virtual function void touch(spike_pkg::pkt_if p);
        int opts[$] = p.get_opts();
        p.set_ttl(p.get_ttl() - 1);
        opts.push_back(99);
        p.set_opts(opts);
        p.dispose();
    endfunction

    virtual function spike_pkg::pkt_if make_ref(bit [7:0] ttl);
        spike_pkg::pkt p = new();
        p.ttl = ttl;
        if (kept.size() == 0) kept.push_back(p);
        return p;
    endfunction

    virtual task xfer(output spike_pkg::pkt retval, input spike_pkg::pkt p);
        #10;
        retval = spike_pkg::pkt_copy(p);
        retval.id++;
    endtask

    virtual task touch_t(input spike_pkg::pkt_if p);
        #5;
        p.set_ttl(p.get_ttl() + 10);
        p.dispose();
    endtask

    virtual function void subscribe(spike_pkg::cb_if cb);
        this.cb = cb;
    endfunction

    virtual function void fire(int v);
        cb.notify(v);
    endfunction

    virtual function void dispose();
    endfunction
endclass

module spike_tb;
    import spike_pkg::*;

    int errors = 0;
    pyhdl_if::PyObject m_test;

    `define CHECK(cond, msg) \
        if (!(cond)) begin \
            $display("[SV] FAIL: %0s", msg); \
            errors++; \
        end

    // Calls spike_drv.<name>(*args). Steals args; returns new ref.
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

    function automatic longint py_int(pyhdl_if::PyObject o);
        longint ret;
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        ret = pyhdl_if::PyLong_AsLongLong(o);
        pyhdl_if::Py_DecRef(o);
        pyhdl_if::PyGILState_Release(state);
        return ret;
    endfunction

    // Returns o with one more reference, for passing to something that
    // steals it while keeping our own.
    function automatic pyhdl_if::PyObject py_incref(pyhdl_if::PyObject o);
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::Py_IncRef(o);
        pyhdl_if::PyGILState_Release(state);
        return o;
    endfunction

    function automatic void py_decref(pyhdl_if::PyObject o);
        pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
        pyhdl_if::Py_DecRef(o);
        pyhdl_if::PyGILState_Release(state);
    endfunction

    function automatic pkt mk_pkt();
        pkt p = new();
        p.ttl = 200;
        p.id = -5;
        p.valid = 1;
        p.weight = 2.5;
        p.name = "hello, \"world\"!";
        p.payload = '{8'h00, 8'h01, 8'h7f, 8'h80, 8'hff};
        p.kind = PROTO_UDP;
        p.h.src = 32'hC0A80001;
        p.h.dst = 32'hFFFFFFFF;
        p.h.proto = PROTO_TCP;
        p.opts = '{1, -1, 32'h7fffffff, 32'h80000000};
        p.tag = (96'hA5 << 88) | 96'h1234;
        return p;
    endfunction

    // The same code works on a local pkt and on a reference to a Python pkt
    function automatic int sum_ttl(pkt_if p);
        hdr_if h = p.get_h();
        int ret = p.get_ttl() + h.get_src();
        h.dispose();
        return ret;
    endfunction

    task automatic test_copy();
        pkt p = mk_pkt(), q;
        pyhdl_if::PyObject o, r;
        $display("[SV] test_copy");
        o = pkt_to_py(p);
        r = call_py("check_copy", args1(o));
        q = pkt_from_py(r);
        py_decref(r);
        `CHECK(q != null, "pkt_from_py returned null")
        `CHECK(q.ttl == 199, $sformatf("q.ttl %0d", q.ttl))
        `CHECK(q.id == -5, $sformatf("q.id %0d", q.id))
        `CHECK(q.valid == 1 && q.weight == 2.5, "q.valid/weight")
        `CHECK(q.name == "hello, \"world\"!", {"q.name ", q.name})
        `CHECK(q.payload.size() == 6 && q.payload[5] == 8'h42 && q.payload[3] == 8'h80, "q.payload")
        `CHECK(q.kind == PROTO_UDP, "q.kind")
        `CHECK(q.h.src == 1 && q.h.dst == 32'hFFFFFFFF && q.h.proto == PROTO_TCP, "q.h")
        `CHECK(q.opts.size() == 5 && q.opts[3] == 32'h80000000 && q.opts[4] == 7, "q.opts")
        `CHECK(q.tag == ((96'hA5 << 88) | 96'h1234), $sformatf("q.tag %0h", q.tag))
        // Copy out does not alias the original
        `CHECK(p.ttl == 200 && p.h.src == 32'hC0A80001, "original changed")
        // Null records cross as None
        o = pkt_to_py(null);
        q = pkt_from_py(o);
        `CHECK(q == null, "null round trip")
        py_decref(o);
    endtask

    task automatic test_sv_ref();
        pkt p = mk_pkt();
        pyhdl_if::PyObject r;
        $display("[SV] test_sv_ref");
        r = pkt_ref_to_py(p);
        py_decref(call_py("mod_ref", args1(r)));
        `CHECK(p.ttl == 64 && p.id == -100 && p.valid == 0, $sformatf("ref ttl/id/valid %0d %0d", p.ttl, p.id))
        `CHECK(p.weight == -0.25 && p.name == "ref-set", "ref weight/name")
        `CHECK(p.payload.size() == 2 && p.payload[0] == 9, "ref payload")
        `CHECK(p.kind == PROTO_ICMP, "ref kind")
        `CHECK(p.opts.size() == 3 && p.opts[2] == 5, "ref opts")
        `CHECK(p.tag == ((96'h1 << 95) | 96'h1), $sformatf("ref tag %0h", p.tag))
        `CHECK(p.h.src == 32'h0A000001, "ref nested h.src")
    endtask

    task automatic test_py_ref();
        pyhdl_if::PyObject o;
        pkt_if r;
        hdr_if h;
        hdr hv = new();
        int opts[$];
        pyhdl_if::pyhdl_if_bytes_t payload;
        longint rc0, rc1;
        $display("[SV] test_py_ref");
        o = call_py("make_py_pkt");
        rc0 = py_int(call_py("py_pkt_refcount"));
        r = pkt_ref_from_py(o);
        py_decref(o);
        rc1 = py_int(call_py("py_pkt_refcount"));
        `CHECK(rc1 == rc0, $sformatf("refcount after wrap: %0d vs %0d", rc1, rc0))

        `CHECK(r.get_ttl() == 33 && r.get_id() == -7, "py get_ttl/id")
        `CHECK(r.get_name() == "py", "py get_name")
        `CHECK(r.get_kind() == PROTO_TCP, "py get_kind")
        payload = r.get_payload();
        `CHECK(payload.size() == 3 && payload[2] == 3, "py get_payload")
        `CHECK(r.get_tag() == 96'h77, "py get_tag")
        `CHECK(sum_ttl(r) == 38, $sformatf("sum_ttl(py ref) %0d", sum_ttl(r)))
        begin
            pkt local_p = mk_pkt();
            `CHECK(sum_ttl(local_p) == 200 + 32'hC0A80001, "sum_ttl(local)")
        end

        r.set_ttl(r.get_ttl() + 1);
        r.set_name({r.get_name(), "+sv"});
        payload.push_back(4);
        r.set_payload(payload);
        r.set_kind(PROTO_UDP);
        opts = r.get_opts();
        opts.push_back(30);
        r.set_opts(opts);
        r.set_tag((96'h1 << 90) | 96'h77);
        h = r.get_h();
        `CHECK(h.get_src() == 5 && h.get_proto() == PROTO_UDP, "py nested get")
        h.set_src(55);
        h.dispose();
        // set_h copies a value in; the Python object now has a new hdr
        hv.src = 55;
        hv.dst = 66;
        hv.proto = PROTO_ICMP;
        r.set_h(hv);
        hv.dst = 1;  // no effect: set_h copied
        py_decref(call_py("check_py_pkt"));

        // A snapshot through accessors
        begin
            pkt snap = pkt_from_if(r);
            `CHECK(snap.ttl == 34 && snap.h.dst == 66, "pkt_from_if")
        end

        r.dispose();
        rc1 = py_int(call_py("py_pkt_refcount"));
        `CHECK(rc1 == rc0 - 1, $sformatf("refcount after dispose: %0d vs %0d", rc1, rc0 - 1))
        r.dispose();  // twice is harmless

        // Use after dispose is a runtime error
        begin
            int errs0 = pyhdl_if::pyhdl_if_rt_errors;
            void'(r.get_ttl());
            `CHECK(pyhdl_if::pyhdl_if_rt_errors == errs0 + 1, "use after dispose not reported")
        end
        `CHECK(py_int(call_py("drop_py_pkt")) == 1, "Python pkt not freed")
    endtask

    task automatic test_sv_svc();
        sv_svc svc = new();
        pyhdl_if::PyObject o, res;
        int py_errs;
        int nobjs;
        $display("[SV] test_sv_svc");
        o = pkt_svc_to_py(svc);
        pyhdl_if::pyhdl_if_rt_callPyTask(res, m_test, "run_sv_svc", args1(o));
        py_errs = int'(py_int(res));
        `CHECK(py_errs == 0, $sformatf("run_sv_svc: %0d Python errors", py_errs))
        `CHECK(svc.kept.size() == 1 && svc.kept[0].ttl == 49, "sv kept ref modified via Python")
        nobjs = pyhdl_if::pyhdl_if_rt_numObjs();
        $display("[SV] object slots in use: %0d (table size %0d)", nobjs, pyhdl_if::__objects.size());
        `CHECK(pyhdl_if::__objects.size() <= 128, $sformatf("object table grew to %0d", pyhdl_if::__objects.size()))
    endtask

    task automatic test_py_svc();
        pkt_svc svc;
        pyhdl_if::PyObject o;
        pkt p = mk_pkt(), q;
        pkt_if r;
        sv_cb cb = new();
        $display("[SV] test_py_svc");
        o = call_py("make_py_svc");
        svc = pkt_svc_from_py(o);
        `CHECK(svc.add(40, 2) == 42, "py add")
        q = svc.bump(p);
        `CHECK(q.ttl == 199 && p.ttl == 200, "py bump")
        svc.touch(p);
        `CHECK(p.ttl == 199 && p.opts.size() == 5 && p.opts[4] == 99, "py touch(local)")
        r = svc.make_ref(12);
        `CHECK(r.get_ttl() == 12 && r.get_name() == "kept", "py make_ref")
        r.set_ttl(13);
        py_decref(call_py("check_py_svc_kept", args1(py_incref(o))));
        r.dispose();
        svc.xfer(q, p);
        `CHECK(q.id == -4 && p.id == -5, $sformatf("py xfer %0d", q.id))
        svc.touch_t(p);
        `CHECK(p.ttl == 209, $sformatf("py touch_t %0d", p.ttl))
        svc.subscribe(cb);
        svc.fire(7);
        svc.fire(8);
        `CHECK(cb.got.size() == 2 && cb.got[0] == 7 && cb.got[1] == 8, "sv callbacks")
        svc.dispose();
        `CHECK(svc.add(1, 1) == 0, "use after dispose")

        // Python exceptions surface as runtime errors
        begin
            int errs0 = pyhdl_if::pyhdl_if_rt_errors;
            pkt_svc bad = pkt_svc_from_py(call_py("make_failing_svc"));
            void'(bad.add(1, 2));
            `CHECK(pyhdl_if::pyhdl_if_rt_errors == errs0 + 1, "function exception not reported")
            bad.xfer(q, p);
            `CHECK(pyhdl_if::pyhdl_if_rt_errors == errs0 + 2, "task exception not reported")
            `CHECK(q == null, "task exception result")
            bad.dispose();
        end
        py_decref(o);
    endtask

    task automatic test_timing();
        pkt p = mk_pkt();
        pyhdl_if::PyObject o, r;
        longint t0, t1;
        int n = 2000;
        int sz = 256;
        int sizes[3] = '{0, 256, 1500};
        $display("[SV] test_timing");
        foreach (sizes[k]) begin
            p.payload.delete();
            for (int i=0; i<sizes[k]; i++) p.payload.push_back(i);
            t0 = pyhdl_if::pyhdl_if_get_real_time_ms();
            for (int i=0; i<n; i++) begin
                o = pkt_to_py(p);
                py_decref(o);
            end
            t1 = pyhdl_if::pyhdl_if_get_real_time_ms();
            $display("[SV] TIMING copy SV->Py (%0d-byte payload): %0.2f us/op", sizes[k], 1000.0*(t1-t0)/n);
            o = pkt_to_py(p);
            t0 = pyhdl_if::pyhdl_if_get_real_time_ms();
            for (int i=0; i<n; i++) begin
                pkt q = pkt_from_py(o);
            end
            t1 = pyhdl_if::pyhdl_if_get_real_time_ms();
            py_decref(o);
            $display("[SV] TIMING copy Py->SV (%0d-byte payload): %0.2f us/op", sizes[k], 1000.0*(t1-t0)/n);
        end
        p.payload.delete();
        for (int i=0; i<sz; i++) p.payload.push_back(i);

        o = pkt_to_py(p);
        t0 = pyhdl_if::pyhdl_if_get_real_time_ms();
        for (int i=0; i<n; i++) begin
            py_decref(call_py("touch_fields_copy", args1(pkt_to_py(p))));
        end
        t1 = pyhdl_if::pyhdl_if_get_real_time_ms();
        $display("[SV] TIMING call with copy + read 4 fields in Py: %0.2f us/op", 1000.0*(t1-t0)/n);

        r = pkt_ref_to_py(p);
        t0 = pyhdl_if::pyhdl_if_get_real_time_ms();
        for (int i=0; i<n; i++) begin
            py_decref(call_py("touch_fields_ref", args1(py_incref(r))));
        end
        t1 = pyhdl_if::pyhdl_if_get_real_time_ms();
        $display("[SV] TIMING call with ref + read 4 fields in Py: %0.2f us/op", 1000.0*(t1-t0)/n);
        py_decref(r);

        begin
            pkt_if pr = pkt_ref_from_py(o);
            int sum = 0;
            t0 = pyhdl_if::pyhdl_if_get_real_time_ms();
            for (int i=0; i<100*n; i++) begin
                sum += pr.get_ttl();
            end
            t1 = pyhdl_if::pyhdl_if_get_real_time_ms();
            $display("[SV] TIMING SV reads 1 field of a Python ref: %0.3f us/op", 1000.0*(t1-t0)/(100*n));
            pr.dispose();
        end
        py_decref(o);

        // Interface calls, both directions
        begin
            pyhdl_if::PyObject so = call_py("make_py_svc");
            pkt_svc ps = pkt_svc_from_py(so);
            pkt q;
            int sum = 0;
            t0 = pyhdl_if::pyhdl_if_get_real_time_ms();
            for (int i=0; i<n; i++) begin
                sum += ps.add(i, 1);
            end
            t1 = pyhdl_if::pyhdl_if_get_real_time_ms();
            $display("[SV] TIMING SV calls Py function (2 ints): %0.2f us/op", 1000.0*(t1-t0)/n);
            t0 = pyhdl_if::pyhdl_if_get_real_time_ms();
            for (int i=0; i<n/4; i++) begin
                ps.xfer(q, p);
            end
            t1 = pyhdl_if::pyhdl_if_get_real_time_ms();
            $display("[SV] TIMING SV calls Py task (pkt copy in/out): %0.2f us/op", 1000.0*(t1-t0)/(n/4));
            ps.dispose();
            py_decref(so);
        end
        begin
            sv_svc svc = new();
            pyhdl_if::PyObject res;
            pyhdl_if::PyGILState_STATE state = pyhdl_if::PyGILState_Ensure();
            pyhdl_if::PyObject args = pyhdl_if::PyTuple_New(2);
            void'(pyhdl_if::PyTuple_SetItem(args, 0, pkt_svc_to_py(svc)));
            void'(pyhdl_if::PyTuple_SetItem(args, 1, pyhdl_if::PyLong_FromLong(64'(n))));
            pyhdl_if::PyGILState_Release(state);
            pyhdl_if::pyhdl_if_rt_callPyTask(res, m_test, "time_sv_svc", args);
            py_decref(res);
        end
    endtask

    initial begin
        pyhdl_if::PyGILState_STATE state;
        int fd, py_errs;

        pyhdl_if::pyhdl_if_start();
        pyhdl_if::pyhdl_if_rt_error_fatal = 0;

        state = pyhdl_if::PyGILState_Ensure();
        m_test = pyhdl_if::PyImport_ImportModule("spike_drv");
        if (m_test == null) begin
            pyhdl_if::PyErr_Print();
            $display("FAIL: cannot import spike_drv");
            $finish;
        end
        pyhdl_if::PyGILState_Release(state);

        test_copy();
        test_sv_ref();
        test_py_ref();
        test_sv_svc();
        test_py_svc();
        test_timing();

        py_errs = int'(py_int(call_py("errors")));

        $display("[SV] errors=%0d py_errors=%0d rt_errors=%0d", errors, py_errs, pyhdl_if::pyhdl_if_rt_errors);
        fd = $fopen("status.txt", "w");
        // 4 runtime errors are deliberate: use after dispose (2), Python
        // function and task exceptions (2)
        if (errors == 0 && py_errs == 0 && pyhdl_if::pyhdl_if_rt_errors == 4) begin
            $fdisplay(fd, "PASS:");
        end else begin
            $fdisplay(fd, "FAIL: errors=%0d py_errors=%0d rt_errors=%0d",
                errors, py_errs, pyhdl_if::pyhdl_if_rt_errors);
        end
        $fclose(fd);
        $finish;
    end

endmodule
