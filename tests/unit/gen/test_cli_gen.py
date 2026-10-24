"""Drives the gen-from-* commands through the argument parser."""
import os
import shutil

import pytest

from hdl_if.__main__ import getparser

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
spike_spec = os.path.join(data_dir, "spike.json")


def run(argv):
    args = getparser().parse_args(argv)
    with pytest.raises(SystemExit) as e:
        args.func(args)
    return e.value.code


def test_gen_from_spec_writes_both(tmpdir):
    sv = os.path.join(str(tmpdir), "out", "my_pkg.sv")
    py = os.path.join(str(tmpdir), "out", "my_api.py")
    assert run(["gen-from-spec", spike_spec, "--sv-out", sv, "--py-out", py]) == 0
    text = open(sv).read()
    assert "package my_pkg;" in text
    assert 'localparam string __PY_MODULE = "my_api";' in text
    assert "class pkt_sv_ref(_rt.SvRef):" in open(py).read()


def test_package_and_module_options(tmpdir):
    sv = os.path.join(str(tmpdir), "a.sv")
    assert run(["gen-from-spec", spike_spec, "--sv-out", sv,
                "-p", "other_pkg", "--py-module", "pkg.sub.mod"]) == 0
    text = open(sv).read()
    assert "package other_pkg;" in text and '"pkg.sub.mod"' in text


def test_check(tmpdir, capsys):
    sv = os.path.join(str(tmpdir), "spike_pkg.sv")
    py = os.path.join(str(tmpdir), "spike_api.py")
    argv = ["gen-from-spec", spike_spec, "--sv-out", sv, "--py-out", py]
    # Missing files fail the check
    assert run(argv + ["--check"]) == 1
    assert "missing" in capsys.readouterr().out
    assert not os.path.exists(sv)
    assert run(argv) == 0
    assert run(argv + ["--check"]) == 0
    assert "up to date" in capsys.readouterr().out
    # An edit is caught and shown as a diff
    with open(py, "a") as fp:
        fp.write("# hand edit\n")
    assert run(argv + ["--check"]) == 1
    out = capsys.readouterr().out
    assert "spike_api.py: differs" in out and "-# hand edit" in out


def test_errors(tmpdir, capsys):
    assert run(["gen-from-spec", spike_spec]) == 2
    assert "Nothing to generate" in capsys.readouterr().err
    assert run(["gen-from-spec", spike_spec, "--sv-out", str(tmpdir.join("x.sv"))]) == 2
    assert "--py-out or --py-module" in capsys.readouterr().err
    bad = tmpdir.join("bad.json")
    bad.write('{"pyhdl-if-spec": 2, "records": [{"name": "r", "fields": [{"name": "a", "type": "nope"}]}]}')
    assert run(["gen-from-spec", str(bad), "--spec-out", str(tmpdir.join("o.json"))]) == 2
    assert "Undefined type 'nope'" in capsys.readouterr().err


def test_gen_from_py(tmpdir):
    sv = os.path.join(str(tmpdir), "fe_pkg.sv")
    py = os.path.join(str(tmpdir), "fe_api.py")
    spec = os.path.join(str(tmpdir), "fe.json")
    assert run(["gen-from-py", "-P", os.path.join(data_dir, "pymods"), "-m", "fe_basic",
                "-e", "fe_basic.SvcPlus", "--sv-out", sv, "--py-out", py,
                "--spec-out", spec]) == 0
    text = open(py).read()
    # Existing Python definitions are imported, not regenerated
    assert "from fe_basic import Outer" in text
    assert "class Outer(" not in text
    assert "class Outer_sv_ref(_rt.SvRef):" in text
    assert "class Svc_sv_proxy(_rt.SvProxy):" in text
    assert "SvcPlus" not in text
    assert "class Outer implements Outer_if;" in open(sv).read()


def test_gen_from_py_requires_module(capsys):
    assert run(["gen-from-py", "--spec-out", "x.json"]) == 2
    assert "at least one module" in capsys.readouterr().err
