import os
import subprocess

import pytest

from . import available_sims_uvm, hdl_if_env


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, "..", ".."))
TUTORIAL_DIR = os.path.join(REPO_ROOT, "tutorials", "01-hello-world")


@pytest.mark.parametrize("sim", available_sims_uvm())
def test_tutorial_01_hello_world(sim, hdl_if_env):
    env = hdl_if_env.copy()
    env["PYTHONPATH"] = TUTORIAL_DIR + os.pathsep + env.get("PYTHONPATH", "")

    cmd = [
        os.path.join(REPO_ROOT, "packages", "python", "bin", "dfm"),
        "run",
        "--clean",
        f"-Dsim={sim}",
        "sim-run",
    ]

    result = subprocess.run(
        cmd,
        cwd=TUTORIAL_DIR,
        env=env,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        raise AssertionError(
            "Tutorial 01 dfm run failed\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    sim_log = os.path.join(TUTORIAL_DIR, "rundir", "hello_world.sim-run", "sim.log")
    assert os.path.isfile(sim_log)

    with open(sim_log, "r") as fp:
        log = fp.read()

    assert "HelloComp: build_phase" in log
    assert "HelloComp: connect_phase" in log
    assert "Hello, World! from Python inside UVM run_phase" in log
