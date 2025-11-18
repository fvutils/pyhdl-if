import os
import sys
from dv_flow.mgr import TaskRunCtxt, TaskDataInput, TaskDataResult, FileSet

async def SvPkg(ctxt: TaskRunCtxt, input: TaskDataInput) -> TaskDataResult:
    """
    Task to return the SystemVerilog package file for the HDL interface.
    
    Args:
        ctxt (TaskRunCtxt): The task run context.
        input (TaskDataInput): The task input data.

    Returns:
        TaskDataResult: The result containing the package file.
    """
    thisdir = os.path.dirname(os.path.abspath(__file__))
    hdl_if_pdir = os.path.dirname(os.path.dirname(thisdir))

    if hdl_if_pdir not in sys.path:
        sys.path.insert(0, hdl_if_pdir)
    from hdl_if import share
    sharedir = share()

    return TaskDataResult(
        status=0,
        output=[
            FileSet(
                filetype="systemVerilogSource",
                basedir=os.path.join(sharedir, "dpi"),
                files=["pyhdl_if.sv"],
                incdirs=["."],
                defines=["HAVE_PYHDL_IF"]
            )
        ]
    )