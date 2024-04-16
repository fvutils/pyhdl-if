import os
import sys
dpi_vpi_dir = os.path.dirname(os.path.abspath(__file__))
proj_dir = os.path.abspath(os.path.join(dpi_vpi_dir, "../../.."))
sys.path.append(os.path.join(proj_dir, "python"))

import asyncio
import pytest
import pytest_fv as ptv
import sysconfig
from pytest_fv.fixtures import *
import hdl_pi_if

def test_load(dirconfig):
    dpi_vpi_dir = os.path.dirname(os.path.abspath(__file__))
    dpi_vpi_data_dir = os.path.join(dpi_vpi_dir, "data")
    proj_dir = os.path.abspath(os.path.join(dpi_vpi_dir, "../../.."))


    flow = ptv.FlowSim(dirconfig, "xsm")
    flow.addFileset("sim", ptv.FSPaths([
        os.path.join(proj_dir, "python/hdl_pi_if/share/dpi/pyhdl_dpi_if.sv"),
        os.path.join(dpi_vpi_data_dir, "test_load.sv")
    ],
    "systemVerilogSource",
    incs=[
        os.path.join(proj_dir, "python/hdl_pi_if/share/dpi")
    ]))

    from hdl_pi_if.pkginfo import PkgInfo
    pkginfo = PkgInfo()
    flow.sim.dpi_libs.extend(pkginfo.getLibs("dpi"))
    print("dpi_libs: %s" % str(flow.sim.dpi_libs))
    flow.sim.top.add("test_load")

    args = flow.sim.mkRunArgs(dirconfig.rundir())
    args.env["PYTHONPATH"] = os.path.join(proj_dir, "python") + ":" + dpi_vpi_data_dir
#    args.env["LD_LIBRARY_PATH"] = "/project/tools/python/3.12.0/lib"
#    args.env["LD_PRELOAD"] = "/project/tools/python/3.12.0/lib/libpython3.12.so"
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(args))

    flow.run_all()
