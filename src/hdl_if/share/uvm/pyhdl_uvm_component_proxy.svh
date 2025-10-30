
typedef class UvmComponentProxy_wrap;
typedef class pyhdl_uvm_component_proxy_helper;
typedef class pyhdl_uvm_object_rgy;

/**
 * Class used to implement a UVM component in Python
 * Set the value of the pyclass field to specify the
 * class to create
 */
class pyhdl_uvm_component_proxy extends uvm_component;
    `uvm_component_utils(pyhdl_uvm_component_proxy)

    string                              pyclass;
    pyhdl_uvm_component_proxy_helper    m_helper;

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
        string modname, clsname;
        PyObject mod, cls;
        int i;

        void'(pyhdl_uvm_object_rgy::inst());

        if (pyclass == "") begin
            `uvm_fatal(get_name(), "No value specified for 'pyclass'");
        end

        for (i=pyclass.len()-1; i>=0; i--) begin
            if (pyclass[i] == ":") begin
                clsname = pyclass.substr(i+1, pyclass.len()-1);
                break;
            end
        end

        if (clsname == "") begin
            `uvm_fatal(get_name(), $sformatf("Failed to find '::' in pyclass %0s", pyclass))
        end

        for (; i>=0; i--) begin
            if (pyclass[i] != ":") begin
                break;
            end
        end

        modname = pyclass.substr(0, i);

        mod = PyImport_ImportModule(modname);
        if (mod == null) begin
            PyErr_Print();
            `uvm_fatal(get_name, $sformatf("Failed to load Python module %0s", modname));
            return;
        end

        cls = PyObject_GetAttrString(mod, clsname);

        if (cls == null) begin
            PyErr_Print();
            `uvm_fatal(get_name, $sformatf("Failed to find class %0s in Python module %0s", 
                clsname, modname));
            return;
        end

        m_helper = new(pyclass, cls);
        m_helper.m_proxy = this;

        m_helper.build_phase(null);
    endfunction

    function void connect_phase(uvm_phase phase);
        m_helper.connect_phase(null);
    endfunction

    task run_phase(uvm_phase phase);
        // Ensure that the task scheduler is running
        pyhdl_if_start();

        m_helper.run_phase(null);
    endtask



endclass

class pyhdl_uvm_component_proxy_helper extends UvmComponentProxy;
    pyhdl_uvm_component_proxy       m_proxy;

    function new(string clsname, PyObject cls);
        PyObject impl_o, args;
        super.new();

        args = PyTuple_New(1);
        void'(PyTuple_SetItem(args, 0, m_obj));

        impl_o = PyObject_Call(cls, args, null);
        if (impl_o == null) begin
            PyErr_Print();
            $display("Fatal Error: Failed to construct user class %0s", clsname);
            $finish;
        end

        if (PyObject_SetAttrString(m_obj, "_impl", impl_o) != 0) begin
            PyErr_Print();
            $display("Fatal Error: Failed to set _impl on proxy wrapper");
            $finish;
        end
    endfunction

    virtual function PyObject get_parent();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.get_parent());
    endfunction

    virtual function PyObject get_config_object(string name);
        py_tuple ret;
        uvm_object obj;
        py_object py_obj;
        bit has = m_proxy.get_config_object(name, obj);
        py_object py_has;

        $display("has");

        if (has && obj != null) begin
            $display("have object");
            py_obj = new(pyhdl_uvm_object_rgy::inst().wrap(obj));
        end else begin
            $display("failed to get object");
        end

        py_has = py_from_bool(has);

        return py_tuple::mk_init({py_has, py_obj}).borrow();
    endfunction

endclass

