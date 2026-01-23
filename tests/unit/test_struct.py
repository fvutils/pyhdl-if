import os
import sys
import pytest
from .test_base import *
from dv_flow.libhdlsim.pytest import HdlSimDvFlow
from . import pyhdl_dvflow, hdl_if_env, available_sims_dpi


data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_struct_data_dir = os.path.join(data_dir, "test_struct")


@pytest.mark.parametrize("pyhdl_dvflow", available_sims_dpi(), indirect=True)
def test_struct(pyhdl_dvflow, hdl_if_env):
    """Test basic struct support with Point struct"""
    env = hdl_if_env
    env["PYTHONPATH"] = test_struct_data_dir + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    print("test_struct_data_dir: %s" % test_struct_data_dir, flush=True)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_pkg = pyhdl_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = pyhdl_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="struct_api_pkg",
        filename="struct_api_pkg.sv",
        modules=["struct_api"],
        pythonpath=[test_struct_data_dir])

    test_sv = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=test_struct_data_dir,
                                   include=["struct_bfm.sv"],
                                   type="systemVerilogSource")

    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                        top=["struct_bfm"],
                        needs=[hdl_if_pkg, gen_api, hdl_if_dpi, test_sv],
                        elabargs=args)
    
    sim_run = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
        needs=[sim_img])
    
    status, out = pyhdl_dvflow.runTask(sim_run)
    
    assert status == 0
    
    # Check the status file for PASS
    status_file = os.path.join(out.output[0].basedir, "status.txt")
    assert os.path.isfile(status_file), f"status.txt not found at {status_file}"
    
    with open(status_file) as f:
        status_content = f.read()
        print("Status: %s" % status_content)
        assert "PASS" in status_content


@pytest.mark.parametrize("pyhdl_dvflow", available_sims_dpi(), indirect=True)
def test_struct_comprehensive(pyhdl_dvflow, hdl_if_env):
    """Test comprehensive struct support: multiple types, various field types, many fields"""
    env = hdl_if_env
    env["PYTHONPATH"] = test_struct_data_dir + os.pathsep + env["PYTHONPATH"]
    pyhdl_dvflow.setEnv(env)

    print("test_struct_comprehensive_data_dir: %s" % test_struct_data_dir, flush=True)

    args = ["-timescale=1ps/1ps"] if pyhdl_dvflow.sim == "vcs" else []

    hdl_if_pkg = pyhdl_dvflow.mkTask("pyhdl-if.SvPkg")
    hdl_if_dpi = pyhdl_dvflow.mkTask("pyhdl-if.DpiLib")

    gen_api = pyhdl_dvflow.mkTask(
        "pyhdl-if.APIGenSV",
        pkgname="struct_comprehensive_api_pkg",
        filename="struct_comprehensive_api_pkg.sv",
        modules=["struct_comprehensive_api"],
        pythonpath=[test_struct_data_dir])

    test_sv = pyhdl_dvflow.mkTask("std.FileSet",
                                   base=test_struct_data_dir,
                                   include=["struct_comprehensive_bfm.sv"],
                                   type="systemVerilogSource")

    sim_img = pyhdl_dvflow.mkTask("hdlsim.%s.SimImage" % pyhdl_dvflow.sim,
                        top=["struct_comprehensive_bfm"],
                        needs=[hdl_if_pkg, gen_api, hdl_if_dpi, test_sv],
                        elabargs=args)
    
    sim_run = pyhdl_dvflow.mkTask(
        "hdlsim.%s.SimRun" % pyhdl_dvflow.sim,
        needs=[sim_img])
    
    status, out = pyhdl_dvflow.runTask(sim_run)
    
    assert status == 0
    
    # Check the status file for PASS
    status_file = os.path.join(out.output[0].basedir, "status.txt")
    assert os.path.isfile(status_file), f"status.txt not found at {status_file}"
    
    with open(status_file) as f:
        status_content = f.read()
        print("Status: %s" % status_content)
        assert "PASS" in status_content

