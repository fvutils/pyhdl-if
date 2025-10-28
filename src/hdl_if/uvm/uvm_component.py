from __future__ import annotations
from ..decorators import api, imp
from typing import List, Tuple
from .uvm_object import UvmObject

@api
class UvmComponent(UvmObject):
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

    def __del__(self):
        print("__del__", flush=True)

    def randomize(self) -> bool:
        """
        Randomizes this component via the backend.

        Returns:
        - True on success, False otherwise.

        Notes:
        - UVM seeding for components is applied during construction in SV when enabled.
        - This call triggers backend-specific randomization of fields/knobs.
        """
        return self._randomize()

    # Implementation detail
    @imp
    def _randomize(self) -> bool:
        """
        Backend hook invoked by randomize().

        Returns:
        - True on success, False on failure.
        """
        ...

    @imp
    def get_name(self) -> str:
        """
        Returns the leaf instance name of this component.
        """
        ...

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
    def sprint(self) -> str:
        """
        Returns a formatted string representation of this component.

        Behavior:
        - Mirrors UVM sprint semantics for components; uses SV printer policy.
        """
        ...

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
    def get_config_object(self, name : str) -> Tuple[bool, UvmObject]:
        """
        Retrieves a configuration object for the given field name.

        Args:
        - name: Configuration field name (no wildcards).

        Returns:
        - (found: bool, value: UvmObject)
          found = True and value set when a matching configuration is available.
          found = False and value is unspecified otherwise.

        Notes:
        - Mirrors UVM get_config_object semantics; clone behavior and precedence are
          handled in SV (global table, then hierarchy).
        - Callers typically cast the returned object to the expected type.
        """
        ...
