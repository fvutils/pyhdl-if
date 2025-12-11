from __future__ import annotations
from ...decorators import api, imp
from typing import List, Tuple, cast
from .object import uvm_object as uvm_object_w
from ..component import uvm_component as uvm_component_p
from ..object import uvm_object
from ..visitor import uvm_visitor

@api
class uvm_component(uvm_object_w):
    """
    Root base for structural UVM components.

    Provides (via SV backend):

    - Hierarchy: parent/child relationships and hierarchical names.
    - Phasing: build/connect/run/report-style phase callbacks along the UVM schedule.
    - Reporting/Factory/Recording: convenience access through SV UVM infrastructure.

    Adapter scope:

    - This Python API exposes a subset of queries/utilities.
    - Phase execution, reporting, and factory behavior are managed by the SV side.
    """

    def __init__(self):
        super().__init__()
        self._child_m = None


    # def randomize(self) -> bool:
    #     """
    #     Randomizes this component via the backend.

    #     :returns: True on success, False otherwise.

    #     Notes:

    #     - UVM seeding for components is applied during construction in SV when enabled.
    #     - This call triggers backend-specific randomization of fields/knobs.
    #     """
    #     return self._randomize()

    # # Implementation detail
    # @imp
    # def _randomize(self) -> bool:
    #     """
    #     Backend hook invoked by ``randomize()``.

    #     :returns: True on success, False on failure.
    #     """
    #     ...

    # @imp
    # def get_name(self) -> str:
    #     """
    #     Returns the leaf instance name of this component.
    #     """
    #     ...

    @imp
    def get_full_name(self) -> str:
        """
        Returns the full hierarchical path to this component.

        Behavior:

        - Concatenates ancestor full name with this component's leaf name.
        - Top-level components may return the leaf name.
        """
        ...

    @imp
    def get_parent(self) -> object:
        """
        Gets the parent UVM Component

        :returns: Parent UVM component
        """
        ...

    # @imp
    # def sprint(self) -> str:
    #     """
    #     Returns a formatted string representation of this component.

    #     Behavior:

    #     - Mirrors UVM sprint semantics for components; uses SV printer policy.
    #     """
    #     ...

    @property
    def children(self) -> List[object]:
        return self.get_children()
    
    def __getattr__(self, name):
        if self._child_m is None:
            m = {}
            for c in self.get_children():
                cc = cast(uvm_component_p, c)
                m[cc.get_name()] = cc
            self._child_m = m
        if name in self._child_m.keys():
            return self._child_m[name]
        else:
            return super().__getattr__(name)

    @imp
    def get_children(self) -> List[object]:
        """
        Returns the immediate child components of this component.

        Notes:

        - Order is implementation-defined.
        - Returned elements are component handles/proxies.
        """
        ...

    @imp
    def get_config_object(self, name : str, clone : bool=True) -> Tuple[bool, uvm_object]:
        """
        Retrieves a configuration object for the given field name.

        :param name: Configuration field name (no wildcards).
        :returns: A tuple ``(found, value)`` where:
                  - ``found`` is ``True`` when a matching configuration is available, else ``False``.
                  - ``value`` is the configuration object when found; unspecified otherwise.
        :rtype: Tuple[bool, uvm_object]

        Notes:

        - Mirrors UVM ``get_config_object`` semantics; clone behavior and precedence are
          handled in SV (global table, then hierarchy).
        - Callers typically cast the returned object to the expected type.
        """
        ...

    @imp
    def create_object(self, requested_type_name : str, name : str = "") -> uvm_object: 
        ...

    @imp
    def create_component(self, requested_type_name : str, name : str) -> uvm_object: 
        ...

    def accept(self, v : uvm_visitor):
        v.visit_component(self)
