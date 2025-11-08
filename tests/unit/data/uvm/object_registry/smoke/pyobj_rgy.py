from hdl_if.uvm import uvm_component_impl
from hdl_if.uvm.wrap.object_rgy import UvmObjectRgy

class PyObjRgyTest(uvm_component_impl):

    def build_phase(self, phase):
        print("build_phase: Testing UVM Object Registry", flush=True)
        
        # Get the object registry instance
        rgy = UvmObjectRgy.inst()
        
        # Get the list of available UVM type names
        typenames = rgy.typenames
        
        print(f"Found {len(typenames)} UVM types:", flush=True)
        for typename in typenames:
            print(f"  - {typename}", flush=True)
        
        # Verify we have some expected UVM types and filtered out pyhdl_ types
        expected_types = ['uvm_test', 'uvm_component', 'uvm_object']
        found_expected = []
        found_pyhdl = []
        
        for typename in typenames:
            if typename in expected_types:
                found_expected.append(typename)
            if typename.startswith('pyhdl_'):
                found_pyhdl.append(typename)
        
        print(f"Found expected UVM types: {found_expected}", flush=True)
        print(f"Found pyhdl_ types (should be empty): {found_pyhdl}", flush=True)
        
        # Verify filtering worked correctly
        assert len(found_pyhdl) == 0, f"pyhdl_ types should be filtered out, but found: {found_pyhdl}"
        print("✅ Object registry filtering test passed!", flush=True)

    def connect_phase(self, phase):
        print("connect_phase", flush=True)

    async def run_phase(self, phase):
        print("run_phase", flush=True)
