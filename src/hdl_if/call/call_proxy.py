#****************************************************************************
#* call_proxy.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************

"""Per-object dispatch between Python and HDL method calls."""


class CallProxy(object):
    """Routes method calls between one Python object and its HDL counterpart.

    Where :class:`~hdl_if.call.hdl_call_endpoint.HdlCallEndpoint` is the
    channel to a simulator, a proxy is bound to a single interface object and
    dispatches its calls in both directions: ``invoke_hdl_*`` sends a call to
    SystemVerilog, ``invoke_py_*`` is how SystemVerilog calls in.

    Subclasses implement the transport-specific halves; the base class
    implements only :meth:`invoke_py_f`, which is pure Python dispatch.

    Args:
        obj: The Python object whose methods this proxy dispatches to.
    """

    def __init__(self, obj):
        self.target = obj
        pass

    async def invoke_hdl_t(
            self,
            method_name : str,
            args : tuple):
        """Call an HDL task and await its completion.

        Args:
            method_name: Name of the task to call.
            args: Positional arguments.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("CallProxy.invoke_hdl_t: %s" % str(type(self)))

    def invoke_hdl_f(
            self,
            method_name : str,
            args : tuple):
        """Call an HDL function and return its result.

        Args:
            method_name: Name of the function to call.
            args: Positional arguments.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("CallProxy.invoke_hdl_f: %s" % str(type(self)))

    def response_hdl_t(
            self,
            call_id : int,
            result : object):
        """Deliver the result of an HDL task back to the Python caller.

        Called by the HDL environment when a task started with
        :meth:`invoke_hdl_t` completes.

        Args:
            call_id: Identifier of the call being completed.
            result: The value the task returned.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("CallProxy.response_hdl_t: %s" % str(type(self)))

    def invoke_py_f(
            self,
            method_name : str,
            args : tuple) -> object:
        """Invoke a Python method on behalf of the HDL environment.

        Args:
            method_name: Name of the method to call on the target object.
            args: Positional arguments.

        Returns:
            Whatever the method returned.

        Raises:
            Exception: If the target object has no such method.
        """
        m = getattr(self.target, method_name, None)

        if m is None:
            raise Exception("Failed to find method %s" % method_name)

        return m(*args)

    def invoke_py_t(
            self,
            method_name : str,
            args : tuple) -> int:
        """Start a Python coroutine on behalf of the HDL environment.

        Args:
            method_name: Name of the coroutine method to start.
            args: Positional arguments.

        Returns:
            An identifier for the started call, to be matched by
            :meth:`response_py_t`.
        """
        pass

    def response_py_t(
            self,
            call_id : int,
            result : object):
        """Deliver the result of a Python task back to the HDL caller.

        Args:
            call_id: Identifier returned by :meth:`invoke_py_t`.
            result: The value to return.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("CallProxy.response_py_t: %s" % str(type(self)))

