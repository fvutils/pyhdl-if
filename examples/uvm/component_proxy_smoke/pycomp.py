
from hdl_if.uvm import uvm_component_impl

class PyComp(uvm_component_impl):

    def build_phase(self, phase):
        print("-- build_phase", flush=True)


    def connect_phase(self, phase):
        print("-- connect_phase", flush=True)

    async def run_phase(self, phase):
        print("Hello from PyComp run_phase", flush=True)


