import os
import sys
import pytest
from .test_base import *

print("path: %s" % str(sys.path))

import hdl_if

data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data")
test_vpi_py_if_data_dir = os.path.join(data_dir, "vpi_py_if")

SKIP_HDLSIM = ('xsm', 'vlt')


def test_smoke(dirconfig):
    flow = pfv.FlowSim(dirconfig)

#    flow.fs.add_library(hdl_if.share())
#    flow.sim.addFileset(pfv.FSVlnv("fvutils::pyhdl-if", "systemVerilogSource"))

#    flow.sim.addFileset(pfv.FSPaths(
#        dirconfig.builddir(),
#        ["call_sv_bfm_pkg.sv"],
#        "systemVerilogSource"))

    flow.sim.addFileset(pfv.FSPaths(
        test_vpi_py_if_data_dir,
        ["vpi_py_if_smoke.v"],
        "verilogSource"))
    
    flow.sim.pli_libs.append(hdl_if.get_entry())
    flow.sim.top.add("vpi_py_if_smoke")

    global hdl_if_dir
    run_args = flow.sim.mkRunArgs(dirconfig.rundir())
#    run_args.prepend_pathenv("PYTHONPATH", hdl_if_dir)
    flow.addTaskToPhase("run.main", flow.sim.mkRunTask(run_args))

    if dirconfig.config.getHdlSim() in SKIP_HDLSIM:
        pytest.skip("Unsupported simulator %s" % dirconfig.config.getHdlSim())
    else:
        flow.run_all()