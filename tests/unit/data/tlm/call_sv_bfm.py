
import ctypes as ct
import hdl_if as hif

@hif.tlm_if
class WishboneInitiator(object):

    def __init__(self):
        self._lock = hif.get_backend().mkLock()

    async def write(self, addr : ct.c_uint32, data : ct.c_uint32):
        pass

    async def read(self, addr : ct.c_uint32) -> ct.c_uint32:
        pass

    class ReqData(ct.Structure):
        _fields_ = [
            ('addr', ct.c_uint32),
            ('data', ct.c_uint32)
        ]
    
    class RspData(ct.Structure):
        _fields_ = [
            ('data', ct.c_uint32)
        ]

    @hif.req_fifo
    def req(self, t : ReqData):
        pass

    @hif.rsp_fifo
    def rsp(self) -> RspData:
        pass

@hif.api
class Test(object):

    @hif.exp
    async def run(self, bfm : ct.py_object):
        errors = 0
        print("run")

        for i in range(64):
            wr_val = (i+1)
            print(f'[Py] writing: {wr_val}')
            await bfm.write(0x8000_0000+(4*i), wr_val)
            rd = await bfm.read(0x8000_0000+(4*i))
            print(f'[Py] readback: {rd}')
            if wr_val != rd:
                errors += 1

        with open("status.txt", "w") as fp:
            fp.write("%s: %d errors\n" % (("PASS" if errors==0 else "FAIL"), errors))

