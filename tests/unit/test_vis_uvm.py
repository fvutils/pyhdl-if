import os
import sys
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import hdl_if_env, available_sims_dpi, pyhdl_dvflow

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_vis_uvm_data_dir = os.path.join(data_dir, "vis_uvm")

def vis_uvm_sims():
    return available_sims_dpi(excl=["vlt"])

@pytest.mark.parametrize("pyhdl_dvflow", vis_uvm_sims(), indirect=True)
def test_smoke(pyhdl_dvflow : HdlSimDvFlow, hdl_if_env):

    hdlsim_dvflow = pyhdl_dvflow

    test_sv = hdlsim_dvflow.mkTask("std.FileSet",
                                   base=os.path.join(test_vis_uvm_data_dir, "smoke"),
                                   type="systemVerilogSource",
                                   include=["smoke_pkg.sv", "smoke.sv"])
    uvm = hdlsim_dvflow.mkTask("hdlsim.%s.SimLibUVM" % hdlsim_dvflow.sim)
    pyhdl_if = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    pyhdl_if_dpi = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")
    via = hdlsim_dvflow.mkTask("via.Pkg")
    via_uvm = hdlsim_dvflow.mkTask("via.UVMPkg")
    pyvia = hdlsim_dvflow.mkTask("pyhdl-if.VIAPkg", needs=[uvm])

    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                                   needs=[pyhdl_if, uvm, via, via_uvm, pyvia, test_sv, pyhdl_if_dpi],
                                   top=["smoke"])
    
    sim_run = hdlsim_dvflow.mkTask("hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
                                   needs=[sim_img],
                                   plusargs=["pyhdl.via.class=foobar"])
    
    status, out = hdlsim_dvflow.runTask(sim_run)

    assert status == 0




