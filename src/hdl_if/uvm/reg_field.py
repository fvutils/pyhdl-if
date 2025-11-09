from __future__ import annotations
import abc
from typing import List, TYPE_CHECKING
from .object import uvm_object

if TYPE_CHECKING:
    from .reg import uvm_reg

class uvm_reg_field(uvm_object):
    ...
