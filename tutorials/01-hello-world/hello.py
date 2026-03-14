# hello.py — Python UVM component
#
# This class is instantiated by pyhdl_uvm_component_proxy when the
# simulation starts.  The proxy calls each UVM phase method in turn,
# just as it would for any other UVM component.

from hdl_if.uvm import uvm_component_impl


class HelloComp(uvm_component_impl):

    def build_phase(self, phase):
        print("HelloComp: build_phase", flush=True)

    def connect_phase(self, phase):
        print("HelloComp: connect_phase", flush=True)

    async def run_phase(self, phase):
        # run_phase is a UVM task, so the Python implementation must be
        # an async method.  Any code here runs inside the asyncio event
        # loop that PyHDL-IF embeds in the simulator's time-step scheduler.
        print("Hello, World! from Python inside UVM run_phase", flush=True)
