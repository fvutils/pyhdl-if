
module call_proto();
    reg[31:0] call_proto_m;

    initial begin
        // Call 
        $display("Create a task and wait for its completion");
//        forever begin
            #1ns;
            $pyhdl_if_idle();
//        end
        #1us;
        $finish;
    end

    reg        ev = 0;

    task put();
        $display("put");
    endtask

    initial begin : interp
        static reg[31:0]  call_if;
        static reg[31:0]  init_h, args, res;
        static reg[31:0]  info_h;
        static reg[31:0]  None = $pyhdl_if_None();
        static reg[31:0]  req, id_o, id;
        static int i, tmp;
        
        call_proto_m = $PyImport_ImportModule("call_proto");
        $display("call_python_m: %08h", call_proto_m);

        // Create an interpreter
        $display("Create a fcall interpreter");
        call_if = $pyhdl_if_CallApi_init("call_proto", "CallIF", ev);
        $Py_IncRef(call_if);

        $display("call_if: 'h%08h", call_if);

        // Register methods
        $pyhdl_if_CallApi_setMethodId(call_if, "put", 1);
        $pyhdl_if_CallApi_setMethodId(call_if, "get", 2);

        info_h = $PyObject_GetAttrString(call_proto_m, "info");

        // Pass it to the Python module
        $display("Pass interpreter to init");
        init_h = $PyObject_GetAttrString(call_proto_m, "init");
        $display("init_h: %08h", init_h);
        $display("call_if: %08h", call_if);
        args = $PyTuple_New(1);
        tmp = $PyTuple_SetItem(args, 0, call_if);
        res = $PyObject_Call(init_h, args, 0);

        $display("call_if: 'h%08h", call_if);
//        $Py_DecRef(call_if);

        $display("res: %08h", res);

        forever begin : interp
            req = $pyhdl_if_CallApi_nextReq(call_if);

            $display("req=%08h None=%08h", req, None);


            if (req !== None) begin
                $Py_IncRef(req);

                args = $PyTuple_New(1);
                res = $PyTuple_SetItem(args, 0, req);
                $PyObject_Call(info_h, args, 0);

                id_o = $PyObject_GetAttrString(req, "id");
                $display("id_o: 'h%08h", id_o);
                $Py_IncRef(id_o);
                id = $PyLong_AsLong(id_o);
                $Py_DecRef(id_o);

                $display("id: %0d", id);

                case (id)
                1: begin : __put // put
                    $display("TODO: implement 'put'");
                    args = $PyObject_GetAttrString(req, "args");
                    put();
                    $pyhdl_if_CallApi_ack(req, $PyLong_FromLong(id));
                end
                2: begin // get
                end
                default: begin
                    $display("Command %0d", id);
                end
                endcase 

                $Py_DecRef(req);
            end else begin
                $display("--> ev");
                @(ev);
                $display("<-- ev");
            end
        end

	/*
        begin : vars
            static reg[63:0] res_o;
            static int res;
            static reg[63:0] args, lval;

	    $display("countones: %08h", countones);

            for (i=0; i<256; i=i+1) begin
                args = $PyTuple_New(1);
                res = $PyTuple_SetItem(args, 0, $PyLong_FromLong(i));
		$display("res: %0d", res);
                res_o = $PyObject_Call(countones, args, 0);
		$display("res_o: %08h", res_o);
                res = $PyLong_AsLong(res_o);
                if (res != $countones(i)) begin
                    $display("Error: res=%0d countones=%0d", res, $countones(i));
                end else begin
                    $display("Pass: %0d == %0d", res, $countones(i));
                end
            end
        end
	 */

    end
endmodule
