#****************************************************************************
#* hdl_call_endpoint.py
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

"""The Python end of a simulator call channel."""


class HdlCallEndpoint(object):
    """Python end of the call channel to a simulator.

    One endpoint exists per foreign interface in use. It is what actually
    carries an :func:`~hdl_if.decorators.exp` call across to SystemVerilog, and
    what the simulator calls back into for an
    :func:`~hdl_if.decorators.imp` method. Subclasses implement the transport;
    the base class raises :class:`NotImplementedError` for each operation.

    Applications do not normally construct or call an endpoint directly --
    the decorators route through it.

    Args:
        name: Name of the endpoint, identifying the foreign interface.
    """

    def __init__(self, name):
        from hdl_if.hdl_obj_rgy import HdlObjRgy
        self._name = name
        self._backend = None
        self._obj_rgy = HdlObjRgy.inst()

    @property
    def name(self):
        """The endpoint's name."""
        return self._name

    @property
    def backend(self):
        """The :class:`~hdl_if.backend.Backend` this endpoint runs on.

        Resolved on first access and cached.
        """
        from hdl_if.backend import Backend
        if self._backend is None:
            self._backend = Backend.inst()
        return self._backend

    def idle(self):
        """Yield to the backend scheduler."""
        be = self.backend

    def invoke_hdl_f(self, obj_id : int, method_name : str, args : tuple):
        """Call a SystemVerilog function and return its result.

        Args:
            obj_id: Identifier of the target HDL object.
            method_name: Name of the method to call.
            args: Positional arguments.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("Class %s doesn't implement invoke_hdl_f" % str(type(self)))

    def invoke_hdl_t(self,
                     obj_id,
                     evt_obj,
                     method_name,
                     args):
        """Call a SystemVerilog task, which may consume simulation time.

        Args:
            obj_id: Identifier of the target HDL object.
            evt_obj: Event signalled when the task completes.
            method_name: Name of the method to call.
            args: Positional arguments.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("Class %s doesn't implement invoke_hdl_t" % str(type(self)))

    def response_py_t(self, sem_id, res):
        """Deliver the result of a Python task back to the caller.

        Args:
            sem_id: Identifier of the waiting call.
            res: The value to return.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("Class %s doesn't implement response_py_t" % str(type(self)))

    def newObj(self, cls_t, obj_id, args):
        """Construct the HDL-side counterpart of an interface object.

        Args:
            cls_t: The interface class being constructed.
            obj_id: Identifier to bind the new object to.
            args: Constructor arguments.

        Raises:
            NotImplementedError: Always, on the base class.
        """
        raise NotImplementedError("Class %s doesn't implement newObj" % str(type(self)))

    def registerObj(self, obj, inst_path, trim_elems=0):
        """Register an object against an HDL instance path.

        Args:
            obj: The object to register.
            inst_path: The instance path reported by the simulator.
            trim_elems: Number of trailing path elements to drop before
                registering. Use this when the simulator reports the path of a
                nested scope but the object belongs to an enclosing one.

        See Also:
            :meth:`HdlObjRgy.registerObj <hdl_if.hdl_obj_rgy.HdlObjRgy.registerObj>`
        """
        if trim_elems:
            path_s = inst_path.split(".")
            path_s = path_s[:-trim_elems]
            inst_path = ".".join(path_s)
        self._obj_rgy.registerObj(obj, inst_path)
    
    



