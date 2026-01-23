
// Simple graphics canvas implementation using structs
class GraphicsAPI_Impl implements struct_passing_pkg::GraphicsAPI_imp_if;
    // Simple framebuffer: stores last drawn pixel/rectangle info
    struct_passing_pkg::Point_t last_point;
    struct_passing_pkg::Color_t last_color;
    struct_passing_pkg::Rectangle_t last_rect;
    
    // Canvas dimensions
    const int CANVAS_WIDTH = 1920;
    const int CANVAS_HEIGHT = 1080;
    
    function new();
        last_point.x = 0;
        last_point.y = 0;
        last_color.r = 0;
        last_color.g = 0;
        last_color.b = 0;
        last_color.a = 0;
        last_rect.x = 0;
        last_rect.y = 0;
        last_rect.width = 0;
        last_rect.height = 0;
    endfunction
    
    virtual task draw_point(
        input struct_passing_pkg::Point_t pos,
        input struct_passing_pkg::Color_t color
    );
        $display("[SV] draw_point: pos=(%0d,%0d) color=RGBA(%0d,%0d,%0d,%0d)", 
                 pos.x, pos.y, color.r, color.g, color.b, color.a);
        
        // Store the last point and color
        last_point = pos;
        last_color = color;
    endtask
    
    virtual task draw_rectangle(
        input struct_passing_pkg::Rectangle_t rect,
        input struct_passing_pkg::Color_t color
    );
        $display("[SV] draw_rectangle: pos=(%0d,%0d) size=%0dx%0d color=RGBA(%0d,%0d,%0d,%0d)", 
                 rect.x, rect.y, rect.width, rect.height,
                 color.r, color.g, color.b, color.a);
        
        // Store the last rectangle and color
        last_rect = rect;
        last_color = color;
    endtask
    
    virtual task get_pixel(
        output struct_passing_pkg::Color_t retval,
        input struct_passing_pkg::Point_t pos
    );
        $display("[SV] get_pixel: pos=(%0d,%0d)", pos.x, pos.y);
        
        // Return the last color drawn at this position
        // (simplified - real implementation would have a framebuffer)
        if (pos.x == last_point.x && pos.y == last_point.y) begin
            retval = last_color;
            $display("[SV]   returning: RGBA(%0d,%0d,%0d,%0d)", 
                     retval.r, retval.g, retval.b, retval.a);
        end else begin
            // Return black for other positions
            retval.r = 0;
            retval.g = 0;
            retval.b = 0;
            retval.a = 0;
            $display("[SV]   returning: RGBA(0,0,0,0) [default]");
        end
    endtask
    
    virtual task get_bounds(output struct_passing_pkg::Rectangle_t retval);
        $display("[SV] get_bounds: returning canvas dimensions");
        retval.x = 0;
        retval.y = 0;
        retval.width = CANVAS_WIDTH;
        retval.height = CANVAS_HEIGHT;
        $display("[SV]   canvas: (%0d,%0d) size %0dx%0d", 
                 retval.x, retval.y, retval.width, retval.height);
    endtask
endclass

module struct_passing
    import struct_passing_pkg::*;
    import pyhdl_if::*;
(
);

    GraphicsAPI_imp_impl#(GraphicsAPI_Impl) gfx_api;

    initial begin
        automatic GraphicsAPI_Impl impl;
        automatic GraphicsTest_exp_impl test;
        
        $display("\n[SV] Starting struct_passing example");
        $display("[SV] Initializing PyHDL-IF...");
        pyhdl_if::pyhdl_if_start();
        
        // Create the graphics API implementation
        impl = new();
        gfx_api = new(impl);
        
        $display("[SV] Graphics API created");
        $display("[SV] Starting test...\n");
        
        // Run the Python test
        test = new();
        test.run(gfx_api.m_obj);
        
        $display("\n[SV] Test completed successfully");
        $finish;
    end

endmodule
