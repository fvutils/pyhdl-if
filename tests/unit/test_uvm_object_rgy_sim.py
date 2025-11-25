import os
import pytest
import hdl_if
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_uvm

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
uvm_data_dir = os.path.join(data_dir, "uvm")
uvm_obj_rgy_data_dir = os.path.join(uvm_data_dir, "object_registry")

@pytest.mark.parametrize("pyhdl_dvflow", available_sims_uvm(), indirect=True)
def test_object_registry_smoke(pyhdl_dvflow, hdl_if_env):
    """
    Test the UVM Object Registry functionality in a simulation environment.
    
    This test runs a UVM simulation that:
    1. Creates various UVM objects and components to populate the factory
    2. Uses the Python UvmObjectRgy to query available type names
    3. Verifies that the typenames property correctly parses the factory output
    4. Ensures pyhdl_* types are filtered out as expected
    5. Confirms that standard UVM types are available
    """
    env = hdl_if_env
    env["PYTHONPATH"] = os.path.join(uvm_obj_rgy_data_dir, "smoke") + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_uvm = pyhdl_dvflow.mkTask("pyhdl-if.UVMPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    uvm_lib = pyhdl_dvflow.mkTask("hdlsim.%s.SimLibUVM" % pyhdl_dvflow.sim)

    uvm_env = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=os.path.join(uvm_obj_rgy_data_dir, "smoke"),
                                   type="systemVerilogSource",
                                   include=["object_registry_smoke_pkg.sv", "top.sv"],
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

    # Check that the object registry test passed
    assert "Object registry filtering test passed!" in simlog, "Object registry test did not pass"
    
    # Verify that we got some UVM type names
    assert "Found" in simlog and "UVM types:" in simlog, "UVM type names were not found"
    
    # Verify that pyhdl_ types were filtered out
    assert "Found pyhdl_ types (should be empty): []" in simlog, "pyhdl_ types were not properly filtered"

    pass
