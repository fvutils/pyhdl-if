"""Every field and parameter type, copied and referenced in both
directions, with SV and Python implementations of an interface."""
import os
import pytest
from . import hdl_if_env, available_sims_dpi, hdlsim_dvflow

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
types_dir = os.path.join(data_dir, "records_types")


@pytest.mark.parametrize("hdlsim_dvflow", available_sims_dpi(excl=["xsm"]), indirect=True)
def test_records_types(hdlsim_dvflow, hdl_if_env):
    env = hdl_if_env
    env["PYTHONPATH"] = types_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    sv_src = hdlsim_dvflow.mkTask("std.FileSet", base=types_dir,
                                  include=["types_pkg.sv", "types_tb.sv"],
                                  type="systemVerilogSource")
    dpi_lib = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")
    sv_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                                   top=["types_tb"],
                                   needs=[sv_pkg, sv_src, dpi_lib])
    sim_run = hdlsim_dvflow.mkTask("hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
                                   needs=[sim_img])
    status, out = hdlsim_dvflow.runTask(sim_run)
    assert status == 0
    with open(os.path.join(sim_run.rundir, "status.txt")) as fp:
        result = fp.read().strip()
    assert result.startswith("PASS:"), result
