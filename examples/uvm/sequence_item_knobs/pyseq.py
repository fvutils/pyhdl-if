from hdl_if.uvm import uvm_sequence_impl


class PyRandSeq(uvm_sequence_impl):  # type: ignore
    async def body(self):
        # Send a small burst of fully-randomized items
        for i in range(8):
            req = self.proxy.create_req()

            req.randomize()

            print("Sending: %s" % req.sprint(), flush=True)
            await self.proxy.start_item(req)
            await self.proxy.finish_item(req)

        # Now, exercise each page in turn 
        for i in range(4):
            req = self.proxy.create_req()
            
            # Get the current values
            val = req.pack()
            val.ctrl_addr_page = 1
            val.addr_page = i

            # Set the field values
            req.unpack(val)

            # Randomize with control knobs
            req.randomize()

            print("Page: %d - Sending: %s" % (i, req.sprint()), flush=True)

            await self.proxy.start_item(req)
            await self.proxy.finish_item(req)
