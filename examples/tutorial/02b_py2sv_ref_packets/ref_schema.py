"""The protocol team's schema for reference packets (pydantic).

This is their data model: readable JSON, addresses as dotted quads, hex
strings, validation. It is not what crosses into SV; see ref_xchg.py.
"""
from enum import Enum
from ipaddress import IPv4Address
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class Expect(str, Enum):
    forward = "forward"
    bad_header = "bad_header"
    bad_checksum = "bad_checksum"
    ttl = "ttl"
    no_route = "no_route"


class RefPacket(BaseModel):
    name: str
    src: IPv4Address
    dst: IPv4Address
    ttl: int = Field(64, ge=0, le=255)
    protocol: Literal["icmp", "tcp", "udp"] = "udp"
    dont_fragment: bool = False
    options: str = Field("", description="Option bytes, hex; a multiple of 4 bytes")
    payload: str = Field("", description="Payload bytes, hex")
    ihl: Optional[int] = Field(None, ge=0, le=15, description="Override IHL (malformed headers)")
    corrupt_checksum: bool = False
    expect: Expect

    @field_validator("options", "payload")
    @classmethod
    def _hex(cls, v):
        bytes.fromhex(v)
        return v

    @field_validator("options")
    @classmethod
    def _opt_len(cls, v):
        if len(bytes.fromhex(v)) % 4 or len(bytes.fromhex(v)) > 40:
            raise ValueError("options must be a multiple of 4 bytes, at most 40")
        return v


class RefSuite(BaseModel):
    description: str = ""
    packets: List[RefPacket]
