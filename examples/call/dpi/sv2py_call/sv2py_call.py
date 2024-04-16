import ctypes
import hdl_if as hif

@hif.api
class MyC(object):

    @hif.expfunc
    def countones(self, v : ctypes.c_int) -> ctypes.c_int:
        ret = 0
        while v:
            ret += 1 if (v&1) else 0
            v >>= 1
        return ret

