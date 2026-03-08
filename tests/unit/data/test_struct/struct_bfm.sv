
// Implement the BFM that Python will call
class StructBFM_Impl implements struct_api_pkg::StructBFM_imp_if;
    struct_api_pkg::Point_t m_point;

    function new();
        m_point.x = 0;
        m_point.y = 0;
    endfunction

    virtual task set_point(input struct_api_pkg::Point_t p);
        $display("[SV] set_point called: x=%0d, y=%0d", p.x, p.y);
        m_point = p;
    endtask

    virtual task get_point(output struct_api_pkg::Point_t retval);
        $display("[SV] get_point called, returning: x=%0d, y=%0d", m_point.x, m_point.y);
        retval = m_point;
    endtask

endclass

module struct_bfm
    import struct_api_pkg::*;
    import pyhdl_if::*;
(
);

    StructBFM_imp_impl#(StructBFM_Impl) bfm;
    Point_t     stored_point;

    initial begin
        automatic StructBFM_Impl impl = new();
        automatic StructTest_exp_impl test;
        int fd;
        string line;
        
        pyhdl_if::pyhdl_if_start();
        
        bfm = new(impl);
        
        $display("[SV] BFM created");
        
        // Run the test
        test = new();
        test.run(bfm.m_obj);
        
        $display("[SV] Test completed");
        
        // Check the final status
        fd = $fopen("status.txt", "r");
        if (fd) begin
            void'($fgets(line, fd));
            $display("%s", line);
            $fclose(fd);
        end else begin
            $display("FAIL: Could not open status.txt");
        end
        
        $finish;
    end

endmodule
