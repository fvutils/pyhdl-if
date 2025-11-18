import dataclasses as dc
from typing import Dict
from .component_impl import uvm_component_impl
from .object import uvm_object
from .visitor import uvm_visitor

class Output(object):
    pass

@dc.dataclass
class PyGen(uvm_component_impl):
    processed_types : Dict[str,object] = dc.field(default_factory=dict)

    def __post_init__(self):
        print("__post_init__", flush=True)

    def build_phase(self, phase):
        from .wrap.object_rgy import uvm_object_rgy

        print("build_phase")

        obj_rgy = uvm_object_rgy.inst()

        print("typename_dump:\n%s" % obj_rgy._get_type_dump(), flush=True)

        for n in obj_rgy.typenames:
            print("Type: %s" % n, flush=True)
            obj = obj_rgy.create_by_name(n)
            self.process_obj(obj)

    def process_obj(self, obj):
        if obj.get_type_name() in self.processed_types.keys():
            print("Already processed (%s)" % obj.get_type_name())
            return
        self.processed_types[obj.get_type_name()] = 1
        print("Processing %s" % obj.get_type_name())
        if hasattr(obj, "get_children"):
            for c in obj.get_children():
                print("Field: %s" % c.get_name())
                self.process_obj(c)






