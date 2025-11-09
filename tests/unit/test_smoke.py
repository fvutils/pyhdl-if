
import os
import sys
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_dpi


data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_smoke_data_dir = os.path.join(data_dir, "test_smoke")
test_smoke_str_data_dir = os.path.join(data_dir, "test_smoke_str")

# Verilator has recently started omitting SV Export tasks 
# for this test. 
@pytest.mark.parametrize("pyhdl_dvflow", available_sims_dpi(excl=('vlt',)), indirect=True)
def test_smoke(pyhdl_dvflow, hdl_if_env):
    env = hdl_if_env
    env["PYTHONPATH"] = test_smoke_data_dir + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    print("test_smoke_data_dir: %s" % test_smoke_data_dir, flush=True)

    hdl_if_pkg = pyhdl_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = pyhdl_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="call_sv_bfm_pkg",
        filename="call_sv_bfm_pkg.sv",
        modules=["call_sv_bfm"],
        pythonpath=[test_smoke_data_dir])

    test_sv = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=test_smoke_data_dir,
                                   include=[
                                       "wb_init_bfm.sv", 
                                       "call_sv_bfm.sv"],
                                   type="systemVerilogSource")

    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                        top=["call_sv_bfm"],
                        needs=[hdl_if_pkg, gen_api, hdl_if_dpi, test_sv])
    
    sim_run = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
        plusargs=["pyhdl_if_debug=1"],
        needs=[sim_img])

    status, out = pyhdl_dvflow.runTask(sim_run)

    assert status == 0

    status = None

    if os.path.isfile(os.path.join(out.output[0].basedir, "sim.log")):
        print("HAVE: sim log")
        with open(os.path.join(out.output[0].basedir, "sim.log"), "r") as fp:
            print(fp.read())
    else:
        print("MISSING: sim log")

    if os.path.isfile(os.path.join(out.output[0].basedir, "status.txt")):
        with open(os.path.join(out.output[0].basedir, "status.txt"), "r") as fp:
            status = fp.read().strip()

        assert status.startswith("PASS:")
    else:
        for e in os.listdir(out.output[0].basedir):
            print("Subelem: %s" % e)

    assert status is not None


@pytest.mark.skip("Needs more investigation")
def test_smoke_str(dirconfig):
    flow = pfv.FlowSim(dirconfig)

    print("test_smoke_data_dir: %s" % test_smoke_str_data_dir, flush=True)

    flow.addTaskToPhase("generate.main", pfv.TaskCmd("gen-api",
        cmd=[sys.executable, "-m", "hdl_if", "api-gen-sv", "-m", "call_sv_bfm",
        "--package", "call_sv_bfm_pkg", "-o", "call_sv_bfm_pkg.sv"],
        env=[pfv.EnvAction.prepend_path("PYTHONPATH", test_smoke_str_data_dir)],
        cwd=dirconfig.builddir()
    ))
    flow.fs.add_library(hdl_if.share())
    flow.sim.addFileset(pfv.FSVlnv("fvutils::pyhdl-if", "systemVerilogSource"))

    flow.sim.addFileset(pfv.FSPaths(
        dirconfig.builddir(),
        ["call_sv_bfm_pkg.sv"],
        "systemVerilogSource"))

    flow.sim.addFileset(pfv.FSPaths(
        test_smoke_str_data_dir,
        ["wb_init_bfm.sv", "call_sv_bfm.sv"],
        "systemVerilogSource"))
    
    flow.sim.dpi_libs.append(hdl_if.get_entry())
    flow.sim.top.add("call_sv_bfm")

    run_args = flow.sim.mkRunArgs(dirconfig.rundir())
    run_args.prepend_pathenv("PYTHONPATH", test_smoke_str_data_dir)
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(run_args))

    if dirconfig.config.getHdlSim() in SKIP_HDLSIM:
        pytest.skip("Unsupported simulator %s" % dirconfig.config.getHdlSim())
    else:
        flow.run_all()

        with open(os.path.join(dirconfig.rundir(), "status.txt"), "r") as fp:
            status = fp.read().strip()

        assert status.startswith("PASS:")
