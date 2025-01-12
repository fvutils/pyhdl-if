
module data1;
    import pyhdl_if::*;

    initial begin
        automatic string datafile;
        automatic py_object json, data_fp, data_s;
        automatic py_dict data;
        automatic py_list keys;

        $display("1");
        if (!$value$plusargs("data=%s", datafile)) begin
            $display("Error: no datafile specified");
            $finish;
        end

        py_gil_enter();

        // Import Python's 'json' package 
        json = py_import("json");

        // Open and read the specified data file
        data_fp = py_call_builtin("open", py_tuple::mk_init('{
            py_from_str(datafile),
            py_from_str("r")}));
        data_s = data_fp.call_attr("read"); 
        data_fp.call_attr("close");

        // Parse the data
        data = py_dict::mk(json.call_attr("loads", py_tuple::mk_init('{data_s})));

        // Get the list of keys
        keys = data.keys();

        // Iterate based on the list size
        for (int i=0; i<keys.size(); i++) begin
            $display("Key: %0d %0s", i, keys.get_item(i).to_str());
        end

        // Use an iterator
        for (py_iter i=keys.iter(); i.valid(); ) begin
            automatic py_object it = i.next();
            $display("Key: %0s", it.to_str());
        end
        
        data = py_dict::mk(json.call_attr("loads", 
            py_tuple::mk_init('{data_s})));
        keys = data.keys();

        // Iterate based on the list size
        for (int i=0; i<keys.size(); i++) begin
            $display("Key: %0d %0s", i, keys.get_item(i).to_str());
        end

        // Use an iterator
        for (py_iter i=keys.iter(); i.valid(); ) begin
            automatic py_object it = i.next();
            $display("Key: %0s", it.to_str());
        end

        begin
            int fp = $fopen("status.txt", "w");
            if (keys.size() == 2) begin
                $fwrite(fp, "PASS:\n");
            end else begin
                $fwrite(fp, "FAIL: %0d != 2\n", keys.size());
            end
            $fclose(fp);
        end
        keys.dispose();
        data.dispose();

        py_gil_leave();
        $finish;

    end
endmodule