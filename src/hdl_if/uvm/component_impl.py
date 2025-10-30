import dataclasses as dc

from .component_proxy import uvm_component_proxy
from .phase import uvm_phase

@dc.dataclass
class uvm_component_impl(object):
    proxy : uvm_component_proxy = dc.field()

    def build_phase(self, phase : uvm_phase): ...

    def connect_phase(self, phase : uvm_phase): ...

    async def run_phase(self, phase : uvm_phase): ...

