import io
import pytest
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
import os
import sys

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from hdl_if.decorators import api, exp, imp
from hdl_if.impl.call.api_def_rgy import ApiDefRgy
from hdl_if.impl.call.ctor import Ctor
from hdl_if.impl.call.gen_sv_class import GenSVClass
from . import available_sims_dpi, hdl_if_env


def _emit_sv_for(cls) -> str:
    fullname = cls.__module__ + "." + cls.__qualname__
    ad = next(a for a in ApiDefRgy.inst().getApis() if a.fullname == fullname)
    out = io.StringIO()
    GenSVClass(out, ind="", uvm=False).gen(ad)
    return out.getvalue()


def test_union_methods_across_inheritance():
    # Reset registries before defining API classes
    ApiDefRgy.init()
    Ctor.init()

    @api
    class Base:
        def __init__(self):
            pass

        @exp
        def base_only_exp(self, a: int) -> int:
            return a

        @imp
        def base_imp(self, a: int) -> int:
            # Implementation body is unused by GenSVClass generation
            return a + 1

    @api
    class Derived(Base):
        def __init__(self):
            super().__init__()

        @exp
        def derived_only_exp(self, b: int) -> int:
            return b

    sv = _emit_sv_for(Derived)

    # Extract interface block
    iface_hdr = f"interface class I{Derived.__name__} extends pyhdl_if::ICallApi;"
    assert iface_hdr in sv
    iface_start = sv.index(iface_hdr)
    iface_end = sv.index("endclass", iface_start)
    iface_block = sv[iface_start:iface_end]

    # Interface must declare both base and derived exp methods
    assert "base_only_exp(" in iface_block
    assert "derived_only_exp(" in iface_block

    # Func-dispatch appears in both creator and wrapper; expect two occurrences
    assert sv.count('"%s": begin' % "base_imp") == 2


def test_override_masks_base():
    ApiDefRgy.init()
    Ctor.init()

    @api
    class Base2:
        def __init__(self):
            pass

        @exp
        def foo(self, x: int) -> int:
            return x

    @api
    class Derived2(Base2):
        def __init__(self):
            super().__init__()

        # Override base exp method; union should keep derived version only
        @exp
        def foo(self, x: int) -> int:
            return x + 1

        @imp
        def drv_imp(self, y: int) -> int:
            return y - 1

    sv = _emit_sv_for(Derived2)

    iface_hdr = f"interface class I{Derived2.__name__} extends pyhdl_if::ICallApi;"
    assert iface_hdr in sv
    iface_start = sv.index(iface_hdr)
    iface_end = sv.index("endclass", iface_start)
    iface_block = sv[iface_start:iface_end]

    # Only one declaration of foo in the interface
    assert iface_block.count("foo(") == 1

    # Func-dispatch appears in both creator and wrapper; expect two occurrences
    assert sv.count('"%s": begin' % "drv_imp") == 2
