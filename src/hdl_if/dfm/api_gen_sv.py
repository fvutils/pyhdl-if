import os
import sys
from dv_flow.mgr import TaskRunCtxt, TaskDataInput, TaskDataResult, FileSet

async def APIGenSV(runner, input) -> None:

    env = runner.env.copy()

    if input.params.pythonpath:
        for path in input.params.pythonpath:
            if "PYTHONPATH" not in env:
                env["PYTHONPATH"] = path
            else:
                env["PYTHONPATH"] += os.pathsep + path

    status = 0
    
    cmd = [
        sys.executable,
        '-m', 'hdl_if',
        'api-gen-sv'
    ]

    for m in input.params.modules:
        cmd.extend(['-m', m])

    if input.params.pkgname:
        cmd.extend(['--package', input.params.pkgname])
    
    filename = input.params.filename

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