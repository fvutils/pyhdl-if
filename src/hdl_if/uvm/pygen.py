import dataclasses as dc
import io
import logging
import os
from typing import ClassVar, Dict, List, Optional, Set, TextIO, cast

from hdl_if.uvm.component import uvm_component
from .component_impl import uvm_component_impl
from .object import uvm_object
from .visitor import uvm_visitor

@dc.dataclass
class Output(object):
    out : TextIO = dc.field()
    ind : str = dc.field(default="")
    clsnames : Set[str] = dc.field(default_factory=set)

    def println(self, msg):
        if msg != "":
            self.out.write("%s%s\n" % (self.ind, msg))
        else:
            self.out.write("\n")

    def write(self, msg):
        self.out.write(msg)

    def inc_ind(self):
        self.ind += "    "

    def dec_ind(self):
        if len(self.ind) > 4:
            self.ind = self.ind[4:]
        else:
            self.ind = ""


@dc.dataclass
class PyGen(uvm_component_impl, uvm_visitor):
    processed_types : Dict[str,object] = dc.field(default_factory=dict)
    outdir : str = dc.field(default="")
    out_s : List[Output] = dc.field(default_factory=list)
    _log : ClassVar = logging.getLogger("PyGen")

    def __post_init__(self):
        from .wrap.object_rgy import uvm_object_rgy
        obj_rgy = uvm_object_rgy.inst()
        plusargs = obj_rgy.clp().plusargs()

        level_i = 0
        for p in plusargs:
            if p.startswith("+"): p=p[1:]
            if p.startswith("pyhdl.debug="):
                level = p[len("pyhdl.debug="):]
                try:
                    level_i = int(level)
                except Exception as e:
                    print("Error: failed to process +pyhdl.debug: %s (%s)" % (level, str(e)))
            elif p.startswith("pygen.debug="):
                level = p[len("pygen.debug="):]
                try:
                    level_i = int(level)
                except Exception as e:
                    print("Error: failed to process +pygen.debug: %s (%s)" % (level, str(e)))
        if level_i:
            logging.basicConfig(level=logging.DEBUG)


    def build_phase(self, phase):
        from .wrap.object_rgy import uvm_object_rgy
        self._log.debug("--> build_phase")

        obj_rgy = uvm_object_rgy.inst()

        self.outdir = os.path.join(os.getcwd(), "pyhdl_uvm_classes")
        plusargs = obj_rgy.clp().plusargs()

        self._log.debug("plusargs: %s" % str(plusargs))
        for a in plusargs:
            if a.startswith("+"): a = a[1:]
            if a.startswith("pyhdl.outdir="):
                outdir = a[len("pyhdl.outdir="):]
                if not os.path.isabs(outdir):
                    outdir = os.path.abspath(outdir)
                self.outdir = outdir
        self._log.debug("outdir: %s" % self.outdir) 


        self._log.debug("typename_dump:\n%s" % obj_rgy._get_type_dump())

        os.makedirs(self.outdir, exist_ok=True)

        # Create a generic root module
        with open(os.path.join(self.outdir, "__init__.py"), "w") as fp:
            fp.write("""
import importlib
import os

pkg_dir = os.path.dirname(os.path.abspath(__file__))

for f in os.listdir(pkg_dir):
    if f.endswith(".py") and f != "__init__.py":
        base = f[:-3]
        importlib.import_module(f".{base}", package=__name__)
            """)

        for n in obj_rgy.typenames:
            self._log.debug("Type: %s" % n)
            if n in self.processed_types.keys():
                self._log.debug("Type %s already processed" % n)
                continue
            obj = obj_rgy.create_by_name(n)
            self.process_obj(obj)

        self._log.debug("<-- build_phase")

    def process_obj(self, obj):
        if obj.get_type_name() in self.processed_types.keys():
            print("Already processed (%s)" % obj.get_type_name())
            return
        self.processed_types[obj.get_type_name()] = 1
        print("Processing %s" % obj.get_type_name())
        obj.accept(self)

    def visit_component(self, obj: uvm_component) -> None:
        self._log.debug("--> visit_component %s (%s)" % (obj.get_name(), obj.get_type_name()))
        if (obj.get_type_name().startswith("uvm_")):
            self._log.debug("<-- visit_component -- skip because is a uvm_ type")
            return
        if len(self.out_s):
            self.out_s[-1].clsnames.add(obj.get_type_name())
        
        fp = open(os.path.join(self.outdir, "%s.py" % obj.get_type_name()), "w")
        out = Output(fp)
        self.out_s.append(out)
        out.println("from __future__ import annotations")
        out.println("import dataclasses as dc")
        out.println("import typing")
        out.println("from hdl_if.uvm import uvm_component")
        out.println("")

        out_c = Output(io.StringIO())
        self.out_s.append(out_c)
        base = self._gen_field_decl(obj)

        out_c.println("@dc.dataclass(kw_only=True)")
        out_c.println("class %s(uvm_component%s):" % (obj.get_type_name(), base))
        new_types : Dict[str,uvm_object] = {}

        added = False
        out_c.inc_ind()
        for c in obj.get_children():
            self._log.debug("Child: %s : %s" % (c.get_name(), c.get_type_name()))
            if not c.get_type_name().startswith("uvm_"):
                out_c.println("    %s : typing.Optional[%s] = dc.field(default=None)" % (c.get_name(), c.get_type_name()))
                added = True
                tname = c.get_type_name()
                if tname not in self.processed_types.keys() and tname not in new_types.keys():
                    new_types[tname] = c
        if not added:
            out_c.println("pass")
        out_c.dec_ind()
        
        for name,c in new_types.items():
            from .wrap.object_rgy import uvm_object_rgy
            obj_rgy = uvm_object_rgy.inst()

            # We have an object, but it probably hasn't bee
            # properly constructed. Create it explicitly
            # TODO: maybe skip this if we're working with registers?
            obj = obj_rgy.create_by_name(name)
            self.process_obj(obj)

        self.out_s.pop()
        # Need to add classes gathered by out_c
        if len(out_c.clsnames):
            out.println("if typing.TYPE_CHECKING:")
            out.inc_ind()
            for c in out_c.clsnames:
                out.println("from .%s import %s" % (c, c))
            out.dec_ind()
            out.println("")

        out.out.write(cast(io.StringIO,out_c.out).getvalue())
        out.out.close()
        self.out_s.pop()

    def visit_object(self, obj: uvm_object) -> None:
        if (obj.get_type_name().startswith("uvm_")):
            return
        if len(self.out_s):
            self.out_s[-1].clsnames.add(obj.get_type_name())

        fp = open(os.path.join(self.outdir, "%s.py" % obj.get_type_name()), "w")
        out = Output(fp)
        self.out_s.append(out)
        out.println("from __future__ import annotations")
        out.println("import dataclasses as dc")
        out.println("import typing")
        out.println("from hdl_if.uvm import uvm_object")
        out.println("")

        out_c = Output(io.StringIO())
        self.out_s.append(out_c)

        base = self._gen_fields(obj)

        out_c.println("@dc.dataclass")
        out_c.println("class %s(uvm_object%s):" % (obj.get_type_name(), base))
        out_c.inc_ind()
        out_c.println("pass")
        out_c.dec_ind()

        self.out_s.pop()

        out.out.write(cast(io.StringIO,out_c.out).getvalue())
        self.out_s.pop()
        out.out.close()


    def _gen_fields(self, obj):
        out = self.out_s[-1]

        val = obj.pack()
        # Get the value object
        fields = dc.fields(val)
        if len(fields) > 0:
            clsname = "%s_fields" % obj.get_type_name()
            base = ", %s" % clsname

            out.println("")
            out.println("@dc.dataclass(kw_only=True)")
            out.println("class %s(object):" % clsname)
            out.inc_ind()
            for f in fields:
                out.println("%s" % self._gen_field_decl(f))
            out.dec_ind()
            out.println("")
        else:
            base = ""

        return base

#        out.println("")
#        out.println("    def pack(self) -> Fields: ...")
#        out.println("")
#        out.println("    def unpack(self, val : Fields): ...")
#        out.println("")
    
    def _gen_field_decl(self, f : dc.Field) -> str:

        if f.type == int:
            tname = "int"
            value = "0"
        else:
            raise Exception("Unsupported type %s" % str(f.type))

        return "%s : %s = dc.field(default=%s)" % (f.name, tname, value)

        







