`include "uvm_macros.svh"

module test_with_data;
  import uvm_pkg::*;
  import pyhdl_uvm::*;
  import pyhdl_if::*;
  import queue_int_test_pkg::*;

  initial begin
    test_queue_data obj;
    int unsigned packed_data[];
    test_queue_data obj_unpacked;
    
    // Initialize pyhdl_if
    pyhdl_if_init(1'b1);
    
    // Create object with populated queues
    obj = new("obj_with_data");
    obj.queue_8bit = {8'h12, 8'h34, 8'h56, 8'h78};
    obj.queue_16bit = {16'h100, 16'h200, 16'h300};
    obj.queue_signed = {32'sd127, -32'sd128, 32'sd0, -32'sd1};
    obj.scalar_field = 32'hDEADBEEF;
    
    $display("=== Original object ===");
    obj.print();
    
    // Pack the object
    void'(obj.pack_ints(packed_data));
    $display("Packed into %0d ints", packed_data.size());
    
    // Unpack into new object
    obj_unpacked = new("obj_unpacked");
    void'(obj_unpacked.unpack_ints(packed_data));
    
    $display("=== Unpacked object ===");
    obj_unpacked.print();
    
    // Verify
    assert(obj_unpacked.queue_8bit.size() == 4) else $error("queue_8bit size mismatch");
    assert(obj_unpacked.queue_8bit[0] == 8'h12) else $error("queue_8bit[0] mismatch");
    assert(obj_unpacked.queue_8bit[1] == 8'h34) else $error("queue_8bit[1] mismatch");
    assert(obj_unpacked.queue_8bit[2] == 8'h56) else $error("queue_8bit[2] mismatch");
    assert(obj_unpacked.queue_8bit[3] == 8'h78) else $error("queue_8bit[3] mismatch");
    
    assert(obj_unpacked.queue_16bit.size() == 3) else $error("queue_16bit size mismatch");
    assert(obj_unpacked.queue_16bit[0] == 16'h100) else $error("queue_16bit[0] mismatch");
    assert(obj_unpacked.queue_16bit[1] == 16'h200) else $error("queue_16bit[1] mismatch");
    assert(obj_unpacked.queue_16bit[2] == 16'h300) else $error("queue_16bit[2] mismatch");
    
    assert(obj_unpacked.queue_signed.size() == 4) else $error("queue_signed size mismatch");
    assert(obj_unpacked.queue_signed[0] == 127) else $error("queue_signed[0] mismatch");
    assert(obj_unpacked.queue_signed[1] == -128) else $error("queue_signed[1] mismatch");
    assert(obj_unpacked.queue_signed[2] == 0) else $error("queue_signed[2] mismatch");
    assert(obj_unpacked.queue_signed[3] == -1) else $error("queue_signed[3] mismatch");
    
    assert(obj_unpacked.scalar_field == 32'hDEADBEEF) else $error("scalar_field mismatch");
    
    $display("=== All assertions passed! ===");
    
    #100;
    $finish;
  end

endmodule
