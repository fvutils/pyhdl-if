import os
import sys
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import hdlsim_dvflow, HdlSimDvFlow
from . import hdl_if_env, available_sims_dpi


data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_data_dir = os.path.join(data_dir, "datatypes")

@pytest.mark.parametrize("hdlsim_dvflow", available_sims_dpi(), indirect=True)
def test_real_exp(hdlsim_dvflow, hdl_if_env):
    env = hdl_if_env
    env["PYTHONPATH"] = test_data_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    print("test_smoke_data_dir: %s" % test_data_dir, flush=True)

    hdl_if_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = hdlsim_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="datatypes_real_exp_pkg",
        filename="datatypes_real_exp_pkg.sv",
        modules=["datatypes_real_exp"],
        pythonpath=[test_data_dir])

    test_sv = hdlsim_dvflow.mkTask("std.FileSet",
                                   base=test_data_dir,
                                   include=["datatypes_real_exp.sv"],
                                   type="systemVerilogSource")

    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                        top=["top"],
                        needs=[hdl_if_pkg, hdl_if_dpi, gen_api, test_sv])
    
    sim_run = hdlsim_dvflow.mkTask(
        "hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
        plusargs=["pyhdl_if_debug=1"],
        needs=[sim_img])

    status, out = hdlsim_dvflow.runTask(sim_run)

    assert status == 0

    with open(os.path.join(out.output[0].basedir, "status.txt"), "r") as fp:
        status = fp.read().strip()
    assert "PASS:" in status and "FAIL:" not in status

@pytest.mark.parametrize("hdlsim_dvflow", available_sims_dpi(excl=('xsm',)), indirect=True)
def test_real_imp(hdlsim_dvflow, hdl_if_env):
    env = hdl_if_env
    env["PYTHONPATH"] = test_data_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    print("test_smoke_data_dir: %s" % test_data_dir, flush=True)

    hdl_if_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = hdlsim_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="datatypes_real_imp_pkg",
        filename="datatypes_real_imp_pkg.sv",
        modules=["datatypes_real_imp"],
        pythonpath=[test_data_dir])

    test_sv = hdlsim_dvflow.mkTask("std.FileSet",
                                   base=test_data_dir,
                                   include=["datatypes_real_imp.sv"],
                                   type="systemVerilogSource")

    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                        top=["top"],
                        needs=[hdl_if_pkg, hdl_if_dpi, gen_api, test_sv])
    
    sim_run = hdlsim_dvflow.mkTask(
        "hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
        plusargs=["pyhdl_if_debug=1"],
        needs=[sim_img])

    status, out = hdlsim_dvflow.runTask(sim_run)

    if status != 1:
        print("Test failed...")
        for e in os.listdir(os.path.join(hdlsim_dvflow.builder.rundir)):
            print("Dir: %s" % e)
        build_log = os.path.join(hdlsim_dvflow.builder.rundir, "hdlsim.%s.SimImage" % hdlsim_dvflow.sim, "build.log")
        if os.path.isfile(build_log):
            with open(build_log, "r") as fp:
                print("build.log\n%s" % fp.read())
        else:
            print("No build.log")

    assert status == 0

    with open(os.path.join(out.output[0].basedir, "status.txt"), "r") as fp:
        status = fp.read().strip()
    assert "PASS:" in status and "FAIL:" not in status

@pytest.mark.parametrize("hdlsim_dvflow", available_sims_dpi(excl=('xsm',)), indirect=True)
def test_int_imp(hdlsim_dvflow, hdl_if_env):
    env = hdl_if_env
    env["PYTHONPATH"] = test_data_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    print("test_smoke_data_dir: %s" % test_data_dir, flush=True)

    hdl_if_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = hdlsim_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="datatypes_int_imp_pkg",
        filename="datatypes_int_imp_pkg.sv",
        modules=["datatypes_int_imp"],
        pythonpath=[test_data_dir])

    test_sv = hdlsim_dvflow.mkTask("std.FileSet",
                                   base=test_data_dir,
                                   include=["datatypes_int_imp.sv"],
                                   type="systemVerilogSource")

    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                        top=["top"],
                        needs=[hdl_if_pkg, hdl_if_dpi, gen_api, test_sv])
    
    sim_run = hdlsim_dvflow.mkTask(
        "hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
        plusargs=["pyhdl_if_debug=1"],
        needs=[sim_img])

    status, out = hdlsim_dvflow.runTask(sim_run)

    assert status == 0

    with open(os.path.join(out.output[0].basedir, "status.txt"), "r") as fp:
        status = fp.read().strip()
    assert "PASS:" in status and "FAIL:" not in status
