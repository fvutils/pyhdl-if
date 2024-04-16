import asyncio
import ctypes
import io
import os
import pytest
import sys

tests_unit_dir = os.path.dirname(os.path.abspath(__file__))
proj_src_dir = os.path.abspath(os.path.join(tests_unit_dir, "../../src"))
print("proj_src_dir: %s" % proj_src_dir)
sys.path.insert(0, proj_src_dir)

import hdl_call_if as hci

@pytest.fixture
def decorator_init():
    from hdl_call_if.impl.ctor import Ctor
    from hdl_call_if.impl.api_def_rgy import ApiDefRgy
    print("setup")
    Ctor.init()
    ApiDefRgy.init()
    yield 1
    print("teardown")
    Ctor.init()
    ApiDefRgy.init()

    pass

def test_single_api(decorator_init):
    from hdl_call_if.impl.api_def_rgy import ApiDefRgy

    @hci.api
    class API(object):

        def __init__(self, a : ctypes.c_int, b : ctypes.c_int):
            pass

        @hci.impfunc
        def callout(self, 
                    a : ctypes.c_int, 
                    b : ctypes.c_int, 
                    c : ctypes.c_int):
            pass

        @hci.imptask
        async def callout_t(self, a : ctypes.c_int):
            pass


#    a = API()
#    a.callout(1, 2, 3)
#    asyncio.new_event_loop().run_until_complete(a.callout_t(2))

    rgy = ApiDefRgy.inst()
    apis = rgy.getApis()
    assert len(apis) == 1
    assert apis[0].name == "API"
    assert len(apis[0].methods) == 2

    from hdl_call_if.impl.gen_sv_class import GenSVClass
    out = io.StringIO()
    gen = GenSVClass(out)
    gen.gen(apis[0])

    print("Result:\n%s\n" % out.getvalue())

