from hdl_if.uvm import uvm_sequence_impl

class PyRegSeq(uvm_sequence_impl):

    async def body(self):
        # Obtain the register model from the sequencer
        _,spi_regs = self.proxy.m_sequencer.get_config_object("spi_regs", False)

        print("spi_regs: %s" % str(spi_regs), flush=True)

        spi_regs.CTRL.enable.set(1)
        spi_regs.CTRL.master.set(1)
        print("--> update", flush=True)
        await spi_regs.CTRL.update()
        print("<-- update", flush=True)

        print("--> write", flush=True)
        spi_regs.CLKDIV.div.set(0x4)
        print("<-- write", flush=True)
        spi_regs.SS.ss_mask.set(0x1)
        await spi_regs.CLKDIV.update()
        await spi_regs.SS.update()

        print("--> write", flush=True)
        await spi_regs.TXDATA.write(0xA5)
        print("<-- write", flush=True)

        # Wait for 
        for _ in range(100):
            await spi_regs.STATUS.read()

            if spi_regs.STATUS.tx_empty.get() == 1:
                break


