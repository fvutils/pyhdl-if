############################
PyHDL-IF Theory of Operation
############################

*****************************
PyHDL-IF Library Fundamentals
*****************************

PyHDL-IF implements a function- and task-based interface with the simulator
using three core components:

* Python library
* SystemVerilog library
* DPI library

These three components provide APIs that are used to create linked pairs of
Python and SystemVerilog objects. Each object in the pair is responsible for 
implementing and responding to method invocation requests from its peer
object.

Startup Behavior
================
On startup, the simulator initializes the pyhdl_if package by calling
`__pyhdl_if_init`. This method loads the DPI library, initializes the
Python interpreter, and loads the Python portion of the PyHDL-IF library.
The pyhdl_if SystemVerilog package calls `hdl_if.impl.dpi.dpi_init` as
a step in the startup process. This method returns an HdlCallEndpointDPI
object that allows the Python and SystemVerilog portions of the 
implementation to coordinate.

Connecting Peer Objects
=======================

The Python and SystemVerilog peer objects may be created in any manner. 
Before they can be used as a pair, though, they must be connected. This 
is done by passing both the SystemVerilog and Python objects to 
`pyhdl_if_connectObject`. This method allocates a unique integer 
identifier for the SystemVerilog object and calls `connectObj` on 
the endpoint (ie HdlCallEndpointDPI), passing the Python object and
the unique identifier for the SystemVerilog object.

Calling a Python Method from SystemVerilog
==========================================

Synchronous Python methods (functions) are called from SystemVerilog using
`pyhdl_if_invokePyFunc`. This function:

1. Acquires the Python GIL via `PyGILState_Ensure`
2. Retrieves the `_proxy` attribute from the Python object
3. Calls `invoke_py_f` on the proxy with the method name and arguments
4. Releases the GIL and returns the result

Since Python functions are non-blocking, the call completes synchronously
within the SystemVerilog function context.

Calling a Python Async Method from SystemVerilog
================================================

Calling an async Python method from a SystemVerilog task is more complex
because it requires bridging the SystemVerilog simulation thread with
Python's asyncio event loop. The mechanism works as follows:

1. **SV Task calls `pyhdl_if_invokePyTask`**: This allocates a semaphore ID
   using `pyhdl_if_allocSem` to track the call's completion.

2. **Invoke Python proxy**: The task retrieves the `_proxy` attribute from 
   the Python object and calls `invoke_py_t` with the semaphore ID, method 
   name, and arguments.

3. **Python creates async task**: `CallProxyDPI.invoke_py_t` retrieves the
   target method and calls `Backend.mkTask()` with `invoke_py_t_wrap()`.
   This schedules the coroutine on the asyncio event loop.

4. **Run event loop**: `Backend.idle()` is called, which runs the asyncio
   event loop until the next stopping point via `run_forever()` and 
   `call_soon(stop)`.

5. **SV waits on semaphore**: Back in SystemVerilog, `pyhdl_if_waitSem` 
   blocks on the semaphore, waiting for the Python async method to complete.

6. **Python method completes**: When the async method finishes, 
   `invoke_py_t_wrap` calls `response_py_t` on the endpoint.

7. **Signal completion**: `HdlCallEndpointDPI.response_py_t` calls the DPI
   export function `pyhdl_call_if_response_py_t`, which calls 
   `pyhdl_if_setSem` to put the result in the semaphore array and signal 
   the semaphore.

8. **SV task resumes**: The semaphore unblocks, `pyhdl_if_waitSem` returns
   the result, and the SystemVerilog task continues.

Calling a SystemVerilog Function from Python
============================================

Python code calls SystemVerilog functions through the `CallProxyDPI` class:

1. **Python calls `invoke_hdl_f`**: The proxy's `invoke_hdl_f` method is
   called with the method name and arguments.

2. **DPI call to SV**: `HdlCallEndpointDPI.invoke_hdl_f` uses ctypes to
   call the DPI export function `pyhdl_call_if_invoke_hdl_f` directly.

3. **SV function dispatch**: The exported function looks up the SV object
   by `obj_id` in the `__objects` array and calls `invokeFunc` on the
   `ICallApi` interface.

4. **Result returned**: The function result is returned through DPI back
   to Python.

This is a straightforward synchronous call since SystemVerilog functions
cannot consume simulation time.

Calling a SystemVerilog Task from Python
========================================

Calling a SystemVerilog task from Python requires special handling because
SV tasks can consume simulation time, while Python async methods expect to
await completion. The mechanism works as follows:

1. **Python calls `invoke_hdl_t`**: This is an async method on 
   `CallProxyDPI`. It creates an asyncio Event object via `Backend.mkEvent()`
   to track completion.

2. **DPI call to queue task**: `HdlCallEndpointDPI.invoke_hdl_t` calls
   the DPI export `pyhdl_call_if_invoke_hdl_t` with the object ID, event
   object, method name, and arguments.

3. **Create TaskCallClosure**: The SV function creates a `TaskCallClosure`
   object that implements `PyHdlPiRunnable`. This closure captures the
   target object, event, method name, and arguments.

4. **Queue for execution**: The closure is passed to 
   `pyhdl_pi_if_queue_runnable`, which adds it to the `prv_run_q` mailbox.

5. **Python awaits event**: Back in Python, `invoke_hdl_t` awaits the
   event with `res = await evt.wait()`.

6. **SV event loop executes task**: The `__pyhdl_pi_if_run` task 
   continuously pulls runnables from the mailbox and forks them for
   execution. This allows multiple SV tasks to run concurrently.

7. **TaskCallClosure runs**: The closure's `run` task:
   
   a. Acquires the Python GIL
   b. Calls `invokeTask` on the `ICallApi` interface to execute the 
      actual SystemVerilog task
   c. Retrieves the `set` method from the Python event object
   d. Calls `evt.set(result)` to signal completion with the return value
   e. Releases the GIL

8. **Event signaled**: The `Event.set()` method stores the result value
   and signals the asyncio event, also calling `Backend.idle()` to 
   advance the Python event loop.

9. **Python resumes**: The awaiting coroutine receives the result from
   `evt.wait()` and continues execution.

Key Design Elements
===================

**SV Event Loop**: The `__pyhdl_pi_if_run` task runs as a forever loop,
pulling runnables from a mailbox and forking each one. This is essential
because it allows Python-initiated tasks to execute within the simulation
time domain while the Python event loop remains responsive.

**Semaphore Pool**: For SV-to-Python async calls, a pool of semaphores
(`__callsem`) tracks pending calls. Each call allocates a semaphore ID,
and completion signals that specific semaphore.

**Event Objects**: For Python-to-SV task calls, Python's asyncio Event
objects are passed to SystemVerilog. The SV task closure holds a reference
and calls the event's `set` method when complete.

**GIL Management**: Both directions carefully manage Python's Global
Interpreter Lock (GIL) using `PyGILState_Ensure` and `PyGILState_Release`
to ensure thread safety when crossing the Python/C/SV boundary.

**Backend Abstraction**: The `Backend` class abstracts the asyncio 
operations, allowing different backends (asyncio, cocotb) while maintaining
the same call semantics.

Python Thread Support
=====================

PyHDL-IF supports Python threads that need to call back into SystemVerilog
tasks. This is useful when integrating with Python libraries that use 
threading for blocking I/O or compute-intensive operations.

The challenge with threads is that:

1. Python threads need the GIL (Global Interpreter Lock) to execute Python code
2. The asyncio event loop runs in the main thread  
3. SystemVerilog tasks execute in the simulation thread
4. A thread calling `run_coroutine_threadsafe()` schedules work but blocks
   waiting for the result

The solution involves a two-part approach: an up-front event loop pump when
invoking async methods, and a background polling thread for ongoing 
asynchronous Python activity.

Up-Front Event Loop Pump
------------------------

When SystemVerilog calls a Python async method via ``pyhdl_if_invokePyTask``,
the implementation pumps the Python event loop up to a configurable number of
times (default: 10) *before* advancing simulation time. This allows threaded
Python code to initiate callbacks into SystemVerilog without any simulation
time passing:

.. code-block:: systemverilog

    // Pump event loop up-front to allow threads to initiate SV callbacks
    repeat (__py_poll_upfront_count) begin
        pyhdl_pi_if_idle();
        if (__callsem[id].try_get()) begin
            // Early completion - no time advanced
            break;
        end
    end

This is critical because:

1. Threaded Python code typically calls back into SV very quickly
2. We don't want to advance simulation time during this initial setup phase
3. Most SV→Python→SV round-trips complete within a few event loop iterations

Background Polling Thread
-------------------------

For ongoing asynchronous Python activity (such as user interactions or 
background I/O), a separate SystemVerilog thread polls the Python event
loop at regular intervals. This polling thread:

1. Starts automatically when ``pyhdl_if_start()`` is called
2. Adjusts its simulation-time wait based on real-time elapsed since last poll
3. Targets a configurable real-time interval (default: 100ms)

The polling algorithm uses adaptive timing:

.. code-block:: systemverilog

    forever begin
        // Wait simulation time
        #(__py_poll_sim_time);
        
        // Get current real time and compare to target
        current_real_time = get_real_time_ms();
        elapsed = current_real_time - last_poll_real_time;
        
        // Pump the Python event loop
        pyhdl_pi_if_idle();
        
        // Adjust next simulation wait based on real-time performance
        if (elapsed > target_real_time_ms) begin
            // Real time is passing faster than sim time - decrease wait
            __py_poll_sim_time = __py_poll_sim_time / 2;
        end else if (elapsed < target_real_time_ms / 2) begin
            // Sim time is passing faster than real time - increase wait
            __py_poll_sim_time = __py_poll_sim_time * 2;
        end
        
        last_poll_real_time = current_real_time;
    end

This adaptive approach ensures responsive Python interaction regardless of
simulation speed.

Configuration Plusargs
----------------------

The polling behavior is configurable via plusargs:

- ``+pyhdl.poll_upfront_count=N``: Number of event loop iterations before
  advancing simulation time (default: 10)
- ``+pyhdl.poll_sim_time=N``: Initial simulation time in time units between
  background polls (default: 1000)
- ``+pyhdl.poll_real_time_ms=N``: Target real-time interval in milliseconds
  between background polls (default: 100)

Wait Semaphore Implementation
-----------------------------

The wait semaphore implementation uses a two-phase approach to balance
performance with thread support:

.. code-block:: systemverilog

    // Phase 1: Up-front pump (no simulation time advancement)
    // Fast path for pure asyncio calls
    repeat (__py_poll_upfront_count) begin
        pyhdl_pi_if_idle();
        if (__callsem[id].try_get()) begin
            // Early completion - no time advanced
            return;
        end
    end

    // Phase 2: Slower path for threaded calls
    // Release GIL and wait to allow Python threads to run
    while (!__callsem[id].try_get()) begin
        PyGILState_Release(state);
        #(__py_poll_sim_time);
        state = PyGILState_Ensure();
        pyhdl_pi_if_idle();
    end

This design ensures:

1. Pure asyncio calls complete with no simulation time advancement
2. Threaded calls (via ``run_coroutine_threadsafe``) get OS scheduler time
3. The GIL is released to allow Python threads to run

**Using asyncio.to_thread**: Python code that needs to run blocking work
in a thread while calling back to SystemVerilog should use 
``asyncio.to_thread()``:

.. code-block:: python

    @hif.api
    class MyTest(object):
        @hif.exp
        async def run(self, bfm):
            # Get event loop reference for thread
            loop = asyncio.get_event_loop()
            
            def blocking_work():
                # Schedule SV call from thread
                future = asyncio.run_coroutine_threadsafe(
                    bfm.some_task(), loop)
                return future.result(timeout=30.0)
            
            # Run blocking work in thread
            result = await asyncio.to_thread(blocking_work)

The ``await asyncio.to_thread()`` keeps the main async method suspended,
allowing the polling loop to pump the event loop and process the thread's
scheduled coroutines.

*************************
SystemVerilog API Classes
*************************

The `api-gen-sv` command generates convenience classes to enable
calling `exp` methods from SystemVerilog and to allow SystemVerilog
classes to implement `imp` methods.

.. code-block:: python3

    class 


*************************
SystemVerilog UVM Classes
*************************

PyHDL-IF provides built-in support for interacting with SystemVerilog UVM
testbench environments. The following classes exist for each UVM class:

* Python `Protocol` class in hdl_if.uvm that defines the available methods. 
  Note that these classes are not marked with @api, @imp, or @exp.
* Python implementation classes in hdl_if.uvm.wrap that implement the 
  interface to SystemVerilog. 
* SystemVerilog interface class in hdl_if/share/uvm/pyhdl_uvm_<name>.svh 
  that implements the conversion between SystemVerilog types and Python
  types when necessary.
* SystemVerilog wrapper class in hdl_if/share/uvm/pyhdl_uvm_<name>.svh
  named pyhdl_uvm_<name>_w. This class extends from the generated SV/Python
  integration 'imp' implementation class, and implements pyhdl_uvm_object_if.

In general, SystemVerilog inout method parameters are implemented as
return values of the Python method.


