import ctypes
import hdl_call_if as hci

@hci.api
class MyC(object):

    @hci.exptask
    async def body(self):
        print("body", flush=True)
        for i in range(100):
            print("--> await read", flush=True)
            val = await self.read(i)
            print("<-- await read %s" % str(val), flush=True)

    @hci.imptask
    async def read(self, v : ctypes.c_int) -> ctypes.c_int:
        pass

