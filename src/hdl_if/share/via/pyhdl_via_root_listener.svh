/****************************************************************************
 * pyhdl_via_root_listener.svh
 *
 *
 ****************************************************************************/

typedef interface class IRoot;
typedef class Root_wrap;

class pyhdl_via_root_listener extends via_root_listener_if;
    IRoot           roots[string];
    py_object       pyhdl_via;

    function new();
        pyhdl_via = py_import("hdl_if.via");
    endfunction

    virtual function void post_build(via_component_if root);
        PyObject cls;
        string option = "pyhdl.via.class=%s";
        string option_name = {"pyhdl.via.class.", root.get_name(), "=%s"};
        string clsname;
        py_ctxt ctxt = new();
        pyhdl_via_component root_obj;
        py_object root_obj_h;
        Root_wrap root_h;

        $display("post_build %0s", root.get_name());
        if ($value$plusargs(option, clsname)) begin
            $display("Found class name: %s", clsname);
        end else if ($value$plusargs(option_name, clsname)) begin
            $display("Found class name: %s", clsname);
        end

        if (clsname != "") begin
            py_object load = pyhdl_via.get_attr("load");
            py_object cls, post_build;

            $display("--> Create new object");
            root_obj = new(root);
            root_obj_h = new(root_obj.m_obj);
            void'(ctxt.add(root_obj_h));
            $display("<-- Create new object");

            $display("--> Python class: %0s", clsname);
            py_gil_enter();
            cls = py_check(load.call(py_tuple::mk_init({py_from_str(clsname)})));
            root_h = new(cls.borrow());
            roots[root.get_full_name()] = root_h;
            py_gil_leave();
            $display("<-- Python class: %0s", clsname);

            post_build = py_check(cls.get_attr("post_build"));
            void'(ctxt.add(post_build));

            py_gil_enter();
            void'(py_check(post_build.call(py_tuple::mk_init('{root_obj_h}))));
            py_gil_leave();
            ctxt.dispose();
        end else begin
            $display("No Python class");
        end

    endfunction

    virtual function void post_connect(via_component_if root);
        pyhdl_via_component root_obj;
        py_object root_obj_h;
        py_ctxt ctxt = new();
        $display("-- post_connect");

        if (roots.exists(root.get_full_name())) begin
            py_object post_connect;
            IRoot root_h = roots[root.get_full_name()];

            root_obj = new(root);
            root_obj_h = new(root_obj.m_obj);
            void'(ctxt.add(root_obj_h));


            py_gil_enter();
            $display("--> Calling class post_connect");
            root_h.post_connect(root_obj.m_obj);
            $display("<-- Calling class post_connect");
            py_gil_leave();
        end else begin
            $display("No root");
        end

        ctxt.dispose();
    endfunction

    virtual task run(via_component_if root);
        pyhdl_via_component root_obj;
        py_object root_obj_h;
        py_ctxt ctxt = new();

        $display("post_run");

        if (roots.exists(root.get_full_name())) begin
            py_object post_connect;
            IRoot root_h = roots[root.get_full_name()];

            root_obj = new(root);
            root_obj_h = new(root_obj.m_obj);
//            void'(ctxt.add(root_obj_h));

            fork
                root_h.run(root_obj_h.borrow());
            join_none
        end

        ctxt.dispose();
    endtask

endclass
