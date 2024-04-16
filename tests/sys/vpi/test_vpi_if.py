import os
import asyncio
import pytest
import pytest_fv as ptv
from pytest_fv.fixtures import *
import hdl_pi_if

def test_load(dirconfig):
    vpi_dir = os.path.dirname(os.path.abspath(__file__))
    vpi_data_dir = os.path.join(vpi_dir, "data")
    proj_dir = os.path.abspath(os.path.join(vpi_dir, "../../.."))

    flow = ptv.FlowSim(dirconfig, "ivl")
    flow.addFileset("sim", ptv.FSPaths([
        os.path.join(vpi_data_dir, "test_load.sv")
    ],
    "verilogSource"))
    flow.sim.top.add("test_load")
    flow.sim.pli_libs.append(hdl_pi_if.get_entry())
    flow.sim.plusargs.append("pyhdl-pi-if.mod=load")

    args = flow.sim.mkRunArgs(dirconfig.rundir())
    args.env["PYTHONPATH"] = os.path.join(proj_dir, "python") + ":" + vpi_data_dir
    args.env["LD_LIBRARY_PATH"] = "/project/tools/python/3.12.0/lib"
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(args))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(flow.run())

    pass

