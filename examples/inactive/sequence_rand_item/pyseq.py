from hdl_if.uvm import uvm_sequence_impl


class PyRandSeq(uvm_sequence_impl):

    async def body(self):
        # Send a small burst of randomized items
        for i in range(8):
            req = self.proxy.create_req()

            await self.proxy.start_item(req)
            # Backend-driven randomization of the SV sequence item
            req.randomize()

            vals = req.pack()
            print("Addr: 0x%08x" % req.addr, flush=True)

            await self.proxy.finish_item(req)
