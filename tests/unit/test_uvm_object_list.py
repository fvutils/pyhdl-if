import os
import pytest
import hdl_if
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_uvm

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
uvm_data_dir = os.path.join(data_dir, "uvm")
object_list_data_dir = os.path.join(uvm_data_dir, "object_list")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_uvm(excl=('vlt')), indirect=True)
def test_uvm_object_list(pyhdl_dvflow, hdl_if_env):
    """
    Test the uvm_object_list functionality in a simulation environment.
    
    This test runs a UVM simulation that:
    1. Creates a uvm_object_list instance
    2. Adds multiple UVM objects to the list using push_back()
    3. Retrieves objects from the list using at(index)
    4. Verifies that all object data is preserved correctly
    5. Tests list operations with various object types
    """
    env = hdl_if_env
    env["PYTHONPATH"] = os.path.join(object_list_data_dir) + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_uvm = pyhdl_dvflow.mkTask("pyhdl-if.UVMPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    uvm_lib = pyhdl_dvflow.mkTask("hdlsim.%s.SimLibUVM" % pyhdl_dvflow.sim)

    uvm_env = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=os.path.join(object_list_data_dir),
                                   type="systemVerilogSource",
                                   include=["object_list_test_pkg.sv", "top.sv"],
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

    # Check that the object list test passed
    assert "All uvm_object_list tests passed!" in simlog, "Object list test did not pass"
    
    # Verify key operations
    assert "Created uvm_object_list" in simlog, "Failed to create uvm_object_list"
    assert "Pushed 3 objects to list" in simlog, "Failed to push objects to list"
    assert "Retrieved objects from list" in simlog, "Failed to retrieve objects from list"
    assert "All values verified correctly" in simlog, "Values not verified correctly"

    pass
