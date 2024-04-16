
import os
import pytest
import pytest_fv as ptv
from pytest_fv.fixtures import *
import sys

print("PYTHONPATH: %s" % str(sys.path))

def test_hvl2hdl_fifo(dirconfig):
    from ivpm import PkgInfoRgy
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(tests_dir, "data")
    proj_dir = os.path.abspath(os.path.join(tests_dir, "../../.."))

    flow = ptv.FlowSim(dirconfig, "mti")
    flow.sim.debug = True

    flow.addFileset("sim", ptv.FSVlnv("pyhdl-if::tlm"))
    flow.addFileset("sim", ptv.FSPaths([
        os.path.join(data_dir, "hvl2hdl_fifo.sv")], "verilogSource"))
    flow.sim.addIncdir(dirconfig.builddir())
    flow.sim.top.add("hvl2hdl_fifo")

    pi_if_pkg = PkgInfoRgy.inst().getPkg("pyhdl-call-if")
    flow.sim.dpi_libs.extend(PkgInfoRgy.inst().getLibs("dpi"))
    flow.sim.addLibDirs(PkgInfoRgy.inst().getLibDirs("dpi"))
    flow.sim.append_pathenv("PYTHONPATH", os.path.join(proj_dir, "src"))
    flow.sim.append_pathenv("PYTHONPATH", os.path.join(proj_dir, "packages/pyhdl-pi-if/python"))
    flow.sim.append_pathenv("PYTHONPATH", data_dir)

    args = flow.sim.mkRunArgs(dirconfig.rundir())
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(args))

    flow.run_all()

def test_hdl2hvl_fifo(dirconfig):
    from ivpm import PkgInfoRgy
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(tests_dir, "data")
    proj_dir = os.path.abspath(os.path.join(tests_dir, "../../.."))

    flow = ptv.FlowSim(dirconfig, "mti")
    flow.sim.debug = True

    flow.addFileset("sim", ptv.FSVlnv("pyhdl-if::tlm"))
    flow.addFileset("sim", ptv.FSPaths([
        os.path.join(data_dir, "hdl2hvl_fifo.sv")], "verilogSource"))
    flow.sim.addIncdir(dirconfig.builddir())
    flow.sim.top.add("hdl2hvl_fifo")

    pi_if_pkg = PkgInfoRgy.inst().getPkg("pyhdl-call-if")
    flow.sim.dpi_libs.extend(PkgInfoRgy.inst().getLibs("dpi"))
    flow.sim.addLibDirs(PkgInfoRgy.inst().getLibDirs("dpi"))
    flow.sim.append_pathenv("PYTHONPATH", os.path.join(proj_dir, "src"))
    flow.sim.append_pathenv("PYTHONPATH", os.path.join(proj_dir, "packages/pyhdl-pi-if/python"))
    flow.sim.append_pathenv("PYTHONPATH", data_dir)

    args = flow.sim.mkRunArgs(dirconfig.rundir())
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(args))

    flow.run_all()
    pass