
module counter_bfm;
    import pyhdl_if::*;
    import threaded_test_pkg::*;

    // Counter value
    int unsigned counter_value = 0;

    // Counter implementation class
    class CounterImpl extends Counter_imp_impl #(CounterImpl);

        function new();
            super.new(this);
        endfunction

        virtual task increment(output int unsigned retval);
            // Increment and return the new value
            counter_value++;
            retval = counter_value;
            $display("[SV] increment: counter = %0d at time %0t", counter_value, $time);
            // Small delay to simulate some work
            #10ns;
        endtask

        virtual task get_value(output int unsigned retval);
            retval = counter_value;
            $display("[SV] get_value: counter = %0d at time %0t", counter_value, $time);
        endtask

    endclass

    CounterImpl m_counter;

    initial begin
        automatic ThreadedTest_exp_impl test;

        // Start the PyHDL-IF event loop
        pyhdl_if_start();

        // Create the counter implementation
        m_counter = new();

        // Register the counter object
        pyhdl_if::pyhdl_if_registerObject(m_counter.m_obj, $sformatf("%m.m_counter"), 1);

        // Small delay
        #10ns;

        // Create test instance and run
        $display("[SV] %0t --> Starting threaded test", $time);
        test = new();
        test.run(m_counter.m_obj);
        $display("[SV] %0t <-- Threaded test complete", $time);
        
        $finish;
    end

endmodule
