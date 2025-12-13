
import os
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_dpi


data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_perf_data_dir = os.path.join(data_dir, "test_perf")


@pytest.mark.parametrize("pyhdl_dvflow", available_sims_dpi(), indirect=True)
def test_perf_py_to_sv_task(pyhdl_dvflow, hdl_if_env):
    """Performance test comparing asyncio vs asyncio.to_thread for Py->SV task calls"""
    env = hdl_if_env
    env["PYTHONPATH"] = test_perf_data_dir + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    print("test_perf_data_dir: %s" % test_perf_data_dir, flush=True)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_pkg = pyhdl_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = pyhdl_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="perf_test_pkg",
        filename="perf_test_pkg.sv",
        modules=["perf_test"],
        pythonpath=[test_perf_data_dir])

    test_sv = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=test_perf_data_dir,
                                   include=["perf_bfm.sv"],
                                   type="systemVerilogSource")

    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                        top=["perf_bfm"],
                        needs=[hdl_if_pkg, gen_api, hdl_if_dpi, test_sv],
                        elabargs=args)
    
    sim_run = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
        plusargs=["pyhdl_if_debug=0"],
        needs=[sim_img])

    status, out = pyhdl_dvflow.runTask(sim_run)

    assert status == 0

    # Print simulation log
    sim_log_path = os.path.join(out.output[0].basedir, "sim.log")
    if os.path.isfile(sim_log_path):
        print("\n" + "=" * 60)
        print("Simulation Log:")
        print("=" * 60)
        with open(sim_log_path, "r") as fp:
            print(fp.read())

    # Check performance results
    perf_results_path = os.path.join(out.output[0].basedir, "perf_results.txt")
    assert os.path.isfile(perf_results_path), "perf_results.txt not found"

    results = {}
    with open(perf_results_path, "r") as fp:
        for line in fp:
            line = line.strip()
            if "=" in line:
                key, val = line.split("=", 1)
                results[key] = val

    print("\n" + "=" * 60)
    print("Performance Results:")
    print("=" * 60)
    for key, val in results.items():
        print(f"  {key}: {val}")

    assert results.get("status") == "PASS", "Test did not pass"
    assert float(results.get("asyncio_time", 0)) > 0, "asyncio_time should be > 0"
    assert float(results.get("thread_time", 0)) > 0, "thread_time should be > 0"
