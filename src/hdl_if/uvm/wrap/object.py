
import ctypes
from typing import Generic, TypeVar, List, Optional
from ...decorators import api, imp, exp
from ..object import uvm_object as uvm_object_p
from ..visitor import uvm_visitor
from .object_type import UvmObjectType

@api
class uvm_object(uvm_object_p):
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

    def __init__(self):
        super().__init__()
        self._uvm_obj_t : Optional[UvmObjectType] = None
        pass

    # def __getattr__(self, name):
    #     pass

    # def __setattr__(self, name, value):
    #     pass

    def __del__(self):
        print("__del__", flush=True)

    def __getattr__(self, name):
        obj_t = object.__getattribute__(self, "_uvm_obj_t")
        if name in obj_t.field_m.keys():
            pack = self.pack()
            return getattr(pack, name)
        else:
            raise AttributeError("Field %s not found in %s (%s)" % (
                name, 
                str(self),
                ",".join([f.name for f in obj_t.fields])))
        
    def __setattr__(self, name: str, value):
        try:
            obj_t = object.__getattribute__(self, "_uvm_obj_t")
        except:
            obj_t = None
        if name in ("_uvm_obj_t",) or obj_t is None or name not in obj_t.field_m.keys():
            object.__setattr__(self, name, value)
        else:
            pack = self.pack()
            setattr(pack, name, value)
            self.unpack(pack)

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

    @imp
    def reseed(self) -> None:
        """
        Reseeds this object's RNG via the backend using UVM seeding rules.
        """
        pass

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
    def set_name(self, name: str) -> None:
        """
        Sets the object's leaf instance name in the backend.
        """
        ...

    @imp
    def get_inst_id(self) -> int:
        """
        Returns the unique instance ID assigned by the backend.
        """
        ...

    @imp
    def get_type_name(self) -> str: ...

    @imp
    def create(self, name: str = "") -> uvm_object_p: ...

    @imp
    def clone(self) -> uvm_object_p: ...

    @imp
    def print(self) -> None: ...

    @imp
    def convert2string(self) -> str: ...

    @imp
    def record(self) -> None: ...

    @imp
    def copy(self, rhs: uvm_object_p) -> None: ...

    @imp
    def compare(self, rhs: uvm_object_p) -> bool: ...

    @imp
    def set_int_local(self, name: str, value: int) -> None: ...

    @imp
    def set_string_local(self, name: str, value: str) -> None: ...

    @imp
    def set_object_local(self, name: str, value: uvm_object_p) -> None: ...

    @imp
    def get_inst_count(self) -> int:
        """
        Returns the number of instances created for this object's type in the backend.
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

    @imp
    def get_full_name(self) -> str:
        """
        Returns the full hierarchical name for components; for plain objects,
        this typically matches get_name().
        """
        ...

    def pack(self) -> object: 
        """Packs field values of the SystemVerilog object into a Python object"""
        data = self.pack_ints()
        return getattr(self, "_uvm_obj_t").unpack_ints(data)
        ...

    @imp
    def pack_ints(self) -> List[int]:
        ...

    def unpack(self, val : object):
        """Sets the field values of the SystemVerilog object from a Python object"""
        data = getattr(self, "_uvm_obj_t").pack_ints(val)
        self.unpack_ints(data)
        ...

    @imp
    def unpack_ints(self, data : List[int]):
        ...

    def accept(self, v : uvm_visitor):
        v.visit_object(self)
