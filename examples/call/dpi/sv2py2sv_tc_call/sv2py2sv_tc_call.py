import ctypes
import hdl_if as hif

@hif.api
class MyC(object):

    @hif.exptask
    async def body(self):
        print("body", flush=True)
        for i in range(100):
            print("--> await read", flush=True)
            val = await self.read(i)
            print("<-- await read %s" % str(val), flush=True)

    @hif.imptask
    async def read(self, v : ctypes.c_int) -> ctypes.c_int:
        pass

