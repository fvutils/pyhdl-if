####################
Python API Reference
####################

This is the reference for the Python side of PyHDL-IF. For the SystemVerilog
side, see :doc:`sv_api`; for task-oriented material, start from
:doc:`quickstart` or :doc:`theory_of_op`.

Only the public surface is documented here. Anything under ``hdl_if.impl`` and
``hdl_if.uvm.wrap`` is an implementation detail and may change without notice.

.. currentmodule:: hdl_if

Interface declaration
*********************

The decorators are the primary API and are normally reached through the
package namespace as ``hif.api``, ``hif.imp`` and so on.

.. autosummary::

   api
   imp
   exp
   tlm_if
   req_fifo
   rsp_fifo
   reqrsp_fifo

.. automodule:: hdl_if.decorators
   :members: api, imp, exp, tlm_if, req_fifo, rsp_fifo, reqrsp_fifo, req_mbox, rsp_mbox

Package layout
**************

Helpers for locating the artifacts a simulator needs -- the shared library and
the shipped SystemVerilog sources.

.. autofunction:: hdl_if.get_entry

.. autofunction:: hdl_if.share

.. autofunction:: hdl_if.root

.. autofunction:: hdl_if.libs

.. autofunction:: hdl_if.get_backend

Runtime services
****************

.. automodule:: hdl_if.backend
   :members:

.. automodule:: hdl_if.hdl_obj_rgy
   :members:

.. automodule:: hdl_if.hdl_services
   :members:

Call interface
**************

The runtime objects behind an :func:`~hdl_if.decorators.api` interface.

.. automodule:: hdl_if.call.hdl_call_endpoint
   :members:

.. automodule:: hdl_if.call.call_proxy
   :members:

TLM interface
*************

.. automodule:: hdl_if.tlm.tlm_ifc
   :members:

.. automodule:: hdl_if.tlm.tlm_method
   :members:

.. automodule:: hdl_if.tlm.tlm_ifc_rgy
   :members:

.. automodule:: hdl_if.tlm.stream_rgy
   :members:

pytest runner
*************

See :doc:`pytest_runner` for the guide.

.. automodule:: hdl_if.pytest_runner
   :members:

UVM
***

See :doc:`uvm` for the guide and the class reference.
