
import ctypes as ct
import hdl_if as hif

@hif.api
class RealExp(object):

    @hif.exp
    def add(self, a : ct.c_double, b : ct.c_double) -> ct.c_double:
        print("Hello from add", flush=True)
        print("Hello from add", flush=True)
        print("Hello from add", flush=True)
        print("Hello from add", flush=True)
        print("Hello from add", flush=True)
        return a + b