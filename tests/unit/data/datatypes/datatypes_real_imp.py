
import ctypes as ct
import hdl_if as hif

@hif.api
class RealImp(object):

    @hif.imp
    def add(self, a : ct.c_double, b : ct.c_double) -> ct.c_double: pass

    @hif.exp
    def test(self) -> ct.c_int:
        status = 0

        try:
            result = self.add(0, 0)
            # for i in range(10):
            #     for j in range(10):
            #         result = self.add(i, j)

            #         if result != i+j:
            #             status = 1
        except Exception as e:
            print("Exception: %s" % str(e), flush=True)

        return status
