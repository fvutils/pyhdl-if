
// Comprehensive struct test BFM implementation
class ComprehensiveBFM_Impl implements struct_comprehensive_api_pkg::ComprehensiveBFM_imp_if;
    struct_comprehensive_api_pkg::Point_t m_point;
    struct_comprehensive_api_pkg::Color_t m_color;
    struct_comprehensive_api_pkg::Rectangle_t m_rectangle;
    struct_comprehensive_api_pkg::AllTypes_t m_all_types;
    struct_comprehensive_api_pkg::ManyFields_t m_many_fields;

    function new();
        m_point.x = 0;
        m_point.y = 0;
        m_color.r = 0;
        m_color.g = 0;
        m_color.b = 0;
        m_color.a = 0;
        m_rectangle.x = 0;
        m_rectangle.y = 0;
        m_rectangle.width = 0;
        m_rectangle.height = 0;
    endfunction

    virtual task set_point(input struct_comprehensive_api_pkg::Point_t p);
        $display("[SV] set_point: x=%0d, y=%0d", p.x, p.y);
        m_point = p;
    endtask

    virtual task get_point(output struct_comprehensive_api_pkg::Point_t retval);
        $display("[SV] get_point: returning x=%0d, y=%0d", m_point.x, m_point.y);
        retval = m_point;
    endtask

    virtual task set_color(input struct_comprehensive_api_pkg::Color_t c);
        $display("[SV] set_color: r=%0d, g=%0d, b=%0d, a=%0d", c.r, c.g, c.b, c.a);
        m_color = c;
    endtask

    virtual task get_color(output struct_comprehensive_api_pkg::Color_t retval);
        $display("[SV] get_color: returning RGBA(%0d,%0d,%0d,%0d)", 
                 m_color.r, m_color.g, m_color.b, m_color.a);
        retval = m_color;
    endtask

    virtual task set_rectangle(input struct_comprehensive_api_pkg::Rectangle_t r);
        $display("[SV] set_rectangle: (%0d,%0d) %0dx%0d", r.x, r.y, r.width, r.height);
        m_rectangle = r;
    endtask

    virtual task get_rectangle(output struct_comprehensive_api_pkg::Rectangle_t retval);
        $display("[SV] get_rectangle: returning (%0d,%0d) %0dx%0d", 
                 m_rectangle.x, m_rectangle.y, m_rectangle.width, m_rectangle.height);
        retval = m_rectangle;
    endtask

    virtual task set_all_types(input struct_comprehensive_api_pkg::AllTypes_t at);
        $display("[SV] set_all_types: i8=%0d, u8=%0d, i16=%0d, u16=%0d", 
                 at.i8, at.u8, at.i16, at.u16);
        $display("[SV]                i32=%0d, u32=%0d", at.i32, at.u32);
        $display("[SV]                i64=%0d, u64=%0d", at.i64, at.u64);
        $display("[SV]                f32=%f, f64=%f, b=%0d", at.f32, at.f64, at.b);
        m_all_types = at;
    endtask

    virtual task get_all_types(output struct_comprehensive_api_pkg::AllTypes_t retval);
        $display("[SV] get_all_types: returning all fields");
        retval = m_all_types;
    endtask

    virtual task set_many_fields(input struct_comprehensive_api_pkg::ManyFields_t mf);
        $display("[SV] set_many_fields: f0=%0d, f1=%0d, f2=%0d, f3=%0d, f4=%0d", 
                 mf.f0, mf.f1, mf.f2, mf.f3, mf.f4);
        $display("[SV]                  f5=%0d, f6=%0d, f7=%0d, f8=%0d, f9=%0d", 
                 mf.f5, mf.f6, mf.f7, mf.f8, mf.f9);
        m_many_fields = mf;
    endtask

    virtual task get_many_fields(output struct_comprehensive_api_pkg::ManyFields_t retval);
        $display("[SV] get_many_fields: returning all 10 fields");
        retval = m_many_fields;
    endtask

endclass

module struct_comprehensive_bfm
    import struct_comprehensive_api_pkg::*;
    import pyhdl_if::*;
(
);

    ComprehensiveBFM_imp_impl#(ComprehensiveBFM_Impl) bfm;

    initial begin
        automatic ComprehensiveBFM_Impl impl = new();
        automatic ComprehensiveTest_exp_impl test;
        int fd;
        string line;
        
        pyhdl_if::pyhdl_if_start();
        
        bfm = new(impl);
        
        $display("[SV] Comprehensive BFM created");
        
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
