
class pyhdl_uvm_cmdline_processor extends pyhdl_uvm_object;
    uvm_cmdline_processor           m_clp;

    function new(uvm_object clp);
        super.new(clp);
    endfunction

    virtual function pyhdl_if::PyObject get_plusargs();
        uvm_cmdline_processor clp;
        string plusargs[$];
        py_list ret = new();

        $cast(clp, m_uvm_obj);

        clp.get_plusargs(plusargs);

        foreach (plusargs[i]) begin
            ret.append(py_from_str(plusargs[i]));
        end

        return ret.borrow();
    endfunction

endclass

`pyhdl_uvm_type_utils(uvm_cmdline_processor, uvm_object)

