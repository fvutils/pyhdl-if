`include "via_macros.svh"

package pyhdl_if_via;
    import pyhdl_if::*;
    import via::*;

    `include "pyhdl_via_component.svh"
    `include "pyhdl_via_object.svh"
    `include "pyhdl_via_root_if.svh"
    `include "pyhdl_via_root_listener.svh"
    `include "via_if.svh"

    function automatic pyhdl_via_root_listener __initialize();
        via_root root = via_root::get();
        pyhdl_via_root_listener root_listener = new();

        root.add_listener(root_listener);

        return root_listener;
    endfunction

    pyhdl_via_root_listener __listener = __initialize();


endpackage
