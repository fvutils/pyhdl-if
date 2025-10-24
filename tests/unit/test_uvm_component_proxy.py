
import os
import pytest
import hdl_if
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_uvm

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
uvm_data_dir = os.path.join(data_dir, "uvm")
uvm_comp_data_dir = os.path.join(uvm_data_dir, "component")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_uvm(), indirect=True)
def test_smoke(pyhdl_dvflow, hdl_if_env):
    env = hdl_if_env
    env["PYTHONPATH"] = os.path.join(uvm_comp_data_dir, "smoke") + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    hdl_if_uvm = pyhdl_dvflow.mkTask("pyhdl-if.UVMPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    uvm_lib = pyhdl_dvflow.mkTask("hdlsim.%s.SimLibUVM" % pyhdl_dvflow.sim)

    uvm_env = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=os.path.join(uvm_comp_data_dir, "smoke"),
                                   type="systemVerilogSource",
                                   include=["smoke_pkg.sv", "top.sv"],
                                   incdirs=["."])
    
    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                                  needs=[uvm_lib, hdl_if_uvm, hdl_if_dpi, uvm_env],
                                  top=["tb_top"])
    
    sim_run = pyhdl_dvflow.mkTask("hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
                                  needs=[sim_img],
                                  valgrind=False)
    
    status, out = pyhdl_dvflow.runTask(sim_run)

    assert status == 0

    pass
