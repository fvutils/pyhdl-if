import os
from dv_flow.mgr import TaskDataInput, TaskRunCtxt, TaskDataResult, FileSet

async def DpiLib(ctxt : TaskRunCtxt, input : TaskDataInput) -> TaskDataResult:
    from hdl_if import get_entry
    entry = get_entry()

    return TaskDataResult(
        status=0,
        output=[
            FileSet(
                filetype="systemVerilogDPI",
                basedir=os.path.dirname(entry),
                files=[os.path.basename(entry)])
        ]
    )
