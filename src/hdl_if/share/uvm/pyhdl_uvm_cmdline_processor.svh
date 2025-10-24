
class pyhdl_uvm_cmdline_processor extends UvmCmdlineProcessor;
    uvm_cmdline_processor           m_clp;

    function new(uvm_cmdline_processor clp);
        super.new();
        m_clp = clp;
    endfunction

    virtual function pyhdl_if::PyObject _get_plusargs();
        py_list ret = new();
        string plusargs[$];
        m_clp.get_plusargs(plusargs);

        foreach (plusargs[i]) begin
            ret.append(py_from_str(plusargs[i]));
        end

        return ret.borrow();
    endfunction

endclass

