import os
import pytest
from . import pyhdl_dvflow, hdl_if_env, available_sims_uvm

# Data directories
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data", "uvm", "component", "smoke")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_uvm(excl=('vlt')), indirect=True)
def test_smoke(pyhdl_dvflow, hdl_if_env):
    env = hdl_if_env
    env["PYTHONPATH"] = DATA_DIR + os.pathsep + env.get("PYTHONPATH", "")
    pyhdl_dvflow.setEnv(env)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    # Build prerequisites
    hdl_if_uvm = pyhdl_dvflow.mkTask("pyhdl-if.UVMPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    # UVM library for the selected simulator
    uvm_lib = pyhdl_dvflow.mkTask("hdlsim.%s.SimLibUVM" % pyhdl_dvflow.sim)

    # UVM env fileset
    uvm_env = pyhdl_dvflow.mkTask(
        "std.FileSet",
        base=DATA_DIR,
        type="systemVerilogSource",
        include=["smoke_pkg.sv", "top.sv"],
        incdirs=["."]
    )

    # Create sim image and run
    sim_img = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
        needs=[uvm_lib, hdl_if_uvm, hdl_if_dpi, uvm_env],
        top=["tb_top"],
        elabargs=args)

    sim_run = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
        needs=[sim_img],
        valgrind=False,
    )

    status, out = pyhdl_dvflow.runTask(sim_run)

    assert status == 0
