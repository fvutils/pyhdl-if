
from hdl_if.uvm import uvm_sequence_impl

class PySeq(uvm_sequence_impl):

    async def body(self):
        print("body", flush=True)
        req = self.proxy.create_req()
        req.randomize()
        await self.proxy.start_item(req)
        await self.proxy.finish_item(req)
