
from hdl_if.uvm import uvm_component_impl


class PyComp(uvm_component_impl):

    def build_phase(self, phase):
        print("build_phase", flush=True)
        parent = self.proxy.get_parent()
        print("parent: %s" % parent.get_name());
        for c in parent.get_children():
            print("Child: %s" % c.get_full_name(), flush=True)

        print("--> get_config", flush=True)
        has, obj = self.proxy.get_config_object("MY_CONFIG")
        print("<-- get_config", flush=True)

        print("type: %s" % getattr(obj, "obj_t", "<notset>"), flush=True)

    def connect_phase(self, phase):
        print("connect_phase", flush=True)

    async def run_phase(self, phase):
        print("run_phase", flush=True)

    pass