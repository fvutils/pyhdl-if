
    /**
     * Schedules a Python callback for a point in simulation time.
     *
     * Exported to the C layer, which is how a Python `await` on a delay is
     * satisfied. Registration returns immediately; the callback fires when the
     * simulation reaches the requested time.
     *
     * @param target The Python object to call back. A reference is held until
     *        the callback has run.
     * @param time_ps Delay from now, in picoseconds.
     * @return The callback's id, which identifies it if it must be cancelled.
     */
    function automatic int pyhdl_pi_if_RegisterTimeCB(
        PyObject            target,
        longint unsigned    time_ps);
        PyHdlDpiTimeCB cb;
        int cb_id = -1;
        foreach (prv_time_cb[i]) begin
            if (prv_time_cb[i] == null) begin
                cb_id = i;
                break;
            end
        end

        if (cb_id == -1) begin
            cb_id = prv_time_cb.size();
            prv_time_cb.push_back(null);
        end

        cb = new(target, cb_id, time_ps);

        pyhdl_pi_if_queue_runnable(cb);

        return cb_id;
    endfunction
    export "DPI-C" function pyhdl_pi_if_RegisterTimeCB;
