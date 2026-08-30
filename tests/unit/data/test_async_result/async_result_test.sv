
/*
 * Checks that the result of an @hif.exp async call is delivered to the
 * SV process that made the call, including when several such calls are
 * outstanding at the same time.
 */
module async_result_test;
    import pyhdl_if::*;
    import async_result_test_pkg::*;

    int unsigned errors = 0;

    // Simulation-time delay requested by the Python side
    class DelayImpl extends Delay_imp_impl #(DelayImpl);

        function new();
            super.new(this);
        endfunction

        virtual task wait_ns(input int unsigned delay_ns);
            #(delay_ns * 1ns);
        endtask

    endclass

    // Mirrors async_result_test.payload() on the Python side. All labels
    // used below are the same length, so every result string is too.
    function automatic string payload(string label);
        string pad = "";
        for (int i=0; i<48; i++) begin
            pad = {pad, "."};
        end
        return {label, ":", pad};
    endfunction

    function automatic void check_str(string what, string actual, string expected);
        if (actual != expected) begin
            $display("FAIL: %0s: expected '%0s', received '%0s'", what, expected, actual);
            errors++;
        end else begin
            $display("PASS: %0s", what);
        end
    endfunction

    function automatic void check_time(string what, time actual, time expected);
        if (actual != expected) begin
            $display("FAIL: %0s: expected %0t elapsed, saw %0t", what, expected, actual);
            errors++;
        end else begin
            $display("PASS: %0s (%0t elapsed)", what, actual);
        end
    endfunction

    // Four concurrent @hif.exp calls, each collecting into its own local.
    //
    // The delays are identical on purpose: all four results are produced
    // within the same delta region, so several exist before any waiting
    // process resumes. If the response is stored without a reference,
    // CPython is free to reclaim each result as soon as the responding
    // coroutine returns and hand the same block to the next one, leaving
    // more than one semaphore slot pointing at a single object.
    task automatic concurrent_burst(
        AsyncResultTest_exp_impl    test,
        DelayImpl                   delay,
        string                      tag);
        string r_a, r_b, r_c, r_d;

        fork
            test.echo(r_a, delay.m_obj, {tag, "-A"}, 10);
            test.echo(r_b, delay.m_obj, {tag, "-B"}, 10);
            test.echo(r_c, delay.m_obj, {tag, "-C"}, 10);
            test.echo(r_d, delay.m_obj, {tag, "-D"}, 10);
        join

        check_str({tag, "-A result"}, r_a, payload({tag, "-A"}));
        check_str({tag, "-B result"}, r_b, payload({tag, "-B"}));
        check_str({tag, "-C result"}, r_c, payload({tag, "-C"}));
        check_str({tag, "-D result"}, r_d, payload({tag, "-D"}));
    endtask

    initial begin
        automatic AsyncResultTest_exp_impl test;
        automatic DelayImpl delay;
        automatic string res;
        automatic time t0;
        automatic int fd;

        pyhdl_if_start();

        delay = new();
        test = new();

        #10ns;

        // Two back-to-back bursts, so semaphore slots are reused across
        // the boundary between them.
        concurrent_burst(test, delay, "burst0");
        concurrent_burst(test, delay, "burst1");

        // A zero-length wait returns without advancing simulation time
        t0 = $time;
        test.echo(res, delay.m_obj, "zerodly", 0);
        check_str("zero-delay result", res, payload("zerodly"));
        check_time("zero-delay elapsed time", $time-t0, 0);

        // Two sequential awaits in one call advance time by exactly the sum
        t0 = $time;
        test.echo_two_delays(res, delay.m_obj, "twodlys", 20, 30);
        check_str("two-delay result", res, payload("twodlys"));
        check_time("two-delay elapsed time", $time-t0, 50ns);

        // A blocking sleep in Python issues no wait_ns, so simulation time
        // must not advance across the call
        t0 = $time;
        test.echo_blocking(res, "blockng", 50);
        check_str("blocking result", res, payload("blockng"));
        check_time("blocking elapsed time", $time-t0, 0);

        fd = $fopen("status.txt", "w");
        if (errors == 0) begin
            $fdisplay(fd, "PASS: async result handoff");
        end else begin
            $fdisplay(fd, "FAIL: %0d errors", errors);
        end
        $fclose(fd);

        $display("async_result_test: %0d errors", errors);

        $finish;
    end

endmodule
