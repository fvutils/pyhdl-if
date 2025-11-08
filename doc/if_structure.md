
# PyHDL-IF SV Class API Interface

gen_sv_class creates two interfaces for each Python API class:
- An Exp interface class (<class>_exp_if) with pure virtual methods for each export method
- An Imp interface class (<class>_imp_if) with pure virtual methods for each import method

Each interface class has a corresponding 'impl' class.

class <class>_exp_impl implements <class>_exp_if;
  function new(PyObject obj=null, bit create=1, string clsname="<class>");
    if (obj == null && create) begin
        // Create an instance of the Python class
    end
  endfunction

  function void callpy();
    // Prepares arguments and calls Python object
  endfunction
endclass

class <class>_imp_impl #(type ImpT=<class>_imp_if) implements ICallApi;
  ImpT         m_impl;

  function new(ImpT impl, PyObject obj=null, bit create=1, string clsname="<class>");
    m_impl = impl;
    if (obj == null && create) begin
      // Create an instance of the Python class
    end
  endfunction

  virtual function PyObject invokeFunc(
    string method, PyObject args);
    // Decode

    // Call proper method
    m_impl.callsv();
  endfunction

endclass

Update the gen_sv_class generator to create the two interfaces and implementations described above.
The Imp implementation (ExpImpl) must implement the ICallApi interface. It must be parameterized with the type of the class that implements the exported functions. By default, this type is the Exp interface type. The 'new' method of the ExpImpl class must accept an argument of the template-parameter type. Store this argument in a class field where the invokeTask/invokeFunc methods can call it. Include the implementation of invokeTask and invokeFunc in this implementation class. 

