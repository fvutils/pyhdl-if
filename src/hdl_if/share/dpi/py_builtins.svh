
class py_builtins;
    static py_object    m_builtins;

    static function py_object get_builtins();
        if (m_builtins == null) begin
            m_builtins
        end
        return m_builtins;
    endfunction

    static function py_object call(string name, py_tuple args, py_dict kwargs=null);
        py_object builtins = 
    endfunction
endclass