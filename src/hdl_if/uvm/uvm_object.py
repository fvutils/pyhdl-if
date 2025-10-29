
import ctypes
from typing import Generic, TypeVar, List
from ..decorators import api, imp, exp

@api
class UvmObject(object):
    """
    Base for UVM-style data objects in this Python HDL interface.

    Purpose:

    - Identification: leaf and, optionally, full hierarchical names (reported by the SV backend).
    - Visualization: string formatting compatible with UVM printer behavior.
    - Randomization: backend-driven field randomization via ``_randomize()``.

    Notes:

    - SystemVerilog ``uvm_object`` defines broader APIs (create/copy/compare/print/record/pack/unpack).
      This adapter exposes a minimal subset and delegates to the SV side.
    - In SV, ``get_full_name`` defaults to ``get_name`` for objects without hierarchy; components override it.
    """

    def randomize(self) -> None:
        """
        Randomizes this object via the backend.

        Behavior:

        - Calls the implementation hook ``_randomize()``.
        - Raises ``Exception`` if randomization fails.

        UVM alignment:

        - Mirrors the UVM object randomization flow; seeding policy is handled on the SV side.
        """
        if not self._randomize():
            raise Exception("Randomization failed")

    # Implementation detail
    @imp
    def _randomize(self) -> bool: ...

    @imp
    def get_name(self) -> str: 
        """
        Returns the leaf instance name of this object.

        Notes:

        - Typically set by construction or ``set_name`` on the SV side.
        - Objects (non-components) generally do not maintain hierarchy; see components for full names.
        """
        ...

    @imp
    def sprint(self) -> str: 
        """
        Returns a formatted string representation of this object.

        Behavior:

        - Mirrors UVM sprint semantics: produces the printable view without emitting to output.
        - Formatting policy (printer) is controlled in SV.
        """
        ...

    def pack(self) -> object: 
        """Packs field values of the SystemVerilog object into a Python object"""
        data = self.pack_ints()
        return getattr(self, "obj_t").unpack_ints(data)
        ...

    @imp
    def pack_ints(self) -> List[int]:
        ...

    def unpack(self, val : object):
        """Sets the field values of the SystemVerilog object from a Python object"""
        data = getattr(self, "obj_t").pack_ints(val)
        self.unpack_ints(data)
        ...

    @imp
    def unpack_ints(self, data : List[int]):
        ...
