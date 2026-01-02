import os
import sys
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import HdlSimDvFlow
from . import hdl_if_env, available_sims_vpi

print("path: %s" % str(sys.path))

import hdl_if

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_vpi_py_if_data_dir = os.path.join(data_dir, "vpi_py_if")

SKIP_HDLSIM = ('xsm', 'vlt')


@pytest.mark.parametrize("hdlsim_dvflow", available_sims_vpi(excl=["vcs"]), indirect=True)
def test_smoke(hdlsim_dvflow : HdlSimDvFlow, hdl_if_env):
    hdlsim_dvflow.setEnv(hdl_if_env)

    vpi_py_if_smoke = hdlsim_dvflow.mkTask("std.FileSet",
        base=test_vpi_py_if_data_dir,
        include=["vpi_py_if_smoke.v"],
        type="verilogSource")
    
    vpi_lib = hdlsim_dvflow.mkTask("pyhdl-if.VpiLib")

    sim_img = hdlsim_dvflow.mkTask(
        "hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
        needs=[vpi_py_if_smoke, vpi_lib],
        top=["vpi_py_if_smoke"])
    
    sim_run = hdlsim_dvflow.mkTask(
        "hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
        needs=[sim_img])
    
    status, out = hdlsim_dvflow.runTask(sim_run)

    assert status == 0
