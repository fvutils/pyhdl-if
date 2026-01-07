"""
Test the pytest runner functionality by invoking it from a simulation
"""
import os
import sys
import pytest
from . import pyhdl_dvflow, hdl_if_env, available_sims_dpi

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_pytest_runner_data_dir = os.path.join(data_dir, "test_pytest_runner")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_dpi(incl=["vlt"]), indirect=True)
def test_pytest_runner(pyhdl_dvflow, hdl_if_env):
    """Test pytest runner with simulation"""
    env = hdl_if_env
    env["PYTHONPATH"] = test_pytest_runner_data_dir + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    print("test_pytest_runner_data_dir: %s" % test_pytest_runner_data_dir, flush=True)

    hdl_if_pkg = pyhdl_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    test_sv = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=test_pytest_runner_data_dir,
                                   include=["pytest_runner_test.sv"],
                                   type="systemVerilogSource")

    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                        top=["pytest_runner_test"],
                        needs=[hdl_if_pkg, hdl_if_dpi, test_sv])

    # Pass the testpath as a plusarg
    sample_tests_path = os.path.join(test_pytest_runner_data_dir, "sample_async_tests.py")

    sim_run = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
        plusargs=["testpath=%s" % sample_tests_path],
        needs=[sim_img])

    status, out = pyhdl_dvflow.runTask(sim_run)

    print("Simulation completed with status: %d" % status, flush=True)
    
    # Check simulation log
    if os.path.isfile(os.path.join(out.output[0].basedir, "sim.log")):
        with open(os.path.join(out.output[0].basedir, "sim.log"), "r") as fp:
            log_content = fp.read()
            print("=== Simulation Log ===", flush=True)
            print(log_content, flush=True)
            
            # Verify pytest runner was invoked
            assert "[PyHDL-IF Pytest] Starting pytest runner" in log_content
            # Verify tests were collected
            assert "collected 3 items" in log_content or "test_simple_pass" in log_content
            # Verify Summary was printed
            assert "[PyHDL-IF Pytest] Test Summary:" in log_content
    
    assert status == 0, "Simulation failed"
