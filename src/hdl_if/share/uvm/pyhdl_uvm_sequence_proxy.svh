
typedef class pyhdl_uvm_sequence_proxy_helper;



class pyhdl_uvm_sequence_proxy #(type REQ=uvm_sequence_item, type RSP=REQ, string PyClass="")
    extends uvm_sequence #(.REQ(REQ), .RSP(RSP));
    typedef pyhdl_uvm_sequence_proxy #(.REQ(REQ), .RSP(RSP), .PyClass(PyClass)) this_t;
    `uvm_object_param_utils(this_t);

    typedef pyhdl_uvm_sequence_proxy_helper #(.REQ(REQ), .RSP(RSP)) helper_t;

    string      pyclass = PyClass;
    helper_t    m_helper;

    function new(string name="pyhdl_uvm_sequence_proxy");
        super.new(name);
    endfunction

    task body();
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

        $display("modname=%0s clsname=%0s", modname, clsname);

        m_helper = new();
        m_helper.m_proxy = this;
        m_helper.init(m_helper.create_pyobj(modname, clsname));

        m_helper.body();
    endtask

endclass

class pyhdl_uvm_sequence_proxy_helper #(type REQ=uvm_sequence_item, type RSP=REQ) 
        extends UvmSequenceProxy_wrap;
    uvm_sequence_base       m_proxy;

    virtual function string get_name();
        $display("get_name");
        return m_proxy.get_name();
    endfunction

    virtual function PyObject create_req();
        REQ req = REQ::type_id::create();
        return null;
    endfunction

    virtual function PyObject create_rsp();
        RSP req = REQ::type_id::create();
        return null;
    endfunction

endclass