import ctypes
import hdl_if as hif

@hif.tlm_if
class ReqRspLoopback(object):

    class ReqData(ctypes.Structure):
        _fields_ = [
            ('data', ctypes.c_uint),
        ]

    class RspData(ctypes.Structure):
        _fields_ = [
            ('data', ctypes.c_uint),
        ]

    @hif.req_fifo
    def req(self, t : ReqData):
        pass

    @hif.rsp_fifo
    def rsp(self) -> RspData:
        pass

# req2 = ReqRspLoopback.ReqData.from_buffer_copy(bytes(req))

async def main():
    from hdl_if.tlm import StreamRgy
    rgy = StreamRgy.inst()

    await rgy.initialize()

    ifc_name = rgy.get_interfaces()[0]
    print("ifc: %s" % ifc_name)

    ifc = ReqRspLoopback()
    await rgy.connect_if(ifc, ifc_name, False)

    req = ReqRspLoopback.ReqData()
    req.data = 0x03020100

    for _ in range(16):
        print("--> req", flush=True)
        await ifc.req(req)
        print("<-- req", flush=True)

        rsp = await ifc.rsp()
        print("rsp: %s" % str(rsp.data))
        print("done", flush=True)

        req.data += 1
    pass

def init():
    print("init", flush=True)

    backend = hif.Backend.inst()

    backend.mkTask(main())

