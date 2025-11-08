from hdl_if.uvm import uvm_component_impl

class PyReseed(uvm_component_impl):
    def build_phase(self, phase):
        has, obj = self.proxy.get_config_object("MY_CONFIG")
        assert has, "Expected MY_CONFIG object from config DB"

        # Deterministic across reseed() + randomize() cycles
        obj.reseed()
        obj.randomize()
        s1 = obj.sprint()

        obj.reseed()
        obj.randomize()
        s2 = obj.sprint()

        print("s1:", s1, flush=True)
        print("s2:", s2, flush=True)
        assert s1 == s2, "Reseed should produce deterministic randomized state"

    def connect_phase(self, phase):
        pass

    async def run_phase(self, phase):
        pass
