import os
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

    flow = ptv.FlowSim(dirconfig, "mti")
    flow.addFileset("sim", ptv.FSPaths([
        os.path.join(proj_dir, "python/hdl_pi_if/share/dpi/pyhdl_dpi_if.sv"),
        os.path.join(dpi_vpi_data_dir, "test_load.sv")
    ],
    "systemVerilogSource",
    incs=[
        os.path.join(proj_dir, "python/hdl_pi_if/share/dpi")
    ]))
    flow.sim.dpi_libs.append(hdl_pi_if.get_entry())
    flow.sim.pli_libs.append(hdl_pi_if.get_entry())
    flow.sim.top.add("test_load")

    args = flow.sim.mkRunArgs(dirconfig.rundir())
    args.env["PYTHONPATH"] = os.path.join(proj_dir, "python") + ":" + dpi_vpi_data_dir
    args.env["LD_LIBRARY_PATH"] = "/project/tools/python/3.12.0/lib"
    args.plusargs.append("pyhdl-pi-if.mod=load")
#    args.env["LD_PRELOAD"] = "/project/tools/python/3.12.0/lib/libpython3.12.so"
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(args))

    flow.run_all()
