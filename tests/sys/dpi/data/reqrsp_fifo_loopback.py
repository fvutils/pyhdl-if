
import traceback
import hdl_tlm_if as hti
import vsc_dataclasses as vdc

@hti.tlm_if
class reqrsp_fifo(object):

    @vdc.randclass
    class Req(object):
        data : vdc.bit_t[8]
        data2 : vdc.bit_t[8]

    @vdc.randclass
    class Rsp(object):
        data : vdc.bit_t[8]
        data2 : vdc.bit_t[8]

    @hti.req_fifo
    async def req(self, req : Req):
        pass

    @hti.rsp_fifo
    async def rsp(self, rsp : Rsp):
        pass

evt = None
def callback():
    global evt
    print("callback", flush=True)
    evt.set()

# Test entry-point
async def run():
    global evt
    from hdl_pi_if.hdl_services import HdlServices
    from hdl_pi_if.backend import Backend

    print("run", flush=True)
    reqrsp_if = reqrsp_fifo()

    await hti.initialize()

    ifcs = hti.get_interfaces()

    print("ifcs: %s" % str(ifcs), flush=True)

    try:
        services = HdlServices.inst()
        services.registerTimeCB(callback, 0)

        be = Backend.inst()
        evt = be.mkEvent()

        print("--> waiting", flush=True)
        await evt.wait()
        print("<-- waiting", flush=True)
        
        await hti.connect_if(reqrsp_if, ifcs[0], False)

    except Exception as e:
        print("Exception: %s" % str(e), flush=True)
        traceback.print_exc()


    try:
        for i in range(20):
            req = reqrsp_fifo.Req()
            req.data = i;
            req.data2 = i+1;
            await reqrsp_if.req(req)
            rsp = reqrsp_fifo.Rsp()
            await reqrsp_if.rsp(rsp)
            print("rsp: data=%08x data2=%08x" % (rsp.data, rsp.data2))

    except Exception as e:
        print("Exception: %s" % str(e))
        traceback.print_exc()


