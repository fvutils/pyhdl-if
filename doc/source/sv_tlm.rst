###############
TLM FIFO Layer
###############

The TLM layer moves *transactions* between Python and the design, rather than
calls. Where the call API has Python invoking a SystemVerilog task and waiting
for it to return, a TLM FIFO decouples the two sides: Python pushes an entry and
carries on, the design consumes entries at its own rate, and the FIFO absorbs
the difference.

These are the only pyhdl-if constructs you *instantiate*. Everything else in the
SystemVerilog API is a class you call or extend.

Choosing an interface
=====================

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Interface
     - Direction
     - Use when
   * - :sv:mod:`tlm_hvl2hdl_fifo`
     - Python → design
     - Python generates stimulus the design consumes.
   * - :sv:mod:`tlm_hdl2hvl_fifo`
     - Design → Python
     - The design produces results Python collects.
   * - :sv:mod:`pyhdl_if_reqrsp_fifo`
     - Both
     - A request is answered by a response, and the pairing matters.

All three register themselves as a named stream at time zero, under the
interface's own hierarchical path (``$sformatf("%m")``). That path is what the
Python side binds against, so an instance needs no configuration beyond where
you put it.

Connecting the design side
==========================

Each FIFO presents a ``valid``/``ready`` pair plus a data port, synchronous to
``clock`` and held in reset while ``reset`` is asserted::

   tlm_hvl2hdl_fifo #(.Twidth(64), .Tdepth(4)) u_req (
       .clock(clk), .reset(rst),
       .valid(in_valid), .ready(in_ready), .dat_o(in_data));

``Twidth`` must match the packed width of the Python structure bound to the
stream. Widths above 64 bits are not yet supported and terminate the simulation
at run time.

Blocking and the GIL
====================

A FIFO's ``put`` and ``get`` block on simulation time -- they wait for a clock
edge, and then for the other side to make room or supply data. The Python
interpreter lock is released across those waits and re-acquired afterwards, so a
blocked transfer does not stall unrelated Python threads.

This matters when reading the source: ``Closure::invokeTask`` takes the GIL
state as an ``inout`` argument precisely so it can hand it back for the duration
of a blocking wait. A transfer that held the lock while waiting for a clock edge
would deadlock against the Python thread that was supposed to satisfy it.

Interface Reference
===================

.. autosvmodule:: tlm_hvl2hdl_fifo
   :members:

.. autosvmodule:: tlm_hdl2hvl_fifo
   :members:

.. autosvmodule:: pyhdl_if_reqrsp_fifo
   :members:
