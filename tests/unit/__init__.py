import os
import pytest

@pytest.fixture(scope="session")
def hdl_if_env():
    unit_tests_dir = os.path.dirname(os.path.abspath(__file__))
    hdl_if_dir = os.path.abspath(
        os.path.join(unit_tests_dir, "..", "..", "src"))

    env = os.environ.copy()
    if "PYTHONPATH" not in env:
        env["PYTHONPATH"] = hdl_if_dir
    else:
        env["PYTHONPATH"] += os.pathsep + hdl_if_dir

    return env


