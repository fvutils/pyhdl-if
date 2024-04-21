import ctypes
import hdl_if as hif

@hif.api
class MyC(object):

    @hif.exptask
    async def body(self):
        exp = [0]*100
        for i in range(100):
            await self.write(4*i, exp[i])
        for i in range(100):
            val = await self.read(i)

    @hif.imptask
    async def read(self, addr : ctypes.c_uint) -> ctypes.c_uint:
        pass

    @hif.imptask
    async def write(self, addr : ctypes.c_uint, data : ctypes.c_uint):
        pass


