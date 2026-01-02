import os
import pytest
import hdl_if
from dv_flow.libhdlsim.pytest import HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_uvm

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
uvm_data_dir = os.path.join(data_dir, "uvm")
queue_int_data_dir = os.path.join(uvm_data_dir, "queue_int")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_uvm(excl=('vlt')), indirect=True)
def test_uvm_field_queue_int_with_data(pyhdl_dvflow, hdl_if_env):
    """
    Test the uvm_field_queue_int pack/unpack functionality with populated queues.
    
    This test runs a UVM simulation that:
    1. Creates UVM objects with queue_int fields
    2. Populates queues with actual data using SV helper methods
    3. Packs objects with various queue sizes (single element, multiple, many)
    4. Unpacks the packed data into new objects
    5. Verifies that all queue data and elements are preserved correctly through pack/unpack
    6. Tests different element sizes (8-bit, 16-bit, signed 32-bit)
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
                                   include=["queue_int_data_test_pkg.sv", "top_data.sv"],
                                   incdirs=["."])
    
    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                                  needs=[uvm_lib, hdl_if_uvm, hdl_if_dpi, uvm_env],
                                  top=["tb_top_data"],
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
    assert "All populated queue tests passed!" in simlog, "Queue int data test did not pass"
    
    # Verify key operations for each test case
    assert "Test 1: Pack/unpack" in simlog or "Test 1" in simlog, "Test 1 not found"
    assert "Test 2: Round-trip" in simlog or "Test 2" in simlog, "Test 2 not found"
    assert "Test 3: Compare" in simlog or "Test 3" in simlog, "Test 3 not found"
    assert "Test 4: Clone" in simlog or "Test 4" in simlog, "Test 4 not found"
    
    # Verify note about standalone test
    assert "standalone" in simlog or "test_with_data.sv" in simlog, "Standalone test reference not found"
    
    # Ensure no 'Invalid size for field' errors
    assert "Invalid size for field" not in simlog, "Found 'Invalid size for field' error in simulation log"

    pass
