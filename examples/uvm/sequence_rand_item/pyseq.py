from hdl_if.uvm import uvm_sequence_impl


class PyRandSeq(uvm_sequence_impl):

    async def body(self):
        # Send a small burst of randomized items
        for i in range(8):
            req = self.proxy.create_req()
            # Backend-driven randomization of the SV sequence item
            req.randomize()

            # Optional visibility
            try:
                s = req.sprint()
            except Exception:
                s = "<no sprint available>"
            print(f"PyRandSeq: sending item {i}\n{s}", flush=True)

            val = req.pack()
            print("val: %s" % str(val))

            await self.proxy.start_item(req)
            await self.proxy.finish_item(req)
