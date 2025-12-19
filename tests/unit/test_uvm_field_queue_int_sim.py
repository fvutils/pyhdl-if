import os
import pytest
import hdl_if
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_uvm

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
uvm_data_dir = os.path.join(data_dir, "uvm")
queue_int_data_dir = os.path.join(uvm_data_dir, "queue_int")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_uvm(excl=('vlt')), indirect=True)
def test_uvm_field_queue_int_sim(pyhdl_dvflow, hdl_if_env):
    """
    Test the uvm_field_queue_int pack/unpack functionality in a simulation environment.
    
    This test runs a UVM simulation that:
    1. Creates UVM objects with queue_int fields
    2. Packs objects with various queue configurations (empty, single, multiple)
    3. Unpacks the packed data into new objects
    4. Verifies that all queue data is preserved correctly through pack/unpack
    5. Tests with different queue element sizes (8-bit, 16-bit, signed)
    """
    env = hdl_if_env
    env["PYTHONPATH"] = os.path.join(queue_int_data_dir) + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_uvm = pyhdl_dvflow.mkTask("pyhdl-if.UVMPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    uvm_lib = pyhdl_dvflow.mkTask("hdlsim.%s.SimLibUVM" % pyhdl_dvflow.sim)

    uvm_env = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=os.path.join(queue_int_data_dir),
                                   type="systemVerilogSource",
                                   include=["queue_int_test_pkg.sv", "top.sv"],
                                   incdirs=["."])
    
    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                                  needs=[uvm_lib, hdl_if_uvm, hdl_if_dpi, uvm_env],
                                  top=["tb_top"],
                                  elabargs=args)
    
    sim_run = pyhdl_dvflow.mkTask("hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
                                  needs=[sim_img],
                                  valgrind=False)
    
    status, out = pyhdl_dvflow.runTask(sim_run)

    assert len(out.output) == 1

    with open(os.path.join(out.output[0].basedir, "sim.log"), "r") as fp:
        simlog = fp.read()

    print("simlog:\n%s" % simlog)

    # Verify simulation completed successfully
    assert status == 0, f"Simulation failed with status {status}"

    # Check that the queue int test passed
    assert "All uvm_field_queue_int pack/unpack tests passed!" in simlog, "Queue int test did not pass"
    
    # Verify key operations for each test case
    assert "Test 1: Basic pack/unpack (empty queues)" in simlog, "Test 1 not found"
    assert "Test 2: Copy then pack/unpack" in simlog, "Test 2 not found"
    assert "Test 3: Multiple pack/unpack cycles" in simlog, "Test 3 not found"
    assert "Test 4: Compare objects" in simlog, "Test 4 not found"
    assert "Test 5: Randomize then pack/unpack" in simlog, "Test 5 not found"
    
    # Ensure no 'Invalid size for field' errors
    assert "Invalid size for field" not in simlog, "Found 'Invalid size for field' error in simulation log"

    pass
