"""Generated code checks the runtime API version it was generated for."""
import os
import shutil
import types

import pytest
from . import hdl_if_env, available_sims_dpi, hdlsim_dvflow

from hdl_if.gen.spec import load_spec
from hdl_if.gen.sv import gen_sv
from hdl_if.gen.py import gen_py
from hdl_if.rt_api import PYHDL_IF_RT_API_VERSION

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
spec = os.path.join(data_dir, "..", "gen", "data", "spike.json")
ver = PYHDL_IF_RT_API_VERSION


def _restamp(text, old, new):
    assert old in text
    return text.replace(old, new)


@pytest.mark.parametrize("stamp,msg", [(ver + 1, "Upgrade pyhdl-if"), (0, "Regenerate")])
def test_python_module_rejects_version(stamp, msg):
    text = gen_py(load_spec(spec), "spike.json")
    text = _restamp(text, "_rt.check_rt_api_version(%d," % ver,
                    "_rt.check_rt_api_version(%d," % stamp)
    m = types.ModuleType("ver_api")
    with pytest.raises(RuntimeError, match=msg):
        exec(compile(text, "ver_api.py", "exec"), m.__dict__)


@pytest.mark.parametrize("hdlsim_dvflow", available_sims_dpi(excl=["xsm"]), indirect=True)
def test_sv_package_rejects_version(hdlsim_dvflow, hdl_if_env, tmpdir):
    text = gen_sv(load_spec(spec), "ver_pkg", "spike_api", "spike.json")
    text = _restamp(text, "pyhdl_if_check_rt_api_version(%d," % ver,
                    "pyhdl_if_check_rt_api_version(%d," % (ver + 1))
    srcdir = tmpdir.mkdir("src")
    srcdir.join("ver_pkg.sv").write(text)
    shutil.copy(os.path.join(data_dir, "records_version", "ver_tb.sv"), str(srcdir))

    hdlsim_dvflow.setEnv(hdl_if_env)
    src = hdlsim_dvflow.mkTask("std.FileSet", base=str(srcdir),
                               include=["ver_pkg.sv", "ver_tb.sv"], type="systemVerilogSource")
    dpi_lib = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")
    sv_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                                   top=["ver_tb"], needs=[sv_pkg, src, dpi_lib])
    sim_run = hdlsim_dvflow.mkTask("hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
                                   needs=[sim_img])
    hdlsim_dvflow.runTask(sim_run)
    with open(os.path.join(sim_run.rundir, "sim.log")) as fp:
        log = fp.read()
    assert "ver_pkg targets runtime API version %d" % (ver + 1) in log
    assert "Upgrade pyhdl-if" in log
    assert not os.path.isfile(os.path.join(sim_run.rundir, "status.txt"))
