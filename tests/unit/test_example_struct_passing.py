import os
import sys
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_dpi


examples_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../../examples")

struct_passing_example_dir = os.path.join(examples_dir, "call/dpi/struct_passing")


@pytest.mark.parametrize("pyhdl_dvflow", available_sims_dpi(), indirect=True)
def test_struct_passing_example(pyhdl_dvflow, hdl_if_env):
    """Test the struct_passing example runs successfully"""
    env = hdl_if_env
    env["PYTHONPATH"] = struct_passing_example_dir + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    print("struct_passing_example_dir: %s" % struct_passing_example_dir, flush=True)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_pkg = pyhdl_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = pyhdl_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="struct_passing_pkg",
        filename="struct_passing_pkg.sv",
        modules=["struct_passing"],
        pythonpath=[struct_passing_example_dir])

    example_sv = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=struct_passing_example_dir,
                                   include=["struct_passing.sv"],
                                   type="systemVerilogSource")

    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                        top=["struct_passing"],
                        needs=[hdl_if_pkg, gen_api, hdl_if_dpi, example_sv],
                        elabargs=args)
    
    sim_run = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
        needs=[sim_img])
    
    status, out = pyhdl_dvflow.runTask(sim_run)
    
    assert status == 0, "Simulation failed"
    
    # Check the simulation log for success message
    sim_log = os.path.join(out.output[0].basedir, "sim.log")
    assert os.path.isfile(sim_log), f"sim.log not found at {sim_log}"
    
    with open(sim_log) as f:
        log_content = f.read()
        print("Simulation output:", flush=True)
        print(log_content)
        assert "All Tests Passed!" in log_content, "Test did not complete successfully"
        assert "Test completed successfully" in log_content, "SV side did not complete successfully"
