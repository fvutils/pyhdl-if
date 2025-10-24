typedef class ObjectIF;
typedef class pyhdl_via_object_type;

/**
 * pyhdl_via_object is a wrapper for the via type. It connects 
 * the SV APIs to the pyhdl-if Python APIs
 */
class pyhdl_via_object extends ObjectIF;
    via_object_if m_via_obj;

    function new(via_object_if obj);
        m_via_obj = obj;
    endfunction

    virtual function string get_name();
        return m_via_obj.get_name();
    endfunction

    virtual function pyhdl_if::PyObject get_object_type();
        via_object_type_if t = m_via_obj.get_object_type();
        pyhdl_via_object_type t_w = new(t);
        return t_w.m_obj;
    endfunction

    virtual function pyhdl_if::PyObject pack_ints();
        int unsigned intstream[];
        int bits;
        py_object ret;
        py_list intstream_l = new();

        bits = m_via_obj.pack_ints(intstream);

        foreach (intstream[i]) begin
            intstream_l.append_obj(PyLong_FromUnsignedLong(longint'(intstream[i])));
        end

        ret = py_tuple::mk_init('{py_from_int(bits), intstream_l});

        return ret.borrow();
    endfunction

    virtual function int unpack_ints(pyhdl_if::PyObject intstream);
        typedef int unsigned uint32_t;
        int bits;
        int unsigned data[] = new[int'(pyhdl_if::PyList_Size(intstream))];

        for (int i=0; i<data.size(); i++) begin
            data[i] = uint32_t'(PyLong_AsLong(PyList_GetItem(intstream, longint'(i))));
        end

        bits = m_via_obj.unpack_ints(data);

        return bits;
    endfunction

endclass
