import os
import pytest
import hdl_if
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_uvm

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
uvm_data_dir = os.path.join(data_dir, "uvm")
object_string_data_dir = os.path.join(uvm_data_dir, "object_string")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_uvm(excl=('vlt')), indirect=True)
def test_uvm_object_string(pyhdl_dvflow, hdl_if_env):
    """
    Test the uvm_object_string functionality in a simulation environment.
    
    This test runs a UVM simulation that:
    1. Creates a uvm_object_string instance
    2. Sets and gets string values
    3. Tests various string content (special chars, multiline, etc.)
    4. Tests integration with uvm_object_list
    5. Tests integration with uvm_object_map
    """
    env = hdl_if_env
    env["PYTHONPATH"] = os.path.join(object_string_data_dir) + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_uvm = pyhdl_dvflow.mkTask("pyhdl-if.UVMPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    uvm_lib = pyhdl_dvflow.mkTask("hdlsim.%s.SimLibUVM" % pyhdl_dvflow.sim)

    uvm_env = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=os.path.join(object_string_data_dir),
                                   type="systemVerilogSource",
                                   include=["object_string_test_pkg.sv", "top.sv"],
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

    # Check that the object string test passed
    assert "All uvm_object_string tests passed!" in simlog, "Object string test did not pass"
    
    # Verify key operations
    assert "Created uvm_object_string" in simlog, "Failed to create uvm_object_string"
    assert "Set and retrieved value" in simlog, "Failed to set/get value"
    assert "Updated and retrieved value" in simlog, "Failed to update value"
    assert "Verified empty string default" in simlog, "Empty string test failed"
    assert "Successfully tested" in simlog and "different string values" in simlog, "String variety test failed"
    assert "Successfully used uvm_object_string in a list" in simlog, "List integration failed"
    assert "Successfully used uvm_object_string in a map" in simlog, "Map integration failed"
    assert "All __str__ and __repr__ tests passed!" in simlog, "__str__ and __repr__ tests failed"

    pass
