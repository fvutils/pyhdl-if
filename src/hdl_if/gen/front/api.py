#****************************************************************************
#* api.py
#*
#* Copyright 2026 Matthew Ballance and Contributors
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
#****************************************************************************
"""Maps an ``@api`` class onto the neutral description.

An ``@api`` class fixes, per method, which side implements it: ``@imp``
methods are implemented in SystemVerilog, ``@exp`` methods in Python. The
neutral form has no direction, so the result is an interface plus the
implementer of each method.

This is for tools that want to treat existing APIs uniformly. ``api-gen-sv``
does not use it: its output is unchanged.
"""
from typing import Dict, Optional, Tuple

from ..ir import InterfaceDef, MethodDef, ParamDef, TypeUniverse, IrError
from .py import PyFrontEnd
from ...impl.call.method_def import MethodKind

__all__ = ["IMPL_SV", "IMPL_PY", "interface_from_api"]

#: The method is implemented in SystemVerilog (``@imp``).
IMPL_SV = "sv"
#: The method is implemented in Python (``@exp``).
IMPL_PY = "py"

_KIND = {
    MethodKind.ImpTask: (True, IMPL_SV),
    MethodKind.ImpFunc: (False, IMPL_SV),
    MethodKind.ExpTask: (True, IMPL_PY),
    MethodKind.ExpFunc: (False, IMPL_PY),
}


def interface_from_api(api_def, fe: Optional[PyFrontEnd] = None
                       ) -> Tuple[InterfaceDef, Dict[str, str]]:
    """Convert an ``ApiDef`` into an interface and per-method implementers.

    Args:
        api_def: An ``hdl_if.impl.call.api_def.ApiDef`` (as registered by
            ``@api``).
        fe: The Python front end to add record and enum types to. A new one
            is used if not given; its universe holds the types the interface
            uses.

    Returns:
        ``(interface, implementers)``, where ``implementers`` maps each
        method name to :data:`IMPL_SV` or :data:`IMPL_PY`. The interface is
        added to ``fe.u``.

    Raises:
        IrError: If a parameter type has no equivalent (for example a
            ``ctypes.Structure`` or ``ctypes.py_object``; use a dataclass or
            an interface instead).
    """
    if fe is None:
        fe = PyFrontEnd()
    idef = InterfaceDef(api_def.name)
    impl = {}
    for m in api_def.methods:
        if m.kind not in _KIND:
            raise IrError("%s.%s: unexpected method kind %s" % (
                api_def.fullname, m.name, str(m.kind)))
        is_task, who = _KIND[m.kind]
        what = "%s.%s" % (api_def.fullname, m.name)
        md = MethodDef(m.name, is_task=is_task)
        for pname, ptype in m.params:
            md.params.append(ParamDef(pname, fe.map_hint(ptype, "%s parameter %s" % (what, pname))))
        if m.rtype is not None and m.rtype is not type(None):
            md.rtype = fe.map_hint(m.rtype, "%s return" % what)
        idef.methods.append(md)
        impl[m.name] = who
    fe.u.add(idef)
    return idef, impl
