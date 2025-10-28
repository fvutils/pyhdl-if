
from hdl_if.uvm import UvmComponentProxy, UvmObjectRgy

class PyComp(UvmComponentProxy):

    def build_phase(self, phase):
        print("-- build_phase", flush=True)
        inst = UvmObjectRgy.inst()

        print("--> typenames", flush=True)
        inst.typenames
        print("<-- typenames", flush=True)


    def connect_phase(self, phase):
        print("-- connect_phase", flush=True)

    async def run_phase(self, phase):
        print("Hello from PyComp run_phase", flush=True)


