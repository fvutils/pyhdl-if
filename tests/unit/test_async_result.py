import os
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_dpi


data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_async_result_data_dir = os.path.join(data_dir, "test_async_result")


@pytest.mark.parametrize("pyhdl_dvflow", available_sims_dpi(), indirect=True)
def test_async_result(pyhdl_dvflow, hdl_if_env):
    """Check that concurrent @hif.exp calls each receive their own result"""
    env = hdl_if_env
    env["PYTHONPATH"] = test_async_result_data_dir + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    print("test_async_result_data_dir: %s" % test_async_result_data_dir, flush=True)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_pkg = pyhdl_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = pyhdl_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="async_result_test_pkg",
        filename="async_result_test_pkg.sv",
        modules=["async_result_test"],
        pythonpath=[test_async_result_data_dir])

    test_sv = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=test_async_result_data_dir,
                                   include=["async_result_test.sv"],
                                   type="systemVerilogSource")

    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                        top=["async_result_test"],
                        needs=[hdl_if_pkg, gen_api, hdl_if_dpi, test_sv],
                        elabargs=args)

    sim_run = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
        needs=[sim_img])

    status, out = pyhdl_dvflow.runTask(sim_run)

    assert status == 0

    status = None

    if os.path.isfile(os.path.join(out.output[0].basedir, "sim.log")):
        print("HAVE: sim log")
        with open(os.path.join(out.output[0].basedir, "sim.log"), "r") as fp:
            print(fp.read())
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
