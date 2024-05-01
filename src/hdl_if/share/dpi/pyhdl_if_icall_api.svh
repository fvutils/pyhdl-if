
interface class ICallApi;

    pure virtual function PyObject invokeFunc(
        string              method,
        PyObject            args);

    pure virtual task invokeTask(
        output PyObject     retval,
        input string        method,
        input PyObject      args);

endclass