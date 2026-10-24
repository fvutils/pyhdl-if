import os
import pytest
from . import hdl_if_env, available_sims_dpi, hdlsim_dvflow

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
spike_dir = os.path.join(data_dir, "spike_records")


@pytest.mark.parametrize("hdlsim_dvflow", available_sims_dpi(excl=["xsm"]), indirect=True)
def test_spike_records(hdlsim_dvflow, hdl_if_env):
    """Hand-written generated code for records and interfaces (Phase 1)."""
    env = hdl_if_env
    env["PYTHONPATH"] = spike_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    sv_src = hdlsim_dvflow.mkTask("std.FileSet",
                                  base=spike_dir,
                                  include=["spike_pkg.sv", "spike_tb.sv"],
                                  type="systemVerilogSource")
    dpi_lib = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")
    sv_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")

    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                                   top=["spike_tb"],
                                   needs=[sv_pkg, sv_src, dpi_lib])
    sim_run = hdlsim_dvflow.mkTask("hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
                                   needs=[sim_img])

    status, out = hdlsim_dvflow.runTask(sim_run)
    assert status == 0

    with open(os.path.join(sim_run.rundir, "status.txt"), "r") as fp:
        result = fp.read().strip()
    assert result.startswith("PASS:"), result
