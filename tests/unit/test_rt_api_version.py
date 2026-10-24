import os
import re
import pytest

import hdl_if
from hdl_if.rt_api import (
    PYHDL_IF_RT_API_VERSION, PYHDL_IF_RT_API_MIN_VERSION, check_rt_api_version)


def test_current_version_accepted():
    check_rt_api_version(PYHDL_IF_RT_API_VERSION, "x")
    check_rt_api_version(PYHDL_IF_RT_API_MIN_VERSION, "x")


def test_newer_version_rejected():
    with pytest.raises(RuntimeError, match="Upgrade pyhdl-if"):
        check_rt_api_version(PYHDL_IF_RT_API_VERSION + 1, "x")


def test_older_version_rejected():
    with pytest.raises(RuntimeError, match="Regenerate"):
        check_rt_api_version(PYHDL_IF_RT_API_MIN_VERSION - 1, "x")


def test_sv_and_python_versions_match():
    sv = open(os.path.join(hdl_if.share(), "dpi", "pyhdl_if.sv")).read()
    ver = re.search(r"parameter int PYHDL_IF_RT_API_VERSION = (\d+);", sv)
    min_ver = re.search(r"parameter int PYHDL_IF_RT_API_MIN_VERSION = (\d+);", sv)
    assert int(ver.group(1)) == PYHDL_IF_RT_API_VERSION
    assert int(min_ver.group(1)) == PYHDL_IF_RT_API_MIN_VERSION


def test_policy_accepts_range(monkeypatch):
    """Stamps from MIN_VERSION up to VERSION are accepted; others are not."""
    import hdl_if.rt_api as rt_api
    monkeypatch.setattr(rt_api, "PYHDL_IF_RT_API_VERSION", 3)
    monkeypatch.setattr(rt_api, "PYHDL_IF_RT_API_MIN_VERSION", 2)
    rt_api.check_rt_api_version(2, "x")
    rt_api.check_rt_api_version(3, "x")
    with pytest.raises(RuntimeError, match="Regenerate"):
        rt_api.check_rt_api_version(1, "x")
    with pytest.raises(RuntimeError, match="Upgrade"):
        rt_api.check_rt_api_version(4, "x")
