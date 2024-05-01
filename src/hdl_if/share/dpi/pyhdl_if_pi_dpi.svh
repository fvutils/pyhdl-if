
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
