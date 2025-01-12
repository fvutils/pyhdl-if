import os
import sys
import pytest
import pytest_fv as pfv
from pytest_fv.fixtures import *
from .test_base import *

import hdl_if

SKIP_HDLSIM = ('ivl',)

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_py_api_data_dir = os.path.join(data_dir, "py_api")

def _test_file(dirconfig, name, plusargs=None):
    flow = pfv.FlowSim(dirconfig)

    flow.fs.add_library(hdl_if.share())
    flow.sim.addFileset(pfv.FSVlnv("fvutils::pyhdl-if", "systemVerilogSource"))

    flow.sim.addFileset(pfv.FSPaths(
        test_py_api_data_dir, ["%s.sv" % name], "systemVerilogSource"))

    flow.sim.dpi_libs.append(hdl_if.get_entry())
    flow.sim.top.add(name)

    run_args = flow.sim.mkRunArgs(dirconfig.rundir())
    run_args.prepend_pathenv("PYTHONPATH", test_py_api_data_dir)
    if plusargs is not None:
        run_args.plusargs.extend(plusargs)
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(run_args))

    if dirconfig.config.getHdlSim() in SKIP_HDLSIM:
        pytest.skip("Unsupported simulator %s" % dirconfig.config.getHdlSim())
    else:
        flow.run_all()

        with open(os.path.join(dirconfig.rundir(), "status.txt"), "r") as fp:
            status = fp.read().strip()

        assert status.startswith("PASS:")

def test_smoke(dirconfig):
    _test_file(dirconfig, "test_smoke")

def test_a_plus_b(dirconfig):
    _test_file(dirconfig, "a_plus_b")

@pytest.skip("Needs more investigation")
def test_data1(dirconfig):
    _test_file(dirconfig, "data1", plusargs=[
        'data=%s' % os.path.join(test_py_api_data_dir, "data1.json")])