import dataclasses as dc
from typing import List, Optional
from enum import Enum

class UvmFieldKind(Enum):
    INT = "int"
    STR = "str"
    OBJ = "obj"

@dc.dataclass
class UvmFieldType(object):
    name: str
    kind: UvmFieldKind = UvmFieldKind.INT
    size: int = -1
    is_signed: bool = False
    obj_type: Optional['UvmObjectType'] = None

@dc.dataclass
class UvmObjectType(object):
    can_pack : bool = dc.field(default=True)
    fields : List[UvmFieldType] = dc.field(default_factory=list)

    pass
