import os
import pytest
from dv_flow.libhdlsim.pytest import HdlSimDvFlow, hdlsim_available_sims

def available_sims_dpi(incl=None, excl=None):
    if excl is None:
        # TODO: control via env var?
        excl = ["xsm"]
    return hdlsim_available_sims(incl, excl)

def available_sims_vpi(incl=None, excl=None):
    if excl is None:
        # TODO: control via env var?
        excl = ["vlt", "xsm"]
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

    return env


