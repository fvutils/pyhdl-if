
from hdl_if.uvm import UvmSequenceProxy

class PySeq(UvmSequenceProxy):

    async def body(self):
        print("body", flush=True)
        print("name: %s" % self.get_name(), flush=True)
