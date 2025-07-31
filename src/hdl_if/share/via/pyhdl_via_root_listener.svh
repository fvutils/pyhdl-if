/****************************************************************************
 * pyhdl_via_root_listener.svh
 *
 *
 ****************************************************************************/

class pyhdl_via_root_listener extends via_root_listener_if;
    PyObject        roots[string];
    py_object       pyhdl_via;

    function new();
        pyhdl_via = py_import("hdl_if.via");
    endfunction

    virtual function void post_build(via_component_if root);
        PyObject cls;
        string option = "pyhdl.via.class=%s";
        string option_name = {"pyhdl.via.class.", root.get_name(), "=%s"};
        string clsname;

        $display("post_build %0s", root.get_name());
        if ($value$plusargs(option, clsname)) begin
            $display("Found class name: %s", clsname);
        end else if ($value$plusargs(option_name, clsname)) begin
            $display("Found class name: %s", clsname);
        end

        if (clsname != "") begin
            py_object load = pyhdl_via.get_attr("load");
            py_object cls, post_build;
            $display("--> Python class: %0s", clsname);
            cls = py_check(load.call(py_tuple::mk_init({py_from_str(clsname)})));
            $display("<-- Python class: %0s", clsname);

            post_build = py_check(cls.get_attr("post_build"));

            void'(py_check(post_build.call()));
        end else begin
            $display("No Python class");
        end

    endfunction

    virtual function void post_connnect(via_component_if root);
        $display("post_connect");

        if (roots.exists(root.get_name())) begin
        end
    endfunction

    virtual task run(via_component_if root);
        $display("post_run");
    endtask

endclass
