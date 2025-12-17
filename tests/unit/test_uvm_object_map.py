import os
import pytest
import hdl_if
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_uvm

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
uvm_data_dir = os.path.join(data_dir, "uvm")
object_map_data_dir = os.path.join(uvm_data_dir, "object_map")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_uvm(excl=('vlt')), indirect=True)
def test_uvm_object_map(pyhdl_dvflow, hdl_if_env):
    """
    Test the uvm_object_map functionality in a simulation environment.
    
    This test runs a UVM simulation that:
    1. Creates a uvm_object_map instance
    2. Tests has_key() for non-existent keys (should return False)
    3. Adds multiple UVM objects to the map using insert(key, obj)
    4. Tests has_key() for existing keys (should return True)
    5. Retrieves objects from the map using get(key)
    6. Verifies that all object data is preserved correctly
    7. Tests updating existing keys
    8. Tests various key name formats
    """
    env = hdl_if_env
    env["PYTHONPATH"] = os.path.join(object_map_data_dir) + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_uvm = pyhdl_dvflow.mkTask("pyhdl-if.UVMPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    uvm_lib = pyhdl_dvflow.mkTask("hdlsim.%s.SimLibUVM" % pyhdl_dvflow.sim)

    uvm_env = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=os.path.join(object_map_data_dir),
                                   type="systemVerilogSource",
                                   include=["object_map_test_pkg.sv", "top.sv"],
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

    # Check that the object map test passed
    assert "All uvm_object_map tests passed!" in simlog, "Object map test did not pass"
    
    # Verify key operations
    assert "Created uvm_object_map" in simlog, "Failed to create uvm_object_map"
    assert "has_key() correctly returns False for non-existent keys" in simlog, "has_key() failed for non-existent keys"
    assert "Added 3 objects to map with keys" in simlog, "Failed to add objects to map"
    assert "has_key() correctly identifies existing and non-existing keys" in simlog, "has_key() failed to identify keys correctly"
    assert "Retrieved objects from map" in simlog, "Failed to retrieve objects from map"
    assert "All objects verified correctly" in simlog, "Objects not verified correctly"
    assert "Successfully updated existing key" in simlog, "Failed to update existing key"

    pass
