
from hdl_if.uvm import UvmComponentProxy


class PyComp(UvmComponentProxy):

    def __init__(self):
        print("PyComp", flush=True)

    def build_phase(self, phase):
        print("build_phase", flush=True)
        parent = self.get_parent()
        print("parent: %s" % parent.get_name());
        for c in parent.get_children():
            print("Child: %s" % c.get_full_name(), flush=True)

    def connect_phase(self, phase):
        print("connect_phase", flush=True)

    async def run_phase(self, phase):
        print("run_phase", flush=True)

    pass