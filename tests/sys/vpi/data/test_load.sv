
module test_load;

    initial begin : local
        reg[63:0] imp;
        $display("Hello World");
//        $my_task;
        $Py_Initialize();
        imp = $PyImport_ImportModule("load");
        $display("imp: %0d", imp);

    end

endmodule

