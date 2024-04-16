import ctypes
import hdl_call_if as hci

@hci.api
class MyC(object):

    @hci.expfunc
    def countones(self, vi : ctypes.c_int) -> ctypes.c_int:
        ret = 0
        v = vi
        while v:
            ret += 1 if (v&1) else 0
            v >>= 1
        return ret * self.getscale(vi)
    
    @hci.impfunc
    def getscale(self, v : ctypes.c_int) -> ctypes.c_int:
        pass

