#!/usr/bin/env python3
import os
import sys

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from typing import Any
from hdl_if.uvm.wrap import UvmObjectType, UvmFieldKind
from hdl_if.uvm.wrap import uvm_object_rgy as UvmObjectRgy

def test_populate_fields_captures_typename_and_uses_for_dataclass():
    layout = """
------------------------------------
Name      Type      Size  Value
------------------------------------
seq_item  seq_item  -     @560
  addr    integral  8     'hf6
  write   integral  1     'h1
  data    integral  32    'h8efd96e4
  tid     integral  4     'h7
------------------------------------
""".strip("\n")

    obj_t = UvmObjectType()
    rgy: Any = UvmObjectRgy()  # type: ignore  # Pylance: @api wrapper is generic; treat as Any
    rgy.populate_fields(obj_t, layout)

    # Type name captured from the first data line (Type column)
    assert obj_t.type_name == "seq_item"

    # Dataclass is created with that typename
    assert obj_t.data_t is not None
    assert obj_t.data_t.__name__ == "seq_item"

    # Fields parsed correctly
    assert len(obj_t.fields) == 4
    assert obj_t.fields[0].name == "addr" and obj_t.fields[0].size == 8 and obj_t.fields[0].kind == UvmFieldKind.INT
    assert obj_t.fields[1].name == "write" and obj_t.fields[1].size == 1
    assert obj_t.fields[2].name == "data" and obj_t.fields[2].size == 32
    assert obj_t.fields[3].name == "tid" and obj_t.fields[3].size == 4
