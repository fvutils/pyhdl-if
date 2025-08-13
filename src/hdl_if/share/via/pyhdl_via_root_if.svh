
typedef class RootIF;

class pyhdl_via_root_if extends RootIF;
    via_root_if           m_root;

    function new(via_root root);
        super.new();
        m_root = root;
    endfunction

    virtual function void info(input int level, input string msg);
        m_root.info(level, msg);
    endfunction

    virtual function void error(input string msg);
        m_root.error(msg);
    endfunction

    virtual function void fatal(input string msg);
        m_root.fatal(msg);
    endfunction

endclass

