/**
 * The env's implementation of ipv4_env_api, and py_test, which hands it
 * to a Python test and runs that test.
 */
package py_test_pkg;
    import uvm_pkg::*;
    import ipv4_pkt_pkg::*;
    import ipv4_env_pkg::*;
    import env_api_pkg::*;
    `include "uvm_macros.svh"

    class single_pkt_seq extends uvm_sequence #(pkt_item);
        `uvm_object_utils(single_pkt_seq)

        pkt_item item;

        function new(string name="single_pkt_seq");
            super.new(name);
        endfunction

        task body();
            start_item(item);
            finish_item(item);
        endtask
    endclass

    class ipv4_env_api_impl implements ipv4_env_api;
        ipv4_env        env;
        int unsigned    seed;

        function new(ipv4_env env);
            this.env = env;
            seed = $urandom;
        endfunction

        virtual task send(pkt_item p);
            single_pkt_seq s = single_pkt_seq::type_id::create("s");
            p.fix();
            s.item = p;
            s.start(env.in_agent.sqr);
        endtask

        virtual task set_route(int idx, int unsigned prefix, int len, int port);
            env.csr.set_route(idx, prefix, len, port);
            // Keep the scoreboard's copy of the table in step
            if (idx < env.cfg.rt_prefix.size()) begin
                env.cfg.rt_prefix[idx] = prefix;
                env.cfg.rt_len[idx] = len;
                env.cfg.rt_port[idx] = port;
            end else begin
                env.cfg.add_route(prefix, len, port);
            end
        endtask

        virtual task wait_idle();
            env.wait_idle();
        endtask

        virtual task get_fwd_count(output int unsigned count, input int port);
            env.csr.read_fwd_count(port, count);
        endtask

        virtual task get_drop_count(output int unsigned count, input pkt_fate_e reason);
            env.csr.read_drop_count(reason, count);
        endtask

        virtual function int unsigned get_seed();
            return seed;
        endfunction
    endclass

    class py_test extends ipv4_base_test;
        `uvm_component_utils(py_test)

        function new(string name, uvm_component parent);
            super.new(name, parent);
        endfunction

        // The stimulus is the Python test: <module>.run(api), module from
        // +PY_TEST (default ipv4_scenario)
        virtual task run_traffic();
            ipv4_env_api_impl api = new(env);
            string mod = "ipv4_scenario";
            pyhdl_if::PyObject m, args, res;

            void'($value$plusargs("PY_TEST=%s", mod));
            // A Python exception returns null rather than ending the
            // simulation, so it is reported here and the test fails in UVM
            pyhdl_if::pyhdl_if_rt_error_fatal = 0;
            pyhdl_if::pyhdl_if_start();
            pyhdl_if::py_gil_enter();
            m = pyhdl_if::PyImport_ImportModule(mod);
            if (m == null) begin
                pyhdl_if::PyErr_Print();
                pyhdl_if::py_gil_leave();
                `uvm_fatal(get_type_name(), $sformatf("failed to import %s", mod))
                return;
            end
            args = pyhdl_if::PyTuple_New(1);
            void'(pyhdl_if::PyTuple_SetItem(args, 0, api_gen_pkg::ipv4_env_api_to_py(api)));
            pyhdl_if::py_gil_leave();

            `uvm_info(get_type_name(), $sformatf("running %s.run (seed %0d)", mod, api.seed), UVM_LOW)
            pyhdl_if::pyhdl_if_rt_callPyTask(res, m, "run", args);
            if (res == null)
                `uvm_error(get_type_name(), $sformatf("%s.run raised an exception", mod))
        endtask
    endclass
endpackage
