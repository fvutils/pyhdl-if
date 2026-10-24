// Uses a generated package that was stamped with an unsupported runtime
// API version. Package initialization must stop the simulation first.
module ver_tb;
    import ver_pkg::*;
    initial begin
        pkt p = new();
        int fd = $fopen("status.txt", "w");
        $fdisplay(fd, "REACHED: %0d", p.ttl);
        $fclose(fd);
        $finish;
    end
endmodule
