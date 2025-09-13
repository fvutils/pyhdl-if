
import ctypes as ct
import hdl_if as hif

@hif.api
class RealExp(object):

    @hif.exp
    def add(self, a : ct.c_double, b : ct.c_double) -> ct.c_double:
        ret = a + b
        return ret
