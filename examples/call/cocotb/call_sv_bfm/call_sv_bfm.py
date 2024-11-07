
import cocotb
from cocotb.triggers import Timer, RisingEdge
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

@cocotb.test()
async def entry(dut):
    print("entry")
    await Timer(1, 'ns')
    print("post-timeout")
    rgy = hif.HdlObjRgy.inst()
    init_bfm = rgy.findObj(r".*\.init_bfm", regex=True)

    # Wait for reset
    clk_ev = RisingEdge(dut.clk)

    while (True):
        await clk_ev
        print("reset: %d" % dut.reset)
        if dut.reset == 0:
            break

    for i in range(64):
        wr_val = (i+1)
        print(f'[Py] writing: {wr_val}')
        await init_bfm.write(0x8000_0000+(4*i), wr_val)
        rd = await init_bfm.read(0x8000_0000+(4*i))
        print(f'[Py] readback: {rd}')
        assert wr_val == rd

    for i in range(64):
        await init_bfm.read(0x8000_0000+(4*i))

    pass
