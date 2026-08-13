"""Python view of a SystemVerilog ``uvm_object``."""

import abc
from typing import Protocol
from .visitor import uvm_visitor

class uvm_object(Protocol):
    """The interface a SystemVerilog ``uvm_object`` presents to Python.

    Instances are not created in Python. They arrive as wrappers around a
    SystemVerilog object -- a sequence item handed to a sequence body, an
    object retrieved from the object registry -- and every method here
    delegates across to the SystemVerilog side.

    This is a :class:`typing.Protocol`, so it exists to describe and type-check
    that surface rather than to be subclassed.
    """

    @abc.abstractmethod
    def get_name(self) -> str:
        """Return the object's leaf name."""

    @abc.abstractmethod
    def set_name(self, name: str) -> None:
        """Set the object's leaf name.

        Args:
            name: The new leaf name.
        """

    @abc.abstractmethod
    def get_full_name(self) -> str:
        """Return the object's full hierarchical name."""

    @abc.abstractmethod
    def get_inst_id(self) -> int:
        """Return this object's unique instance id."""

    @abc.abstractmethod
    def get_inst_count(self) -> int:
        """Return the number of ``uvm_object`` instances created so far."""

    @abc.abstractmethod
    def sprint(self) -> str:
        """Return the formatted field dump that :meth:`print` would emit."""

    @abc.abstractmethod
    def get_type_name(self) -> str:
        """Return the object's registered type name."""

    @abc.abstractmethod
    def create(self, name: str = "") -> "uvm_object":
        """Construct a new object of this object's type.

        Args:
            name: Leaf name for the new object.

        Returns:
            The new object, with fields at their defaults.

        See Also:
            :meth:`clone`, which copies field values as well.
        """

    @abc.abstractmethod
    def clone(self) -> "uvm_object":
        """Return a copy of this object, fields included."""

    @abc.abstractmethod
    def print(self) -> None:
        """Print the object's fields through the UVM printer."""

    @abc.abstractmethod
    def convert2string(self) -> str:
        """Return the object's single-line string form."""

    @abc.abstractmethod
    def record(self) -> None:
        """Record the object's fields to the transaction database."""

    @abc.abstractmethod
    def copy(self, rhs: "uvm_object") -> None:
        """Copy field values from another object into this one.

        Args:
            rhs: The object to copy from.
        """

    @abc.abstractmethod
    def compare(self, rhs: "uvm_object") -> bool:
        """Compare this object's fields against another's.

        Args:
            rhs: The object to compare against.

        Returns:
            True if the objects compare equal.
        """

    @abc.abstractmethod
    def set_int_local(self, name: str, value: int) -> None:
        """Set an integral field by name.

        Args:
            name: The field name.
            value: The value to assign.

        Warning:
            Not implemented -- the call returns without assigning anything.
            ``set_*_local`` was generated on ``uvm_object`` by the UVM-1.1
            ``uvm_field_*`` macros and is not part of IEEE 1800.2, which
            replaced it with ``uvm_object::set_local``. Set fields through the
            packed view instead -- see :meth:`pack` and :meth:`unpack`.
        """

    @abc.abstractmethod
    def set_string_local(self, name: str, value: str) -> None:
        """Set a string field by name.

        Args:
            name: The field name.
            value: The value to assign.

        Warning:
            Not implemented. See :meth:`set_int_local`.
        """

    @abc.abstractmethod
    def set_object_local(self, name: str, value: "uvm_object") -> None:
        """Set an object field by name.

        Args:
            name: The field name.
            value: The object to assign.

        Warning:
            Not implemented. See :meth:`set_int_local`.
        """

    @abc.abstractmethod
    def pack(self) -> object:
        """Return the object's fields as a packed value.

        This is the supported route for reading and writing fields from
        Python: pack, modify, then :meth:`unpack`.
        """

    @abc.abstractmethod
    def unpack(self, val : object):
        """Populate the object's fields from a packed value.

        Args:
            val: A packed value of the shape :meth:`pack` returns.
        """

    @abc.abstractmethod
    def randomize(self):
        """Randomize the object on the SystemVerilog side.

        Constraints declared in SystemVerilog are honored.
        """

    @abc.abstractmethod
    def reseed(self) -> None:
        """Reseed the object's random number generator."""

    @abc.abstractmethod
    def accept(self, v : uvm_visitor):
        """Accept a visitor over this object.

        Args:
            v: The visitor to dispatch to.
        """
