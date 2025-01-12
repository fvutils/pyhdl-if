
import ctypes as ct
import hdl_if as hif

@hif.api
class WishboneInitiator(object):

    @hif.imp
    async def write(self, addr : ct.c_uint32, data : ct.c_uint32):
        pass

    @hif.imp
    async def read(self, addr : ct.c_uint32) -> ct.c_uint32:
        pass

@hif.api
class Test(object):

    @hif.exp
    async def run(self, bfm : ct.py_object):
        print("run")

        for i in range(64):
            wr_val = (i+1)
            print(f'[Py] writing: {wr_val}')
            await bfm.write(0x8000_0000+(4*i), wr_val)
            rd = await bfm.read(0x8000_0000+(4*i))
            print(f'[Py] readback: {rd}')
            assert wr_val == rd

        for i in range(64):
            await bfm.read(0x8000_0000+(4*i))

    pass
