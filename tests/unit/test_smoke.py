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
test_smoke_data_dir = os.path.join(data_dir, "test_smoke")
test_smoke_str_data_dir = os.path.join(data_dir, "test_smoke_str")


def test_smoke(dirconfig : pfv.DirConfig):
    flow = pfv.FlowSim(dirconfig)

    print("test_smoke_data_dir: %s" % test_smoke_data_dir, flush=True)

    flow.addTaskToPhase("generate.main", pfv.TaskCmd("gen-api",
        cmd=[sys.executable, "-m", "hdl_if", "api-gen-sv", "-m", "call_sv_bfm",
        "--package", "call_sv_bfm_pkg", "-o", "call_sv_bfm_pkg.sv"],
        env=[pfv.EnvAction.prepend_path("PYTHONPATH", test_smoke_data_dir)],
        cwd=dirconfig.builddir()
    ))
    flow.fs.add_library(hdl_if.share())
    flow.sim.addFileset(pfv.FSVlnv("fvutils::pyhdl-if", "systemVerilogSource"))

    flow.sim.addFileset(pfv.FSPaths(
        dirconfig.builddir(),
        ["call_sv_bfm_pkg.sv"],
        "systemVerilogSource"))

    flow.sim.addFileset(pfv.FSPaths(
        test_smoke_data_dir,
        ["wb_init_bfm.sv", "call_sv_bfm.sv"],
        "systemVerilogSource"))
    
    flow.sim.dpi_libs.append(hdl_if.get_entry())
    flow.sim.top.add("call_sv_bfm")

    run_args = flow.sim.mkRunArgs(dirconfig.rundir())
    run_args.prepend_pathenv("PYTHONPATH", test_smoke_data_dir)
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(run_args))

    if dirconfig.config.getHdlSim() in SKIP_HDLSIM:
        pytest.skip("Unsupported simulator %s" % dirconfig.config.getHdlSim())
    else:
        flow.run_all()

        with open(os.path.join(dirconfig.rundir(), "status.txt"), "r") as fp:
            status = fp.read().strip()

        assert status.startswith("PASS:")

def test_smoke_str(dirconfig : pfv.DirConfig):
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
