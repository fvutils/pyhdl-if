import ctypes
import hdl_call_if as hci

@hci.api
class MyC(object):

    @hci.expfunc
    def countones(self, v : ctypes.c_int) -> ctypes.c_int:
        ret = 0
        while v:
            ret += 1 if (v&1) else 0
            v >>= 1
        return ret

class MyCExt(MyC):

    def countones(self, v):
        print("MyCExt.countones", flush=True)
        return super().countones(v) + 5
