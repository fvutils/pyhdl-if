
class pyhdl_uvm_pygen extends uvm_test;
    `uvm_component_utils(pyhdl_uvm_pygen)

    pyhdl_uvm_component_proxy  m_proxy;

    function new(string name, uvm_component parent=null);
        super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
        m_proxy = pyhdl_uvm_component_proxy::type_id::create("m_proxy", this);
        m_proxy.pyclass = "hdl_if.uvm.pygen::PyGen";
        m_proxy.build_phase(phase);
        $finish;
    endfunction

    function void connect_phase(uvm_phase phase);
        m_proxy.connect_phase(phase);
    endfunction

    task run_phase(uvm_phase phase);
        m_proxy.run_phase(phase);
    endtask

endclass

