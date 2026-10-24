"""The GenFromSpec / GenFromPy dfm tasks feed a simulation."""
import os
import pytest
from . import hdl_if_env, available_sims_dpi, hdlsim_dvflow

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
spike_dir = os.path.join(data_dir, "spike_records")
spec = os.path.join(data_dir, "..", "gen", "data", "spike.json")


def _run_spike_tb(hdlsim_dvflow, env, gen):
    # spike_drv.py lives in spike_dir; the generated spike_api comes from
    # the gen task's run directory, which its std.Env puts first
    env["PYTHONPATH"] = spike_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    tb = hdlsim_dvflow.mkTask("std.FileSet", base=spike_dir,
                              include=["spike_tb.sv"], type="systemVerilogSource")
    dpi_lib = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")
    sv_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                                   top=["spike_tb"],
                                   needs=[sv_pkg, gen, tb, dpi_lib])
    sim_run = hdlsim_dvflow.mkTask("hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
                                   needs=[sim_img])
    status, out = hdlsim_dvflow.runTask(sim_run)
    assert status == 0
    with open(os.path.join(sim_run.rundir, "status.txt")) as fp:
        result = fp.read().strip()
    assert result.startswith("PASS:"), result
    with open(os.path.join(sim_run.rundir, "sim.log")) as fp:
        log = fp.read()
    return gen, log


@pytest.mark.parametrize("hdlsim_dvflow", available_sims_dpi(excl=["xsm"]), indirect=True)
def test_gen_from_spec_task(hdlsim_dvflow, hdl_if_env):
    gen = hdlsim_dvflow.mkTask("pyhdl-if.GenFromSpec",
                               pkgname="spike_pkg", pymodule="spike_api",
                               spec=os.path.abspath(spec))
    gen, log = _run_spike_tb(hdlsim_dvflow, hdl_if_env, gen)
    assert os.path.isfile(os.path.join(gen.rundir, "spike_pkg.sv"))
    assert os.path.isfile(os.path.join(gen.rundir, "spike_api.py"))
    assert "spike_api from %s" % os.path.join(gen.rundir, "spike_api.py") in log


@pytest.mark.parametrize("hdlsim_dvflow", available_sims_dpi(excl=["xsm"]), indirect=True)
def test_gen_from_py_task(hdlsim_dvflow, hdl_if_env):
    """A record and interface declared in Python; SV implements the interface."""
    py_dir = os.path.join(data_dir, "records_py")
    env = hdl_if_env
    env["PYTHONPATH"] = py_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    gen = hdlsim_dvflow.mkTask("pyhdl-if.GenFromPy",
                               pkgname="pkt_pkg", pymodule="pkt_api",
                               modules=["pkt_model"], pythonpath=[py_dir])
    tb = hdlsim_dvflow.mkTask("std.FileSet", base=py_dir,
                              include=["pkt_tb.sv"], type="systemVerilogSource")
    dpi_lib = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")
    sv_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                                   top=["pkt_tb"], needs=[sv_pkg, gen, tb, dpi_lib])
    sim_run = hdlsim_dvflow.mkTask("hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
                                   needs=[sim_img])
    status, out = hdlsim_dvflow.runTask(sim_run)
    assert status == 0
    with open(os.path.join(sim_run.rundir, "status.txt")) as fp:
        result = fp.read().strip()
    assert result.startswith("PASS:"), result
    # The Python module imports the user's classes instead of redefining them
    with open(os.path.join(gen.rundir, "pkt_api.py")) as fp:
        assert "from pkt_model import RefPkt" in fp.read()
