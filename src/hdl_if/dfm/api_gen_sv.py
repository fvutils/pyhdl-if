import logging
import os
import sys
from dv_flow.mgr import TaskRunCtxt, TaskDataInput, TaskDataResult, FileSet

_log = logging.getLogger("hdl-if.APIGenSV")

async def APIGenSV(runner, input) -> None:

    env = runner.env.copy()

    _log.debug("Initial PYTHONPATH: %s" % env.get("PYTHONPATH", "<unset>"))

    if input.params.pythonpath:
        for path in input.params.pythonpath:
            if "PYTHONPATH" not in env:
                env["PYTHONPATH"] = path
            else:
                env["PYTHONPATH"] += os.pathsep + path

    _log.debug("Final PYTHONPATH: %s" % env.get("PYTHONPATH", "<unset>"))

    status = 0
    
    cmd = [
        sys.executable,
        '-m', 'hdl_if',
        'api-gen-sv',
    ]

    # Check for spec parameter (new way)
    if hasattr(input.params, 'spec') and input.params.spec:
        # Check if it's a filepath and validate extension
        spec_value = input.params.spec
        if os.path.exists(spec_value):
            ext = os.path.splitext(spec_value)[1].lower()
            if ext != '.json':
                raise Exception(f"Spec filepath must have .json extension (got: {ext})")
        cmd.extend(['-s', spec_value])
        
        # Add spec format if specified
        if hasattr(input.params, 'spec_fmt') and input.params.spec_fmt:
            cmd.extend(['--spec-fmt', input.params.spec_fmt])
    # Check for legacy json_spec parameter
    elif hasattr(input.params, 'json_spec') and input.params.json_spec:
        cmd.extend(['-j', input.params.json_spec])
    # Fall back to modules
    else:
        for m in input.params.modules:
            cmd.extend(['-m', m])

    if input.params.pkgname:
        cmd.extend(['--package', input.params.pkgname])

    filename = input.params.filename

    if filename.strip() == "":
        if input.params.pkgname.strip() != "":
            filename = input.params.pkgname.strip() + ".sv"
        else:
            filename = "pyhdl_api_pkg.sv"

    cmd.extend(['-o', os.path.join(input.rundir, filename)])

    status |= await runner.exec(cmd, env=env)

    output = []
    output.append(FileSet(
        basedir=input.rundir,
        files=[filename],
        filetype="systemVerilogSource"
    ))

    return TaskDataResult(
        status=status,
        output=output
    )
