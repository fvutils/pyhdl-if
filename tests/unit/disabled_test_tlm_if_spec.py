

def test_param_if():
    import os
    import sys
    import vsc_dataclasses as vdc
    unit_tests_dir = os.path.dirname(os.path.abspath(__file__))
    proj_dir = os.path.abspath(os.path.join(unit_tests_dir, "../.."))
    sys.path.append(os.path.join(proj_dir, "src"))

    import vsc_dataclasses as vdc
    import hdl_tlm_if as hti

    @hti.tlm_if
    class BfmIF(object):
        P1 : int = 2
        P2 : int = 3
        P3 : int = P2
        ADDR_WIDTH : vdc.param[int] = 20

        @vdc.randclass
        class AddrWriteReq(object):
            data : vdc.bit_t[8]
            data2 : vdc.bit_t[8]
            def __init__(self):
                pass

        @vdc.randclass
        class WriteRsp(object):
            data : vdc.bit_t[32]
            pass

        @hti.req_fifo
        async def write_addr_req(self, req : AddrWriteReq):
            pass

        @hti.rsp_fifo
        async def write_rsp(self, rsp : WriteRsp):
            pass

    bfm_if = BfmIF()

    req = BfmIF.AddrWriteReq()

    print("Fields: %s" % str(req.fields()))
    print("Size: %d" % req.bitsize())

    for i in range(16):
        req.data = i
        req.data2 = i+1
        print("Value: 0x%08x" % req.intval())



