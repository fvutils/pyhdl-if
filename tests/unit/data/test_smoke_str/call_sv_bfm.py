
import ctypes as ct
import hdl_if as hif

@hif.api
class WishboneInitiator(object):

    @hif.imp
    async def is_eq_hello(self, val : str) -> ct.c_bool:
        pass

    @hif.imp
    async def write(self, addr : ct.c_uint32, data : ct.c_uint32):
        pass

    @hif.imp
    async def read(self, addr : ct.c_uint32) -> ct.c_uint32:
        pass

@hif.api
class Test(object):

    @hif.exp
    async def run(self, bfm : ct.py_object):
        errors = 0
        print("run")

        for i in range(64):
            wr_val = (i+1)
            print(f'[Py] writing: {wr_val}')
            await bfm.write(0x8000_0000+(4*i), wr_val)
            rd = await bfm.read(0x8000_0000+(4*i))
            print(f'[Py] readback: {rd}')
            if wr_val != rd:
                errors += 1
        
        is_eq_1 = await bfm.is_eq_hello("hello")
        is_eq_2 = await bfm.is_eq_hello("goodbye")
        print("is_eq_1: %s" % is_eq_1, flush=True)
        print("is_eq_2: %s" % is_eq_2, flush=True)

        if not is_eq_1:
            errors += 1

        if is_eq_2:
            errors += 1

        with open("status.txt", "w") as fp:
            fp.write("%s: %d errors\n" % (("PASS" if errors==0 else "FAIL"), errors))

