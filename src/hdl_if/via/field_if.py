import enum
import typing
from ..decorators import api, imp

if typing.TYPE_CHECKING:
    from .object_type_if import ObjectTypeIF

class ViaFieldKind(enum.IntEnum):
    FIELD_KIND_INT = 0
    FIELD_KIND_STR = 1
    FIELD_KIND_OBJ = 2

@api
class FieldIF(object):

    @imp
    def get_name(self) -> str: pass

    @imp
    def _get_kind(self) -> int: pass

    def get_kind(self) -> ViaFieldKind: 
        return ViaFieldKind(self._get_kind())

    @imp
    def get_size(self) -> int: pass

    @imp
    def get_signed(self) -> bool: pass

    @imp
    def get_obj_type(self) -> object: pass

