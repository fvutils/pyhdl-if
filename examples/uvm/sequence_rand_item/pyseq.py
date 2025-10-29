from hdl_if.uvm import UvmSequenceProxy


class PyRandSeq(UvmSequenceProxy):  # type: ignore
    async def body(self):
        # Send a small burst of randomized items
        for i in range(8):
            req = self.create_req()
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

            await self.start_item(req)
            await self.finish_item(req)
