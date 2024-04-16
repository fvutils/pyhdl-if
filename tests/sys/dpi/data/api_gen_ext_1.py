import ctypes
import hdl_call_if as hci

@hci.api
class MyC(object):

    @hci.expfunc
    def get_py_val(self, i : ctypes.c_int) -> ctypes.c_int:
        print("get_py_val: %d" % i, flush=True)
        return i + 5

class MyCExt(MyC):

    def get_py_val(self, i):
        print("get_py_val(ext): %d" % i, flush=True)
        return i+8


