
import os
import sys
import pytest

@pytest.fixture
def init_test():
    import vsc_dataclasses as vdc
    unit_tests_dir = os.path.dirname(os.path.abspath(__file__))
    proj_dir = os.path.abspath(os.path.join(unit_tests_dir, "../.."))
    proj_src_dir = os.path.join(proj_dir, "src")
    if proj_src_dir not in sys.path:
        sys.path.append(proj_src_dir)
    yield 5

    # TODO: cleanup

def test_smoke(init_test):
    import hdl_tlm_if as hti
    from hdl_tlm_if.impl.gen_ifc_sv import GenIfcSv
    from hdl_tlm_if.tlm_ifc import TlmIfc
    import vsc_dataclasses as vdc
    import hdl_tlm_if as hti

    @hti.tlm_if
    class TwoChannelIF(object):

        @vdc.randclass
        class Req(object):
            data : vdc.bit_t[8]
            data2 : vdc.bit_t[8]

        @vdc.randclass
        class Rsp(object):
            data : vdc.bit_t[12]
            data2 : vdc.bit_t[20]

        @hti.req_fifo
        async def req(self, pkt : Req):
            pass

        @hti.rsp_fifo
        async def rsp(self, pkt : Rsp):
            pass

    ti = TlmIfc.get(TwoChannelIF)
    print("ti: %s" % str(ti))

    gen = GenIfcSv()
    gen.gen_ifc_module(ti, sys.stdout)
    

