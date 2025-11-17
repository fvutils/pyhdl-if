
from hdl_if.uvm import uvm_component_impl

class PyComp(uvm_component_impl):

    def build_phase(self, phase):
        print("build_phase", flush=True)
        env = self.proxy.get_parent()
        env.prod.ap_a.proxy.add_listener(self.write_a)
        env.ap_b_proxy.proxy.add_listener(self.write_b)

    def write_a(self, t):
        print("write_a %0s" % str(t), flush=True)

    def write_b(self, t):
        print("write_b %0s" % str(t), flush=True)

