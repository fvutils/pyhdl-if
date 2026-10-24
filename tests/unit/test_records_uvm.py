"""gen-from-sv on a uvm_sequence_item subclass: copied and referenced from
Python, and an SV interface class implemented in Python."""
import os
import pytest
from . import hdl_if_env, available_sims_uvm, hdlsim_dvflow

pytest.importorskip("pyslang")

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "records_uvm")


@pytest.mark.parametrize("backdoor", [False, True], ids=["dpi", "backdoor"])
@pytest.mark.parametrize("hdlsim_dvflow", available_sims_uvm(incl=["vlt"]), indirect=True)
def test_records_uvm(hdlsim_dvflow, hdl_if_env, backdoor):
    env = hdl_if_env
    env["PYTHONPATH"] = data_dir + os.pathsep + env["PYTHONPATH"]
    hdlsim_dvflow.setEnv(env)

    # pyhdl-if integrates via DPI. By default the UVM DPI layer is built
    # without --vpi; backdoor adds UVM's register backdoor and --vpi, where
    # pyhdl-if's VPI start-up must stand aside on Verilator.
    uvm = hdlsim_dvflow.mkTask("hdlsim.%s.SimLibUVM" % hdlsim_dvflow.sim, dpi="true",
                               backdoor=backdoor)
    user = hdlsim_dvflow.mkTask("std.FileSet", name="user_src", base=data_dir,
                                include=["pkt_item_pkg.sv"],
                                type="systemVerilogSource")
    tb = hdlsim_dvflow.mkTask("std.FileSet", name="tb_src", base=data_dir,
                              include=["uvm_rec_tb.sv"],
                              type="systemVerilogSource")
    gen = hdlsim_dvflow.mkTask("pyhdl-if.GenFromSv",
                               pkgname="pkt_gen_pkg", pymodule="pkt_gen_api",
                               include=["pkt_item_pkg::*"],
                               needs=[uvm, user])
    dpi_lib = hdlsim_dvflow.mkTask("pyhdl-if.DpiLib")
    sv_pkg = hdlsim_dvflow.mkTask("pyhdl-if.SvPkg")
    sim_img = hdlsim_dvflow.mkTask("hdlsim.%s.SimImage" % hdlsim_dvflow.sim,
                                   top=["uvm_rec_tb"],
                                   needs=[uvm, sv_pkg, dpi_lib, user, gen, tb])
    sim_run = hdlsim_dvflow.mkTask("hdlsim.%s.SimRun" % hdlsim_dvflow.sim,
                                   plusargs=["REC_ARG=42"],
                                   needs=[sim_img])
    status, out = hdlsim_dvflow.runTask(sim_run)
    assert status == 0
    with open(os.path.join(sim_run.rundir, "status.txt")) as fp:
        result = fp.read().strip()
    assert result.startswith("PASS:"), result
    with open(os.path.join(sim_img.rundir, "build.f")) as fp:
        assert ("--vpi" in fp.read().split()) == backdoor
