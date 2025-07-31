import os
import sys
from dv_flow.mgr import TaskDataInput, TaskRunCtxt, TaskDataResult, FileSet

async def DpiLib(ctxt : TaskRunCtxt, input : TaskDataInput) -> TaskDataResult:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    hdl_if_pdir = os.path.dirname(os.path.dirname(thisdir))

    if hdl_if_pdir not in sys.path:
        sys.path.insert(0, hdl_if_pdir)
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
