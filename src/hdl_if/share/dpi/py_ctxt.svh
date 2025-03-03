
typedef class py_object;

class py_ctxt;
    py_object objects[$];

    function void dispose();
        foreach (objects[i]) begin
            objects[i].dispose();
        end
    endfunction

    virtual function py_object add(py_object obj);
        objects.push_back(obj);
        return obj;
    endfunction

endclass
