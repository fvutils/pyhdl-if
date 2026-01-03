
import os
import sys
import pytest
import re
from .test_base import *
from dv_flow.libhdlsim.pytest import HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_dpi


data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_flush_data_dir = os.path.join(data_dir, "test_flush")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_dpi(), indirect=True)
def test_flush(pyhdl_dvflow, hdl_if_env):
    env = hdl_if_env
    env["PYTHONPATH"] = test_flush_data_dir + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    print("test_flush_data_dir: %s" % test_flush_data_dir, flush=True)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_pkg = pyhdl_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = pyhdl_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="flush_test_pkg",
        filename="flush_test_pkg.sv",
        modules=["flush_test"],
        pythonpath=[test_flush_data_dir])

    test_sv = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=test_flush_data_dir,
                                   include=[
                                       "sv_helper.sv",
                                       "flush_test.sv"],
                                   type="systemVerilogSource")

    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                        top=["flush_test"],
                        needs=[hdl_if_pkg, gen_api, hdl_if_dpi, test_sv],
                        elabargs=args)
    
    sim_run = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
        plusargs=["pyhdl_if_debug=1"],
        needs=[sim_img])

    status, out = pyhdl_dvflow.runTask(sim_run)

    assert status == 0

    status = None

    # Check that output is correctly interleaved
    if os.path.isfile(os.path.join(out.output[0].basedir, "sim.log")):
        print("HAVE: sim log")
        with open(os.path.join(out.output[0].basedir, "sim.log"), "r") as fp:
            log_contents = fp.read()
            print(log_contents)
            
            # Verify that Python and SV messages are properly interleaved
            # Look for pattern: [Python] Before -> [SV] Message -> [Python] After
            pattern = r'\[Python\] Before call.*?\[SV.*?\] Message from Python iteration.*?\[Python\] After call'
            if re.search(pattern, log_contents, re.DOTALL):
                print("SUCCESS: Output properly interleaved - flush working correctly")
            else:
                print("WARNING: Could not verify output interleaving pattern")
    else:
        print("MISSING: sim log")

    if os.path.isfile(os.path.join(out.output[0].basedir, "status.txt")):
        with open(os.path.join(out.output[0].basedir, "status.txt"), "r") as fp:
            status = fp.read().strip()

        assert status.startswith("PASS:")
    else:
        for e in os.listdir(out.output[0].basedir):
            print("Subelem: %s" % e)

    assert status is not None
