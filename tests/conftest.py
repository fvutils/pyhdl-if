import os
import pytest

from dv_flow.libhdlsim.pytest import HdlSimDvFlow
from dv_flow.mgr.package_provider_yaml import PackageProviderYaml


@pytest.fixture
def hdlsim_dvflow(request, tmpdir):
    """Override dv_flow.libhdlsim's fixture to make pyhdl-if tasks discoverable from source."""
    dvflow = HdlSimDvFlow(
        request,
        os.path.dirname(request.fspath),
        tmpdir)

    proj_dir = os.path.abspath(os.path.join(os.path.dirname(request.fspath), "..", ".."))
    flow_dv = os.path.join(proj_dir, "src/hdl_if/dfm/flow.dv")

    dvflow.addPackage("pyhdl-if", flow_dv)
    dvflow.ext_rgy._pkg_m["pyhdl-if"] = PackageProviderYaml(path=flow_dv)

    # Force-load so tasks are available immediately via mkTask
    dvflow.builder.loader.findPackage("pyhdl-if")

    return dvflow

# Alias for backward compatibility
pyhdl_dvflow = hdlsim_dvflow
