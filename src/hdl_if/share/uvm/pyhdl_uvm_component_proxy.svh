
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

        $display("modname=%0s clsname=%0s", modname, clsname);

        m_helper = new();
        m_helper.init(m_helper.create_pyobj(modname, clsname));
        m_helper.m_proxy = this;

        m_helper.build_phase(null);
    endfunction

    function void connect_phase(uvm_phase phase);
        m_helper.connect_phase(null);
    endfunction

    task run_phase(uvm_phase phase);
        m_helper.run_phase(null);
    endtask

endclass

class pyhdl_uvm_component_proxy_helper extends UvmComponentProxy_wrap;
    pyhdl_uvm_component_proxy       m_proxy;

    virtual function PyObject get_parent();
        return pyhdl_uvm_object_rgy::inst().wrap(m_proxy.get_parent());
    endfunction

endclass

