import os
import sys
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import hdl_if_env

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_py_api_data_dir = os.path.join(data_dir, "py_api")

def _test_file(hdlsim_dvflow : HdlSimDvFlow, name, env, plusargs=None):
    env["PYTHONPATH"] = test_py_api_data_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim)

    sv_src = hdlsim_dvflow.mkTask("std.FileSet",
                                  base=test_py_api_data_dir,
                                  include="%s.sv" % name,
                                  type="systemVerilogSource")

    dpi_lib = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")
    sv_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")

    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                                   top=[name],
                                   needs=[sv_pkg, sv_src, dpi_lib])
    
    sim_run = hdlsim_dvflow.mkTask("hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
                                   plusargs=plusargs if plusargs is not None else [],
                                   needs=[sim_img])
    
    status, out = hdlsim_dvflow.runTask(sim_run)

    assert status == 0

    with open(os.path.join(sim_run.rundir, "status.txt"), "r") as fp:
        status = fp.read().strip()

    assert status.startswith("PASS:")


def test_smoke(hdlsim_dvflow, hdl_if_env):
    _test_file(hdlsim_dvflow, "test_smoke", env=hdl_if_env)

def test_a_plus_b(hdlsim_dvflow, hdl_if_env):
    _test_file(hdlsim_dvflow, "a_plus_b", env=hdl_if_env)

#@pytest.mark.skip("Needs more investigation")
def test_data1(hdlsim_dvflow, hdl_if_env):
    _test_file(hdlsim_dvflow, "data1", env=hdl_if_env, plusargs=[
        'data=%s' % os.path.join(test_py_api_data_dir, "data1.json")])