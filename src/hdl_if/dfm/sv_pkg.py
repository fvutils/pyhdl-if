import os
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
    from hdl_if import share
    sharedir = share()

    return TaskDataResult(
        status=0,
        output=[
            FileSet(
                filetype="systemVerilogSource",
                basedir=os.path.join(sharedir, "dpi"),
                files=["pyhdl_if.sv"]
            )
        ]
    )