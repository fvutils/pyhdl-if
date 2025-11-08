import dataclasses as dc
from .component_impl import uvm_component_impl
from .object import uvm_object
from .visitor import uvm_visitor

class Output(object):
    pass

@dc.dataclass
class PyGen(uvm_component_impl):

    def __post_init__(self):
        print("__post_init__", flush=True)

    def build_phase(self, phase):
        from .wrap.object_rgy import uvm_object_rgy

        print("build_phase")

        obj_rgy = uvm_object_rgy.inst()

        print("typename_dump:\n%s" % obj_rgy._get_type_dump(), flush=True)


