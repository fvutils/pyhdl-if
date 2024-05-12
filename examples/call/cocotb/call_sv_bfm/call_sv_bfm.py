
import cocotb
from cocotb.triggers import Timer, RisingEdge
import ctypes as ct
import hdl_if as hif

@hif.api
class WishboneInitiator(object):

    @hif.imptask
    async def write(self, addr : ct.c_uint32, data : ct.c_uint32):
        pass

    @hif.imptask
    async def read(self, addr : ct.c_uint32) -> ct.c_uint32:
        pass

@cocotb.test()
async def entry(dut):
    print("entry")
    await Timer(0, 'ns')
    print("post-timeout")
    rgy = hif.HdlObjRgy.inst()
    init_bfm = rgy.findObj(".*\.init_bfm", regex=True)

    # Wait for reset
    clk_ev = RisingEdge(dut.clk)

    while (True):
        await clk_ev
        print("reset: %d" % dut.reset)
        if dut.reset == 0:
            break

    for i in range(64):
        await init_bfm.write(0x8000_0000+(4*i), (i+1))

    for i in range(64):
        await init_bfm.read(0x8000_0000+(4*i))

    pass
