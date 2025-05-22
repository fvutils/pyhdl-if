`include "uvm_macros.svh"

package pyuvm_if;
    import uvm_pkg::*;

    `include "pyuvm_root.svh"

    pyuvm_root __root = new("__pyuvm_root", uvm_root::get());


endpackage

