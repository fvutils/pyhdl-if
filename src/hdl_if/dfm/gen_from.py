#****************************************************************************
#* gen_from.py
#*
#* Copyright 2026 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#****************************************************************************
"""dfm tasks that run the gen-from-* commands.

Each task writes ``<pkgname>.sv`` and ``<pymodule>.py`` into its run
directory and produces the SV file as a ``systemVerilogSource`` FileSet,
plus a ``std.Env`` that puts the run directory (and the task's
``pythonpath``) on ``PYTHONPATH``, so the simulation can import the
Python module.
"""
import logging
import os
import sys
from dv_flow.mgr import TaskDataResult, FileSet

_log = logging.getLogger("hdl-if.GenFrom")


def _names(params):
    pkgname = params.pkgname.strip()
    if pkgname == "":
        raise Exception("pkgname must be set")
    pymodule = params.pymodule.strip() if params.pymodule else ""
    if pymodule == "":
        pymodule = pkgname + "_api"
    return pkgname, pymodule


async def _run(runner, input, args, extra_pythonpath):
    env = runner.env.copy()
    for path in extra_pythonpath:
        env["PYTHONPATH"] = path + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")

    pkgname, pymodule = _names(input.params)
    sv_file = pkgname + ".sv"
    py_file = pymodule + ".py"

    cmd = [sys.executable, '-m', 'hdl_if'] + args + [
        '--sv-out', os.path.join(input.rundir, sv_file),
        '--py-out', os.path.join(input.rundir, py_file),
        '--package', pkgname,
        '--py-module', pymodule,
    ]
    status = await runner.exec(cmd, env=env)

    output = [FileSet(
        basedir=input.rundir,
        files=[sv_file],
        filetype="systemVerilogSource")]

    pypath = [input.rundir] + list(extra_pythonpath)
    env_item = runner.mkDataItem("std.Env")
    env_item.prepend_path = {"PYTHONPATH": os.pathsep.join(pypath)}
    output.append(env_item)

    return TaskDataResult(status=status, output=output)


async def GenFromPy(runner, input) -> TaskDataResult:
    """Runs gen-from-py over ``modules``."""
    p = input.params
    args = ['gen-from-py']
    for m in p.modules:
        args.extend(['-m', m])
    for pat in (p.include or []):
        args.extend(['-i', pat])
    for pat in (p.exclude or []):
        args.extend(['-e', pat])
    pythonpath = [d if os.path.isabs(d) else os.path.join(input.srcdir, d)
                  for d in (p.pythonpath or [])]
    return await _run(runner, input, args, pythonpath)


async def GenFromSpec(runner, input) -> TaskDataResult:
    """Runs gen-from-spec on ``spec``."""
    spec = input.params.spec
    if not os.path.isabs(spec):
        spec = os.path.join(input.srcdir, spec)
    return await _run(runner, input, ['gen-from-spec', spec], [])


async def GenFromSv(runner, input) -> TaskDataResult:
    """Runs gen-from-sv over the SV sources it consumes.

    Sources are the ``systemVerilogSource``/``verilogSource`` FileSets
    produced by the tasks this one needs (files, include directories and
    defines, in order).
    """
    p = input.params
    args = ['gen-from-sv']
    for fs in input.inputs:
        if getattr(fs, "type", None) != "std.FileSet":
            continue
        if fs.filetype not in ("systemVerilogSource", "verilogSource",
                               "systemVerilogInclude", "verilogInclude"):
            continue
        for d in fs.incdirs:
            args.extend(['-I', d if os.path.isabs(d) else os.path.join(fs.basedir, d)])
        if fs.filetype.endswith("Include"):
            args.extend(['-I', fs.basedir])
            continue
        for d in fs.defines:
            args.extend(['-D', d])
        for f in fs.files:
            args.append(f if os.path.isabs(f) else os.path.join(fs.basedir, f))
    for pat in (p.include or []):
        args.extend(['-i', pat])
    for pat in (p.exclude or []):
        args.extend(['-e', pat])
    if p.sv_fields:
        args.extend(['--sv-fields', p.sv_fields])
    for pat in (p.field_exclude or []):
        args.extend(['--field-exclude', pat])
    for pat in (p.skip_base or []):
        args.extend(['--skip-base', pat])
    for pat in (p.stop_at or []):
        args.extend(['--stop-at', pat])
    if p.skip_unsupported:
        args.append('--skip-unsupported')
    return await _run(runner, input, args, [])
