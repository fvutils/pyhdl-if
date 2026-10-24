"""Runs each tutorial example (examples/tutorial) the way a user would, on
Verilator, and each example's own Python-only tests."""
import glob
import os
import shutil
import subprocess
import sys

import pytest
from . import hdl_if_env, available_sims_uvm

pyhdl_if_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
tutorial_dir = os.path.join(pyhdl_if_dir, "examples", "tutorial")

# Example -> the Python modules it needs
EXAMPLES = {
    "00_base": [],
    "01_scoreboard_numpy": ["numpy"],
    "02a_sv2py_coverage": ["vsc", "pyslang"],
    "02b_py2sv_ref_packets": ["pydantic"],
    "03a_py_sv_library": ["scapy"],
    "03b_sv_api_py_test": ["vsc", "pyslang"],
}


def _copy_tutorial(tmp_path):
    dst = os.path.join(str(tmp_path), "tutorial")
    shutil.copytree(tutorial_dir, dst,
                    ignore=shutil.ignore_patterns("rundir", "__pycache__", ".pytest_cache"))
    return dst


@pytest.mark.parametrize("example", list(EXAMPLES.keys()))
def test_tutorial_sim(example, tmp_path, hdl_if_env):
    if "vlt" not in available_sims_uvm(incl=["vlt"]):
        pytest.skip("Verilator is not available")
    for m in EXAMPLES[example]:
        pytest.importorskip(m)

    ex_dir = os.path.join(_copy_tutorial(tmp_path), example)

    # Find pyhdl-if's dfm package in this tree, installed or not
    pkg_map = os.path.join(str(tmp_path), "package-map.yaml")
    with open(pkg_map, "w") as fp:
        fp.write("package-map:\n  version: 1\n  packages:\n"
                 "  - name: pyhdl-if\n    path: %s\n" %
                 os.path.join(pyhdl_if_dir, "src", "hdl_if", "dfm", "flow.dv"))

    log = os.path.join(str(tmp_path), "dfm.log")
    with open(log, "w") as fp:
        status = subprocess.run(
            [sys.executable, "-m", "dv_flow.mgr", "--package-map", pkg_map,
             "run", "-D", "sim=vlt", "sim-run"],
            cwd=ex_dir, env=hdl_if_env, stdout=fp, stderr=subprocess.STDOUT).returncode
    with open(log) as fp:
        assert status == 0, fp.read()[-3000:]

    sim_logs = glob.glob(os.path.join(ex_dir, "rundir", "*.sim-run", "sim.log"))
    assert len(sim_logs) == 1, sim_logs
    with open(sim_logs[0]) as fp:
        text = fp.read()
    assert "TEST PASSED" in text, text[-3000:]


@pytest.mark.parametrize("example", [e for e in EXAMPLES.keys() if e != "00_base"])
def test_tutorial_python(example, tmp_path, hdl_if_env):
    for m in EXAMPLES[example]:
        if m != "pyslang":
            pytest.importorskip(m)
    ex_dir = os.path.join(_copy_tutorial(tmp_path), example)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "."],
                       cwd=ex_dir, env=hdl_if_env, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
