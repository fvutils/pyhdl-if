
//
// UNFINISHED -- NOT PART OF THE BUILD.
//
// This file is not `include`-ed by pyhdl_if.sv and nothing references
// py_builtins.  It does not compile: get_builtins has a bare `m_builtins`
// where an assignment belongs, and call() has an unterminated assignment and
// no return.  It is left in place as a sketch of an intended convenience
// wrapper for the Python builtins module.
//
// Finish it, or delete it -- but do not `include` it as it stands, and do not
// document it in the SV reference until it works.  See doc/documentation-plan.md
// F18.
//
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