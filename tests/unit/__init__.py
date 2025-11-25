import os
import pytest
import sys

from dv_flow.libhdlsim.pytest import hdlsim_dvflow, hdlsim_available_sims, HdlSimDvFlow

def available_sims_dpi(incl=None, excl=None):
    if excl is None:
        # TODO: control via env var?
#        excl = ["xsm"]
        pass
    return hdlsim_available_sims(incl, excl)

def available_sims_vpi(incl=None, excl=None):
    if excl is None:
        # TODO: control via env var?
        excl = ["vlt", "xsm"]
    else:
        if "vlt" not in excl: excl.append("vlt")
        if "xsm" not in excl: excl.append("xsm")
    return hdlsim_available_sims(incl, excl)

def available_sims_uvm(incl=None, excl=None):
    if incl is None:
        # TODO: control via env var?
        incl = ["mti", "vcs", "xcm"]

    return hdlsim_available_sims(incl, excl)


@pytest.fixture(scope="session")
def hdl_if_env():
    unit_tests_dir = os.path.dirname(os.path.abspath(__file__))
    hdl_if_dir = os.path.abspath(
        os.path.join(unit_tests_dir, "..", "..", "src"))

    env = os.environ.copy()
    if "PYTHONPATH" not in env:
        env["PYTHONPATH"] = hdl_if_dir
    else:
        env["PYTHONPATH"] += os.pathsep + hdl_if_dir

    env["PYHDL_IF_PYTHON"] = sys.executable

    return env

@pytest.fixture
def pyhdl_dvflow(request, tmpdir):
    unit_tests_dir = os.path.dirname(os.path.abspath(__file__))
    pyhdl_if_dir = os.path.abspath(os.path.join(unit_tests_dir, "../../"))

    ret = HdlSimDvFlow(
        request=request, 
        srcdir=os.path.dirname(request.fspath),
        tmpdir=tmpdir)
    ret.addPackage("via", os.path.join(pyhdl_if_dir, "packages/via/flow.dv"))

    return ret


