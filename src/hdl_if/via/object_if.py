import enum
import dataclasses as dc
from typing import Tuple, List
from ..decorators import api, imp
from .field_if import ViaFieldKind
from .object_type_if import ObjectTypeIF


@api
class ObjectIF(object):

    def __del__(self):
        print("ObjectIF::__del__")

    @imp
    def get_name(self) -> str: pass

    @imp
    def get_object_type(self) -> ObjectTypeIF: pass

    @imp
    def pack_ints(self) -> Tuple[int,List[int]]: pass

    @imp
    def unpack_ints(self, intstream : List[int]) -> int: pass

    def get_pytype(self):
        obj_type = self.get_object_type()
        fields = []
        print("obj_type: %s" % obj_type)
        for f in obj_type.get_fields():
            print("Field: %s" % f.get_name())
            print("Kind: %s" % f.get_kind())
            if f.get_kind() == ViaFieldKind.FIELD_KIND_INT:
                fields.append((f.get_name(), int, dc.field(
                    default=0,
                    metadata={
                        "kind": f.get_kind(),
                        "size": f.get_size()
                    })))
                pass
            pass

        pytype = dc.make_dataclass(
            obj_type.get_name(),
            fields=fields
        )

        return pytype

    def new_value(self) -> object:
        """Creates a new value object"""
        pytype = self.get_pytype()
        return pytype()


    def get_value(self) -> object:
        sz, intstream = self.pack_ints()

        # Need to create a Python object to return
        pytype = self.get_pytype()
        obj = pytype()

        idx = 0
        offset = 32
        for f in dc.fields(pytype):
            val = 0
            sz = f.metadata["size"]
            if sz <= offset:
                # Whole field within the current word
                val = ((intstream[idx] >> (offset-sz)) & ((1 << sz)-1))
                offset -= sz
                if offset <= 0:
                    idx += 1
                    offset = 32
            else:
                remain_sz = sz
                while remain_sz > 0:
                    n_bits = (remain_sz if offset >= remain_sz else offset)
                    val |= ((intstream[idx] >> (offset-n_bits)) & ((1 << n_bits)-1))
                    remain_sz -= n_bits
                    offset -= n_bits
                    if offset <= 0:
                        idx += 1
                        offset = 32
            setattr(obj, f.name, val)
        return obj

    def set_value(self, v : object):
        intstream = [0]

        # Need to create a Python object to return
        pytype = self.get_pytype()

        idx = 0
        offset = 32
        for f in dc.fields(pytype):
            val = 0
            sz = f.metadata["size"]
            if not hasattr(v, f.name):
                raise Exception("Object passed to set_value (%s) does not contain field %s" % (
                    str(type(v)), f.name))
            val = getattr(v, f.name)
            if sz <= offset:
                # Whole field within the current word
                print("val: %08x sz=%d offset=%d" % (val, sz, offset))
                intstream[idx] |= ((val & ((1 << sz)-1)) << (offset-sz))
                offset -= sz
                if offset <= 0:
                    idx += 1
                    intstream.append(0)
                    offset = 32
            else:
                remain_sz = sz
                while remain_sz > 0:
                    n_bits = (remain_sz if offset >= remain_sz else offset)
                    intstream[idx] |= (((val >> (remain_sz-n_bits)) & ((1 << n_bits)-1)) << (offset-n_bits))
                    remain_sz -= n_bits
                    offset -= n_bits
                    if offset <= 0:
                        idx += 1
                        offset = 32
                        intstream.append(0)

        self.unpack_ints(intstream)
        pass


