# Python Output Flushing Implementation

## Overview

Python buffers its output streams (stdout and stderr) by default. This buffering can make it difficult to correlate Python execution with SystemVerilog execution, as Python print statements may not appear in the output until the buffer is full or the program exits.

## Solution

Implemented automatic flushing of Python output streams whenever control passes from Python to SystemVerilog. This ensures that Python output is visible before SystemVerilog execution continues.

## Implementation Details

### Core Flushing Function

A new utility module `src/hdl_if/impl/output_flush.py` provides the `flush_output()` function:

```python
def flush_output():
    """
    Flush all Python output streams to ensure output is visible before
    control passes to SystemVerilog.
    """
    sys.stdout.flush()
    sys.stderr.flush()
```

### Integration Points

The flushing strategy is integrated at key control transfer points:

1. **DPI Function Calls** (`src/hdl_if/impl/call/hdl_call_endpoint_dpi.py`):
   - `invoke_hdl_f()` - Before Python calls a SystemVerilog function
   - `invoke_hdl_t()` - Before Python calls a SystemVerilog task
   - `response_py_t()` - After Python posts response from async call to SystemVerilog (flush AFTER posting to avoid deadlocks in single-threaded simulators like Verilator)

2. **VPI Task Calls** (`src/hdl_if/impl/vpi/call_proxy_vpi.py`):
   - `invoke_hdl_t()` - Before Python calls a SystemVerilog task via VPI

**Note**: Flushing is intentionally NOT done in `Backend.idle()` as this is called frequently during event loop processing and would cause performance issues.

### Threading Considerations

The implementation accounts for differences between simulators:
- **ModelSim/Questa**: DPI calls can trigger thread swaps, so flush timing is less critical
- **Verilator**: Runs single-threaded, so flushes must occur AFTER posting semaphores/responses to avoid deadlocks

### No Changes to Generated Code

Importantly, no changes were made to generated files (e.g., DPI wrappers). All flushing logic is contained within the Python runtime infrastructure.

## Testing

A comprehensive test suite was added in `tests/unit/test_flush.py` that validates:
- Python print statements appear before corresponding SystemVerilog $display output
- Proper interleaving of Python and SystemVerilog output
- No regression in existing functionality

The test creates a scenario where Python code prints messages, calls SystemVerilog functions, and prints more messages. The output demonstrates proper chronological ordering.

## Benefits

- **Improved Debugging**: Developers can now see Python output in real-time as it occurs
- **Better Correlation**: Easy to correlate Python execution with SystemVerilog execution
- **No User Action Required**: Automatic flushing works without any code changes from users
- **Minimal Performance Impact**: Flushing occurs only at control transfer boundaries
