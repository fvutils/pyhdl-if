
import os
import sys
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import hdl_if_env


data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_smoke_data_dir = os.path.join(data_dir, "test_smoke")
test_smoke_str_data_dir = os.path.join(data_dir, "test_smoke_str")

def test_smoke(hdlsim_dvflow, hdl_if_env):
    env = hdl_if_env
    env["PYTHONPATH"] = test_smoke_data_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    print("test_smoke_data_dir: %s" % test_smoke_data_dir, flush=True)

    hdl_if_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = hdlsim_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="call_sv_bfm_pkg",
        filename="call_sv_bfm_pkg.sv",
        modules=["call_sv_bfm"],
        pythonpath=[test_smoke_data_dir])
    

#    status, out = hdlsim_dvflow.runTask(gen_api)

    # flow.addTaskToPhase("generate.main", pfv.TaskCmd("gen-api",
    #     cmd=[sys.executable, "-m", "hdl_if", "api-gen-sv", "-m", "call_sv_bfm",
    #     "--package", "call_sv_bfm_pkg", "-o", "call_sv_bfm_pkg.sv"],
    #     env=[pfv.EnvAction.prepend_path("PYTHONPATH", test_smoke_data_dir)],
    #     cwd=dirconfig.builddir()
    # ))
    # flow.fs.add_library(hdl_if.share())
    # flow.sim.addFileset(pfv.FSVlnv("fvutils::pyhdl-if", "systemVerilogSource"))

    # flow.sim.addFileset(pfv.FSPaths(
    #     dirconfig.builddir(),
    #     ["call_sv_bfm_pkg.sv"],
    #     "systemVerilogSource"))

    test_sv = hdlsim_dvflow.mkTask("std.FileSet",
                                   base=test_smoke_data_dir,
                                   include=["wb_init_bfm.sv", "call_sv_bfm.sv"],
                                   type="systemVerilogSource")
    # flow.sim.addFileset(pfv.FSPaths(
    #     test_smoke_data_dir,
    #     ["wb_init_bfm.sv", "call_sv_bfm.sv"],
    #     "systemVerilogSource"))
    
    # flow.sim.dpi_libs.append(hdl_if.get_entry())
    # flow.sim.top.add("call_sv_bfm")

    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                        top=["call_sv_bfm"],
                        needs=[hdl_if_pkg, hdl_if_dpi, gen_api, test_sv])
    
    sim_run = hdlsim_dvflow.mkTask(
        "hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
        needs=[sim_img])

    status, out = hdlsim_dvflow.runTask(sim_run)

    assert status == 0

    # run_args = flow.sim.mkRunArgs(dirconfig.rundir())
    # run_args.prepend_pathenv("PYTHONPATH", test_smoke_data_dir)
    # flow.addTaskToPhase("run.main", flow.sim.mkRunTask(run_args))

    with open(os.path.join(out.output[0].basedir, "status.txt"), "r") as fp:
        status = fp.read().strip()

        assert status.startswith("PASS:")

    # if dirconfig.config.getHdlSim() in SKIP_HDLSIM:
    #     pytest.skip("Unsupported simulator %s" % dirconfig.config.getHdlSim())
    # else:
    #     flow.run_all()


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
