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
#        '--deprecated'
    ]

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
