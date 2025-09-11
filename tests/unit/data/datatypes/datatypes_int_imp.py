import ctypes as ct
import hdl_if as hif

@hif.api
class IntImp(object):

    @hif.imp
    def add(self, a : ct.c_int, b : ct.c_int) -> ct.c_int: pass

    @hif.exp
    def test(self) -> ct.c_int:
        status = 0

        try:
            for i in range(10):
                for j in range(10):
                    result = self.add(i, j)

                    if result != i+j:
                        status = 1
        except Exception as e:
            print("Exception: %s" % str(e), flush=True)

        return status
