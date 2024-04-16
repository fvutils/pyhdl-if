import os
import pytest
import pytest_fv as ptv
from pytest_fv.fixtures import *
import sys

def test_reqrsp_fifo_loopback(dirconfig):
    from ivpm import PkgInfoRgy

    tests_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(tests_dir, "data")
    proj_dir = os.path.abspath(os.path.join(tests_dir, "../../.."))

    flow = ptv.FlowSim(dirconfig, "mti")
    flow.sim.debug = True

    flow.addFileset("sim", ptv.FSVlnv("pyhdl-if::tlm"))
    flow.addFileset("sim", ptv.FSPaths([
        os.path.join(data_dir, "reqrsp_fifo_loopback.sv")], "verilogSource"))
    flow.sim.addIncdir(dirconfig.builddir())
    flow.sim.top.add("reqrsp_fifo_loopback")

    pi_if_pkg = PkgInfoRgy.inst().getPkg("pyhdl-call-if")
    flow.sim.dpi_libs.extend(PkgInfoRgy.inst().getLibs("dpi"))
    flow.sim.addLibDirs(PkgInfoRgy.inst().getLibDirs("dpi"))
#    flow.sim.setenv("PYTHONHOME", os.path.join(proj_dir, "packages/python"))
    flow.sim.append_pathenv("PYTHONPATH", os.path.join(proj_dir, "src"))
    flow.sim.append_pathenv("PYTHONPATH", os.path.join(proj_dir, "packages/pyhdl-pi-if/python"))
    flow.sim.append_pathenv("PYTHONPATH", os.path.join(proj_dir, "packages/pyhdl-call-if/src"))
    flow.sim.append_pathenv("PYTHONPATH", os.path.join(proj_dir, "packages/pyvsc-dataclasses/src"))
    flow.sim.append_pathenv("PYTHONPATH", os.path.join(proj_dir, "packages/pytypeworks/src"))
    flow.sim.append_pathenv("PYTHONPATH", data_dir)

    args = flow.sim.mkRunArgs(dirconfig.rundir())
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(args))

    flow.run_all()

    pass